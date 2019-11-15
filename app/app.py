import sys
import json
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from query_description import *
from pyconnect import DBConnection


class App(object):

    def __init__(self, parent):
        self.root = parent
        self.root.title("Main Frame")
        self.frm_input_text = tk.Frame(self.root)
        self.frm_input_text.pack()
        self.frm_input = tk.Frame(self.root)
        self.frm_input.pack()
        self.frm_line = tk.Frame(self.root)
        self.frm_line.pack()
        canvas = Canvas(self.frm_line,width = 2000,height = 20)
        canvas.create_line(0,15,2000,15)
        canvas.pack()
        self.frm_nlp_text = tk.Frame(self.root)
        self.frm_nlp_text.pack()
        self.frm_nlp = tk.Frame(self.root)
        self.frm_nlp.pack()
        self.frm_tree_text = tk.Frame(self.root)
        self.frm_tree_text.pack()
        self.frm_tree = tk.Frame(self.root)
        self.frm_tree.pack()
        self.frm_diff_text = tk.Frame(self.root)
        self.frm_diff_text.pack()   
        self.frm_diff = tk.Frame(self.root)
        self.frm_diff.pack()   

        self.frm_input_t = tk.Frame(self.frm_input)
        self.frm_input_t.pack(side = LEFT)
        self.frm_input_btt = tk.Frame(self.frm_input)
        self.frm_input_btt.pack(side = RIGHT)

        self.frm_nlp_t = tk.Frame(self.frm_nlp)
        self.frm_nlp_t.pack(side = LEFT)
        self.frm_nlp_btt = tk.Frame(self.frm_nlp)
        self.frm_nlp_btt.pack(side = RIGHT)

        self.frm_tree_t = tk.Frame(self.frm_tree)
        self.frm_tree_t.pack(side = LEFT)
        self.frm_tree_btt = tk.Frame(self.frm_tree)
        self.frm_tree_btt.pack(side = RIGHT)

        self.frm_tree_t = tk.Frame(self.frm_tree)
        self.frm_tree_t.pack(side = LEFT)
        self.frm_tree_btt = tk.Frame(self.frm_tree)
        self.frm_tree_btt.pack(side = RIGHT)

        self.frm_diff_t = tk.Frame(self.frm_diff)
        self.frm_diff_t.pack(side = LEFT)
        self.frm_diff_btt = tk.Frame(self.frm_diff)
        self.frm_diff_btt.pack(side = RIGHT)

        self.input_text1 = tk.Label(self.frm_input_text, text='Please input old query:', font=(None, 16),width = 60)
        self.input_text1.pack(side = LEFT,pady =5)
        self.input_text2 = tk.Label(self.frm_input_text, text='Please input new query:                     ', font=(None, 16), width = 75)
        self.input_text2.pack(side = RIGHT,pady =5)

        self.input1 = tk.Text(self.frm_input_t, relief=GROOVE, width=75, height=8, borderwidth=5, font=(None, 12))
        self.input1.pack(side=LEFT, padx = 10)
        self.input2 = tk.Text(self.frm_input_t, relief=RIDGE, width=75, height=8, borderwidth=5, font=(None, 12))
        self.input2.pack(side=RIGHT, padx = 10)

        self.view = tk.Button(self.frm_input_btt, text="view output", width=10, height=2, command=self.retrieve_input)
        self.view.pack(pady = 10)
        
        self.clear = tk.Button(self.frm_input_btt, text="clear input", width=10, height=2, command=self.clear_input)
        self.clear.pack(pady = 10)

 
        self.nlp_text1 = tk.Label(self.frm_nlp_text, text='Old query execution plan:', font=(None, 16),width = 60)
        self.nlp_text1.pack(side = LEFT,pady =5)
        self.nlp_text2 = tk.Label(self.frm_nlp_text, text='New query execution plan:                     ', font=(None, 16), width = 75)
        self.nlp_text2.pack(side = RIGHT,pady =5)

        self.nlp1 = tk.Text(self.frm_nlp_t, relief=GROOVE, width=75, height=8, borderwidth=5, font=(None, 12),state ='disabled')
        self.nlp1.pack(side=LEFT, padx = 10)
        self.nlp2 = tk.Text(self.frm_nlp_t, relief=RIDGE, width=75, height=8, borderwidth=5, font=(None, 12),state ='disabled')
        self.nlp2.pack(side=RIGHT, padx = 10)
        self.placeholder1 = tk.Label(self.frm_nlp_btt,width = 10)
        self.placeholder1.pack()

        self.tree_text1 = tk.Label(self.frm_tree_text, text='Old query tree structure:', font=(None, 16),width = 60)
        self.tree_text1.pack(side = LEFT,pady =5)
        self.tree_text2 = tk.Label(self.frm_tree_text, text='New query tree structure:                     ', font=(None, 16), width = 75)
        self.tree_text2.pack(side = RIGHT,pady =5)

        self.tree1 = tk.Text(self.frm_tree_t, relief=GROOVE, width=75, height=8, borderwidth=5, font=(None, 12),state ='disabled')
        self.tree1.pack(side=LEFT, padx = 10)
        self.tree2 = tk.Text(self.frm_tree_t, relief=RIDGE, width=75, height=8, borderwidth=5, font=(None, 12),state ='disabled')
        self.tree2.pack(side=RIGHT, padx = 10)
        self.placeholder2 = tk.Label(self.frm_tree_btt,width = 10)
        self.placeholder2.pack()

        self.placeholder3 = tk.Label(self.frm_diff_text,width = 60)
        self.placeholder3.pack(pady =5)

        self.diff_text = tk.Label(self.frm_diff_text, text='Difference between two query plans:', font=(None, 16),width = 60)
        self.diff_text.pack(side = LEFT,pady =5)

        self.diff = tk.Text(self.frm_diff_t, relief=GROOVE, width=155, height=8, borderwidth=5, font=(None, 12),state ='disabled')
        self.diff.pack(side=LEFT, padx = 10)

        self.clear_out = tk.Button(self.frm_diff_btt, text="clear output", width=10, height=2, command=self.clear_output)
        self.clear_out.pack(pady = 10)

        self.quit_ = tk.Button(self.frm_diff_btt, text="quit program", width=10, height=2, command=self.quitprogram)
        self.quit_.pack(pady = 10)

    def retrieve_input(self):
        global query_old
        global query_new
        global desc
        global result
        query_old = self.input1.get("1.0", END)
        query_new = self.input2.get("1.0", END)
        result_old = self.get_query_result(query_old)
        result_new = self.get_query_result(query_new)
        result_old_obj = json.loads(json.dumps(result_old))
        result_new_obj = json.loads(json.dumps(result_new))
        result_old_nlp = self.get_description(result_old_obj)
        result_new_nlp = self.get_description(result_new_obj)
        result_old_tree = self.get_tree(result_old_obj)
        result_new_tree = self.get_tree(result_new_obj)
        result_diff = self.get_difference(result_old_obj, result_new_obj)
        self.nlp1.configure(state ='normal')
        self.nlp2.configure(state ='normal')
        self.tree1.configure(state ='normal')
        self.tree2.configure(state ='normal')
        self.diff.configure(state ='normal')
        
        self.nlp1.delete("1.0", END)
        self.nlp1.insert(END,result_old_nlp)
        self.nlp2.delete("1.0", END)
        self.nlp2.insert(END,result_new_nlp)
        self.tree1.delete("1.0", END)
        self.tree1.insert(END,result_old_tree)
        self.tree2.delete("1.0", END)
        self.tree2.insert(END,result_new_tree)
        self.diff.delete("1.0", END)
        self.diff.insert(END,result_diff)

    def clear_input(self):
        self.input1.delete("1.0", END)
        self.input2.delete("1.0", END)

    def clear_output(self):
        self.nlp1.delete("1.0", END)
        self.nlp2.delete("1.0", END)
        self.tree1.delete("1.0", END)
        self.tree2.delete("1.0", END)
        self.diff.delete("1.0", END)
        self.nlp1.configure(state ='disabled')
        self.nlp2.configure(state ='disabled')
        self.tree1.configure(state ='disabled')
        self.tree2.configure(state ='disabled')
        self.diff.configure(state ='disabled')

    def get_query_result(self, query):
        # DBConnection takes 4 arguments
        host="localhost" 
        port = 5432
        database="tpch_db"
        user="eric"
        password=""

        connection = DBConnection()
        result = connection.execute(query)[0][0]
        connection.close()
        return result

    def get_description(self, json_obj):
        descriptions = get_text(json_obj)
        result = ""
        for description in descriptions:
            result = result + description + "\n"
        return result

    def get_tree(self, json_obj):
        head = parse_json(json_obj)
        return generate_tree("", head)
    
    def get_difference(self, json_object_A, json_object_B):
        diff = get_diff(json_object_A, json_object_B)
        return diff
        

    def quitprogram(self):
        result = messagebox.askokcancel("Quit the game.", "Are you sure?", icon='warning')
        if result == True:
            self.root.destroy()
#			root.update()
#			root.deiconify()		


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.geometry('1500x1000+0+0')
    root.mainloop()
