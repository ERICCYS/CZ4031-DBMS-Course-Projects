\t
\a

explain (analyze, costs, verbose, buffers, format json) select * from nation, region where nation.regionkey = region.regionkey and nation.nationkey >= 15;

\g './queries/query_5/query_5a.json'