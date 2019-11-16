\t
\a

explain (analyze, costs, verbose, buffers, format json) select customer.custkey, customer.name, nation_a.name
from customer, (select nationkey, name from nation where nationkey >= 10) as nation_a
where customer.nationkey = nation_a.nationkey and customer.acctbal >= 1000
order by customer.custkey desc;

\g './queries/query_4/query_4a.json'