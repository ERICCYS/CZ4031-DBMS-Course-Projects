\t
\a

explain (analyze, costs, verbose, buffers, format json) select count(*) as customer_count, nation.name from customer, nation where customer.nationkey = nation.nationkey group by nation.name having count(*) >= 6000 order by customer_count desc;

\g './queries/query_3/query_3b.json'