\t
\a

explain(format json) select count(*) as customer_count, region.name from customer, nation, region where customer.nationkey = nation.nationkey and nation.regionkey = region.regionkey group by region.name order by customer_count desc;

\g '/Users/eric/Desktop/Data/query_3/query_3a.json'