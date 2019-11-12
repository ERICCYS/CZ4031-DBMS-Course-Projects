select avg(acctbal) as avgbal, nation.name from customer, nation where customer.nationkey = nation.nationkey  group by nation.name order by avgbal desc;

select sum(totalprice) as spend, nation.name from customer, nation, orders where customer.custkey = orders.custkey and customer.nationkey = nation.nationkey group by nation.name order by spend desc;

select count(*) as customer_count, region.name from customer, nation, region where customer.nationkey = nation.nationkey and nation.regionkey = region.regionkey group by region.name order by customer_count desc;

select count(*) as brand_sold, part.brand from part, lineitem where lineitem.partkey = part.partkey group by part.brand order by brand_sold desc limit 10;

select distinct partsupp.partkey from part, partsupp where partsupp.partkey = part.partkey and partsupp.availqty < 3;

select count(*) as supplier_count, region.name from supplier, nation, region where supplier.nationkey = nation.nationkey and nation.regionkey = region.regionkey group by region.name order by supplier_count desc;

