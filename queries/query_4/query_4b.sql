\t
\a

explain(format json) select count(*) as brand_sold, part.brand from part, lineitem where lineitem.partkey = part.partkey and lineitem.commitdate > '1997-01-01' group by part.brand order by brand_sold desc;

\g '/Users/eric/Desktop/Data/query_4/query_4b.json'

-- select * from lineitem where lineitem.commitdate > '1997-01-01' limit 10;