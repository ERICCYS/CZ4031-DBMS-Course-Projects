\t
\a

explain (analyze, costs, verbose, buffers, format json) select part.brand, part.partkey, lineitem.commitdate
from part, lineitem
where lineitem.partkey = part.partkey and lineitem.commitdate > '1997-01-01'
order by lineitem.commitdate desc;

\g './queries/query_3/query_3b.json'