\t
\a

explain (analyze, costs, verbose, buffers, format json) select orders.orderkey, orders.orderdate, customer.custkey, customer.name from customer, orders where customer.custkey = orders.custkey and orders.orderdate >= '1996-01-01' and customer.nationkey >= 10;

\g './queries/query_2/query_2b.json'