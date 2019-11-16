\t
\a

explain (analyze, costs, verbose, buffers, format json) select customer_a.custkey, customer_a.name, nation.name
from (select name, custkey, nationkey from customer where customer.custkey <= 750) as customer_a, nation
where customer_a.nationkey = nation.nationkey and nation.nationkey >= 10
order by customer_a.custkey desc;

\g './queries/query_4/query_4b.json'