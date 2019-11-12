\t
\a

explain(format json) select avg(acctbal) as avgbal, nation.name from customer, nation where customer.nationkey = nation.nationkey and nation.nationkey >= 10 group by nation.name order by avgbal desc;

\g '/Users/eric/Desktop/Data/query_1/query_1b.json'