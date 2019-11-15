\t
\a

explain (analyze, costs, verbose, buffers, format json) select *
from nation, region
where nation.regionkey = region.regionkey and region.regionkey = 1;

\g './queries/query_5/query_5b.json'