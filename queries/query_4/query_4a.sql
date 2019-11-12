\t
\a

explain(format json) select count(*) as brand_sold, part.brand from part, lineitem where lineitem.partkey = part.partkey group by part.brand order by brand_sold desc;

\g '/Users/eric/Desktop/Data/query_4/query_4a.json'