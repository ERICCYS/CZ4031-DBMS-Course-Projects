\t
\a

explain(format json) select sum(totalprice) as spend, customer.name, nation.name from customer, nation, orders where customer.custkey = orders.custkey and customer.nationkey = nation.nationkey group by customer.custkey, nation.name having sum(totalprice) >= 4000000 order by spend desc;

\g '/Users/eric/Desktop/Data/query_2/query_2b.json'