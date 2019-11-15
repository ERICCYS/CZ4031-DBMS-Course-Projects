---Nest loop inner join
\t
\a

explain (analyze, costs, verbose, buffers, format json) select *
from (SELECT supplier.nationkey,supplier.suppkey FROM supplier  WHERE 200>suppkey ORDER BY supplier.nationkey) AS a
join (SELECT nation.nationkey, nation.regionkey FROM nation ORDER BY nation.nationkey) As b
on a.nationkey = b.nationkey

\g './queries/query_7/query_7c.json'