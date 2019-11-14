\t
\a

explain (analyze, costs, verbose, buffers, format json) select count(*) as brand_sold, part.brand from part, lineitem where lineitem.partkey = part.partkey and lineitem.commitdate > '1997-01-01' group by part.brand order by brand_sold desc;

\g './queries/query_4/query_4b.json'