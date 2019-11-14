\t
\a

explain (analyze, costs, verbose, buffers, format json) select orders.orderkey, orders.orderdate, customer.custkey, customer.name from customer, orders where customer.custkey = orders.custkey and orders.orderkey >= 40000 and customer.custkey >= 50000;

\g './queries/query_2/query_2a.json'