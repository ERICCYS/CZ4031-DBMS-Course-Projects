\t
\a

explain (analyze, costs, verbose, buffers, format json) select count(*) as customer_count, region.name from customer, nation, region where customer.nationkey = nation.nationkey and nation.regionkey = region.regionkey group by region.name order by customer_count desc;

\g './queries/query_3/query_3a.json'