\t
\a

explain (analyze, costs, verbose, buffers, format json) select customer.custkey, customer.name, nation.name from customer, nation where customer.nationkey = nation.nationkey and customer.acctbal >= 1000 and nation.nationkey >= 10  order by customer.custkey desc;


\g './queries/query_1/query_1a.json'