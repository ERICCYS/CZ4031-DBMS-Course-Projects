from __future__ import print_function
import logging
import json
import argparse
import copy
import random
import string
import os
import queue


class Node(object):
    def __init__(self, node_type, relation_name, schema, alias, group_key, sort_key, join_type, index_name, 
            hash_cond, table_filter, index_cond, merge_cond, recheck_cond, join_filter, subplan_name, actual_rows,
            actual_time,description):
        self.node_type = node_type
        self.children = []
        self.relation_name = relation_name
        self.schema = schema
        self.alias = alias
        self.group_key = group_key
        self.sort_key = sort_key
        self.join_type = join_type
        self.index_name = index_name
        self.hash_cond = hash_cond
        self.table_filter = table_filter
        self.index_cond = index_cond
        self.merge_cond = merge_cond
        self.recheck_cond = recheck_cond
        self.join_filter = join_filter
        self.subplan_name = subplan_name
        self.actual_rows = actual_rows
        self.actual_time = actual_time
        self.description = description

    def add_children(self, child):
        self.children.append(child)
    
    def set_output_name(self, output_name):
        if "T" == output_name[0] and output_name[1:].isdigit():
            self.output_name = int(output_name[1:])
        else:
            self.output_name = output_name

    def get_output_name(self):
        if str(self.output_name).isdigit():
            return "T" + str(self.output_name)
        else:
            return self.output_name

    def set_step(self, step):
        self.step = step
    
    def update_desc(self,desc):
        self.description = desc


def parse_json(json_obj):
    q = queue.Queue()
    q_node = queue.Queue()
    plan = json_obj[0]['Plan']
    q.put(plan)
    q_node.put(None)

    while not q.empty():
        current_plan = q.get()
        parent_node = q_node.get()

        relation_name = schema = alias = group_key = sort_key = join_type = index_name = hash_cond = table_filter \
            = index_cond = merge_cond = recheck_cond = join_filter = subplan_name = actual_rows = actual_time = description = None
        if 'Relation Name' in current_plan:
            relation_name = current_plan['Relation Name']
        if 'Schema' in current_plan:
            schema = current_plan['Schema']
        if 'Alias' in current_plan:
            alias = current_plan['Alias']
        if 'Group Key' in current_plan:
            group_key = current_plan['Group Key']
        if 'Sort Key' in current_plan:
            sort_key = current_plan['Sort Key']
        if 'Join Type' in current_plan:
            join_type = current_plan['Join Type']
        if 'Index Name' in current_plan:
            index_name = current_plan['Index Name']
        if 'Hash Cond' in current_plan:
            hash_cond = current_plan['Hash Cond']
        if 'Filter' in current_plan:
            table_filter = current_plan['Filter']
        if 'Index Cond' in current_plan:
            index_cond = current_plan['Index Cond']
        if 'Merge Cond' in current_plan:
            merge_cond = current_plan['Merge Cond']
        if 'Recheck Cond' in current_plan:
            recheck_cond = current_plan['Recheck Cond']
        if 'Join Filter' in current_plan:
            join_filter = current_plan['Join Filter']
        if 'Actual Rows' in current_plan:
            actual_rows = current_plan['Actual Rows']
        if 'Actual Total Time' in current_plan:
            actual_time = current_plan['Actual Total Time']
        if 'Subplan Name' in current_plan:
            if "returns" in current_plan['Subplan Name']:
                name = current_plan['Subplan Name']
                subplan_name = name[name.index("$"):-1]
            else:
                subplan_name = current_plan['Subplan Name']

        current_node = Node(current_plan['Node Type'], relation_name, schema, alias, group_key, sort_key, join_type,
                            index_name, hash_cond, table_filter, index_cond, merge_cond, recheck_cond, join_filter,
                            subplan_name, actual_rows, actual_time, description)

        if "Limit" == current_node.node_type:
            current_node.plan_rows = current_plan['Plan Rows']

        if "Scan" in current_node.node_type:
            if "Index" in current_node.node_type:
                if relation_name:
                    current_node.set_output_name(
                        relation_name + " with index " + index_name)
            elif "Subquery" in current_node.node_type:
                current_node.set_output_name(alias)
            else:
                current_node.set_output_name(relation_name)

        if parent_node is not None:
            parent_node.add_children(current_node)
        else:
            head_node = current_node

        if 'Plans' in current_plan:
            for item in current_plan['Plans']:
                # push child plans into queue
                q.put(item)
                # push parent for each child into queue
                q_node.put(current_node)

    return head_node


def simplify_graph(node):
    new_node = copy.deepcopy(node)
    new_node.children = []

    for child in node.children:
        new_child = simplify_graph(child)
        new_node.add_children(new_child)
        new_node.actual_time -= child.actual_time

    if node.node_type in ["Result"]:
        return node.children[0]

    return new_node


def parse_cond(op_name, conditions, table_subquery_name_pair):
    if isinstance(conditions,str):
        if "::" in conditions:
            return conditions.replace("::", " ")[1:-1]
        return conditions[1:-1]
    cond = ""
    for i in range (len(conditions)):
        cond = cond + conditions[i]
        if (not (i == len(conditions)-1)):
            cond = cond + "and"
    return cond


def to_text(node, skip=False):
    global steps, cur_step, cur_table_name
    increment = True
    # skip the child if merge it with current node
    if node.node_type in ["Unique", "Aggregate"] and len(node.children) == 1 \
            and ("Scan" in node.children[0].node_type or node.children[0].node_type == "Sort"):
        children_skip = True
    elif node.node_type == "Bitmap Heap Scan" and node.children[0].node_type == "Bitmap Index Scan":
        children_skip = True
    else:
        children_skip = False

    # recursive
    for child in node.children:
        if node.node_type == "Aggregate" and len(node.children) > 1 and child.node_type == "Sort":
            to_text(child, True)
        else:
            to_text(child, children_skip)

    if node.node_type in ["Hash"] or skip:
        return

    step = ""

    # generate natural language for various QEP operators
    if "Join" in node.node_type:
        # special preprocessing for joins
        if node.join_type == "Semi":
            # add the word "Semi" before "Join" into node.node_type
            node_type_list = node.node_type.split()
            node_type_list.insert(-1, node.join_type)
            node.node_type = " ".join(node_type_list)
        else:
            pass

        if "Hash" in node.node_type:
            step += " and perform " + node.node_type.lower() + " on "
            for i, child in enumerate(node.children):
                if child.node_type == "Hash":
                    child.set_output_name(child.children[0].get_output_name())
                    hashed_table = child.get_output_name()
                if i < len(node.children) - 1:
                    step += ("table " + child.get_output_name())
                else:
                    step += (" and table " + child.get_output_name())
            # combine hash with hash join
            step = "hash table " + hashed_table + step + " under condition " + \
                parse_cond("Hash Cond", node.hash_cond,
                           table_subquery_name_pair)

        elif "Merge" in node.node_type:
            step += "perform " + node.node_type.lower() + " on "
            any_sort = False  # whether sort is performed on any table
            for i, child in enumerate(node.children):
                if child.node_type == "Sort":
                    child.set_output_name(child.children[0].get_output_name())
                    any_sort = True
                if i < len(node.children) - 1:
                    step += ("table " + child.get_output_name())
                else:
                    step += (" and table " + child.get_output_name())
            # combine sort with merge join
            if any_sort:
                sort_step = "sort "
                for child in node.children:
                    if child.node_type == "Sort":
                        if i < len(node.children) - 1:
                            sort_step += ("table " + child.get_output_name())
                        else:
                            sort_step += (" and table " +
                                          child.get_output_name())
                step = sort_step + " and " + step

    elif node.node_type == "Bitmap Heap Scan":
        # combine bitmap heap scan and bitmap index scan
        if "Bitmap Index Scan" in node.children[0].node_type:
            node.children[0].set_output_name(node.relation_name)
            step = " with index condition " + \
                parse_cond("Recheck Cond", node.recheck_cond,
                           table_subquery_name_pair)

        step = "perform bitmap heap scan on table " + \
            node.children[0].get_output_name() + step

    elif "Scan" in node.node_type:
        if node.node_type == "Seq Scan":
            step += "perform sequential scan on table "
        else:
            step += "perform " + node.node_type.lower() + " on table "

        step += node.get_output_name()

        # if no table filter, remain original table name
        if not node.table_filter:
            increment = False

    elif node.node_type == "Unique":
        # combine unique and sort
        if "Sort" in node.children[0].node_type:
            node.children[0].set_output_name(
                node.children[0].children[0].get_output_name())
            step = "sort " + node.children[0].get_output_name()
            if node.children[0].sort_key:
                step += " with attribute " + \
                    parse_cond(
                        "Sort Key", node.children[0].sort_key, table_subquery_name_pair) + " and "

            else:
                step += " and "

        step += "perform unique on table " + node.children[0].get_output_name()

    elif node.node_type == "Aggregate":
        for child in node.children:
            # combine aggregate and sort
            if "Sort" in child.node_type:
                child.set_output_name(child.children[0].get_output_name())
                step = "sort " + child.get_output_name() + " and "
            # combine aggregate with scan
            if "Scan" in child.node_type:
                if child.node_type == "Seq Scan":
                    step = "perform sequential scan on " + child.get_output_name() + " and "
                else:
                    step = "perform " + child.node_type.lower() + " on " + \
                        child.get_output_name() + " and "

        step += "perform aggregate on table " + \
            node.children[0].get_output_name()
        if len(node.children) == 2:
            step += " and table " + node.children[1].get_output_name()

    elif node.node_type == "Sort":
        step += "perform sort on table " + node.children[0].get_output_name(
        ) + " with attribute " + parse_cond("Sort Key", node.sort_key, table_subquery_name_pair)

    elif node.node_type == "Limit":
        step += "limit the result from table " + \
            node.children[0].get_output_name() + " to " + \
            str(node.plan_rows) + " record(s)"

    else:
        step += "perform " + node.node_type.lower() + " on"
        # binary operator
        if len(node.children) > 1:
            for i, child in enumerate(node.children):
                if i < len(node.children) - 1:
                    step += (" table " + child.get_output_name() + ",")
                else:
                    step += (" and table " + child.get_output_name())
        # unary operator
        else:
            step += " table " + node.children[0].get_output_name()

    # add conditions
    if node.group_key:
        step += " with grouping on attribute " + \
            parse_cond("Group Key", node.group_key, table_subquery_name_pair)

    if node.table_filter:
        step += " and filtering on " + \
            parse_cond("Table Filter", node.table_filter,
                       table_subquery_name_pair)

    if node.join_filter:
        step += " while filtering on " + \
            parse_cond("Join Filter", node.join_filter,
                       table_subquery_name_pair)

    # set intermediate table name
    if increment:
        node.set_output_name("T" + str(cur_table_name))
        step += " to get intermediate table " + node.get_output_name()
        cur_table_name += 1
    if node.subplan_name:
        table_subquery_name_pair[node.subplan_name] = node.get_output_name()

    node.update_desc(step)
    step = "Step " + str(cur_step) + ", " + step + "."
    node.set_step(cur_step)
    cur_step += 1

    steps.append(step)


def random_word(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def get_text(json_obj):
    global steps, cur_step, cur_table_name, table_subquery_name_pair
    global current_plan_tree
    steps = ["The query is executed as follow."]
    cur_step = 1
    cur_table_name = 1
    table_subquery_name_pair = {}

    head_node = parse_json(json_obj)
    simplified_graph = simplify_graph(head_node)

    to_text(simplified_graph)
    if " to get intermediate table" in steps[-1]:
        steps[-1] = steps[-1][:steps[-1].index(
            " to get intermediate table")] + ' to get the final result.'

    return steps

def clear_cache():
    global steps, cur_step, cur_table_name, table_subquery_name_pair
    steps = []
    cur_step = 1
    cur_table_name = 1
    table_subquery_name_pair = {}

def generate_tree(tree, node, _prefix="", _last=True):
    if _last:
        tree = "{}`-- {}\n".format(_prefix, node.node_type)
    else:
        tree = "{}|-- {}\n".format(_prefix, node.node_type)

    _prefix += "   " if _last else "|  "
    child_count = len(node.children)
    for i, child in enumerate(node.children):
        _last = i == (child_count - 1)
        tree = tree + generate_tree(tree, child, _prefix, _last)
    return tree


def generate_why(node_a, node_b, num):

    text = ""
    if node_a.node_type =="Index Scan" and node_b.node_type == "Seq Scan":
        text = "Reason for Difference " + str(num) + ": " 
        text += node_a.node_type + " in P1 on relation " + node_a.relation_name + " has now evolved to Sequential Scan in P2 on relation " + node_b.relation_name + ". This is because "
        if node_b.index_name is None:
            text += "P1 uses the index, i.e. " + node_a.index_name + ", for selection while P2 doesn't. "
        if int(node_a.actual_rows) < int(node_b.actual_rows):
            text += "and the actual row number increases from " + str(node_a.actual_rows) + " to " + str(node_b.actual_rows) + ", "

        if node_a.index_cond != node_b.table_filter and int(node_a.actual_rows) < int(node_b.actual_rows):
            text += "This may be due to the selection predicates change from " + (node_a.index_cond if node_a.index_cond is not None else "None ") + " to " + (node_b.table_filter if node_b.table_filter is not None else "None ") + ". "
        
    elif node_b.node_type =="Index Scan" and node_a.node_type == "Seq Scan":
        text = "Reason for Difference " + str(num) + ": " 
        text += "Sequential Scan in P1 on relation " + node_a.relation_name + " has now evolved to " + node_b.node_type +" in P2 on relation " + node_b.relation_name + ". This is because "
        if  node_a.index_name is None:  
            text += "P2 uses the index, i.e. " + node_b.index_name + ", for selection while P1 doesn't. "
        elif node_a.index_name is not None:
            text += "Both P1 and P2 uses the index, which are respectively " + node_a.index_name + " and " + node_b.index_name + ". "
        if int(node_a.actual_rows) > int(node_b.actual_rows):
            text += "and the actual row number decreases from " + str(node_a.actual_rows) + " to " + str(node_b.actual_rows) + ". "
        if node_a.table_filter != node_b.index_cond and int(node_a.actual_rows) > int(node_b.actual_rows):
            text += "This may be due to the selection predicate changes from " + (node_a.table_filter if node_a.table_filter is not None else "None") + " to " + (node_b.index_cond if node_b.index_cond is not None else "None") + ". "

    elif node_a.node_type and node_b.node_type in ['Merge Join', "Hash Join", "Nested Loop"]:
        text = "Reason for Difference " + str(num) + ": " 
        if node_a.node_type == "Nested Loop" and node_b.node_type == "Merge Join":
            text += node_a.node_type + " in P1 on has now evolved to " + node_b.node_type +" in P2 on relation " + ". This is because "
            if int(node_a.actual_rows) < int(node_b.actual_rows):
                text += "the actual row number increases from " + str(node_a.actual_rows) + " to " + str(node_b.actual_rows) + ", "
            if "=" in node_b.node_type:
                text += "The join condition uses an equality operator. "
            text += "The both side of the Join operator of P2 can be sorted on the join condition efficiently . "

        if node_a.node_type == "Nested Loop" and node_b.node_type == "Hash Join":
            text += node_a.node_type + " in P1 on has now evolved to " + node_b.node_type +" in P2 on relation " + ". This is because "
            if int(node_a.actual_rows) < int(node_b.actual_rows):
                text += "the actual row number increases from " + str(node_a.actual_rows) + " to " + str(node_b.actual_rows) + ". "
            if "=" in node_b.node_type:
                text += "The join condition uses an equality operator. "
                
        if node_a.node_type == "Merge Join" and node_b.node_type == "Nested Loop":
            text += node_a.node_type + " in P1 on has now evolved to " + node_b.node_type +" in P2 on relation " + ". This is because "
            if int(node_a.actual_rows) > int(node_b.actual_rows):
                text += "the actual row number decreases from " + str(node_a.actual_rows) + " to " + str(node_b.actual_rows) + ". "
            elif int(node_a.actual_rows) < int(node_b.actual_rows):
                text += "the actual row number increases from " + str(node_a.actual_rows) + " to " + str(node_b.actual_rows) + ". "
                text += node_b.node_type + " joins are used  if the join condition does not use the equality operator"
            
        if node_a.node_type == "Merge Join" and node_b.node_type == "Hash Join":
            text += node_a.node_type + " in P1 on has now evolved to " + node_b.node_type +" in P2 on relation " + ". " 
            if int(node_a.actual_rows) < int(node_b.actual_rows):
                text += "This is because the actual row number increases from " + str(node_a.actual_rows) + " to " + str(node_b.actual_rows) + ". "
            if int(node_a.actual_rows) > int(node_b.actual_rows):
                text += "The actual row number decreases from " + str(node_a.actual_rows) + " to " + str(node_b.actual_rows) + ". "
            text += "The both side of the Join operator of P2 can be sorted on the join condition efficiently . "

        if node_a.node_type == "Hash Join" and node_b.node_type == "Nested Loop":
            text += node_a.node_type + " in P1 on has now evolved to " + node_b.node_type +" in P2 on relation " + ". This is because "
            if int(node_a.actual_rows) > int(node_b.actual_rows):
                text += "the actual row number decreases from " + str(node_a.actual_rows) + " to " + str(node_b.actual_rows) + ". "
            elif int(node_a.actual_rows) < int(node_b.actual_rows):
                text += "the actual row number increases from " + str(node_a.actual_rows) + " to " + str(node_b.actual_rows) + ". "
                text += node_b.node_type + " joins are used  if the join condition does not use the equality operator"

        if node_a.node_type == "Hash Join" and node_b.node_type == "Merge Join":
            text += node_a.node_type + " in P1 on has now evolved to " + node_b.node_type +" in P2 on relation " + ". " 
            if int(node_a.actual_rows) < int(node_b.actual_rows):
                text += "The actual row number increases from " + str(node_a.actual_rows) + " to " + str(node_b.actual_rows) + ". "
            if int(node_a.actual_rows) > int(node_b.actual_rows):
                text += "The actual row number decreases from " + str(node_a.actual_rows) + " to " + str(node_b.actual_rows) + ". "
            text += "The both side of the Join operator of P2 can be sorted on the join condition efficiently. "

    return text


def modify_text(str):
    str = str.replace('perform ', '')
    return str

def check_children(nodeA, nodeB, difference, reasons):
    global num
    childrenA = nodeA.children
    childrenB = nodeB.children
    children_no_A = len(childrenA)
    children_no_B = len(childrenB)

    if nodeA.node_type == nodeB.node_type and children_no_A == children_no_B:
        if children_no_A != 0:
            for i in range(len(childrenA)):
                check_children(childrenA[i], childrenB[i],  difference, reasons)

    else:
        if nodeA.node_type == 'Hash' or nodeA.node_type == 'Sort':
            text = 'Difference ' + \
                str(num) + ' : ' + nodeA.children[0].description + \
                ' has been changed to ' + nodeB.description
            text = modify_text(text)
            difference.append(text)
            reason = generate_why(nodeA.children[0], nodeB, num)
            reasons.append(reason)
            num += 1

        elif nodeB.node_type == 'Hash' or nodeB.node_type == 'Sort':
            text = 'Difference ' + str(num) + ' : ' + nodeA.description + \
                ' has been changed to ' + nodeB.children[0].description
            text = modify_text(text)
            difference.append(text)
            reason = generate_why(nodeA, nodeB.children[0], num)
            reasons.append(reason)
            num += 1

        elif 'Gather' in nodeA.node_type:
            check_children(childrenA[0], nodeB, difference, reasons)

        elif 'Gather' in nodeB.node_type:
            check_children(nodeA, childrenB[0],  difference, reasons)
        else:
            text = 'Difference ' + \
                str(num) + ' : ' + nodeA.description + \
                ' has been changed to ' + nodeB.description
            text = modify_text(text)
            difference.append(text)
            reason = generate_why(nodeA, nodeB, num)
            reasons.append(reason)
            num += 1

        if children_no_A == children_no_B:
            if children_no_A == 1:
                check_children(childrenA[0], childrenB[0], difference, reasons)
            if children_no_A == 2:
                check_children(childrenA[0], childrenB[0], difference, reasons)
                check_children(childrenA[1], childrenB[1],  difference, reasons)

def get_diff(json_obj_A, json_obj_B):
    global num
    head_node_a = parse_json(json_obj_A)
    clear_cache()
    to_text(head_node_a)

    head_node_b = parse_json(json_obj_B)
    clear_cache()
    to_text(head_node_b)

    num=1
    difference = []
    reasons = []
    check_children(head_node_a, head_node_b, difference, reasons)
    diff_str = ""
    for i in range (len(reasons)):
        diff_str = diff_str + difference[i] + "\n\n"
        if reasons[i] != "":
            diff_str = diff_str + reasons[i] + "\n" 
        if i != len(reasons)-1:
            diff_str = diff_str + "-"*200 + "\n"
    return diff_str
