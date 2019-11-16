\t
\a

explain (analyze, costs, verbose, buffers, format json) select part.brand, part.partkey, lineitem.commitdate
from part, lineitem
where lineitem.partkey = part.partkey and part.partkey >= 150000
order by part.partkey desc;

\g './queries/query_3/query_3a.json'