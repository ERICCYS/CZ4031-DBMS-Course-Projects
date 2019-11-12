CREATE DATABASE "tpch_db" WITH OWNER = eric ENCODING = 'UTF8' CONNECTION LIMIT = -1;
\c "tpch_db"

CREATE TABLE public.region (
    regionkey integer, 
    name character varying(100), 
    comment character varying(200), 
    PRIMARY KEY (regionkey)
);

COPY public.region (
    regionkey,
    name, 
    comment
) FROM '/Users/eric/Desktop/Data/region-processed.csv' DELIMITER '|' CSV HEADER;

CREATE TABLE public.part (
    partkey integer, 
    name character varying(200), 
    mfgr character varying(50), 
    brand character varying(50), 
    type character varying(150), 
    size integer, 
    container character varying(150), 
    retailprice float, 
    comment character varying(200), 
    PRIMARY KEY (partkey)
);

COPY public.part (
    partkey, 
    name, 
    mfgr, 
    brand, 
    type, 
    size, 
    container, 
    retailprice, 
    comment
) FROM '/Users/eric/Desktop/Data/part-processed.csv' DELIMITER '|' CSV HEADER;

CREATE TABLE public.nation (
    nationkey integer, 
    name character varying(100), 
    regionkey integer references public.region(regionkey), 
    comment character varying(200), 
    PRIMARY KEY (nationkey)
);

COPY public.nation (
    nationkey, 
    name, 
    regionkey, 
    comment
) FROM '/Users/eric/Desktop/Data/nation-processed.csv' DELIMITER '|' CSV HEADER;

CREATE TABLE public.supplier (
    suppkey integer, 
    name character varying(100), 
    address character varying(250), 
    nationkey integer references public.nation(nationkey), 
    phone character varying(30), 
    acctbal float, 
    comment character varying(200), 
    PRIMARY KEY (suppkey)
);

COPY public.supplier (
    suppkey, 
    name, 
    address, 
    nationkey, 
    phone, 
    acctbal, 
    comment
) FROM '/Users/eric/Desktop/Data/supplier-processed.csv' DELIMITER '|' CSV HEADER;

CREATE TABLE public.partsupp (
    partkey integer references public.part(partkey), 
    suppkey integer references public.supplier(suppkey), 
    availqty integer, 
    supplycost float, 
    comment character varying(200)
);

COPY public.partsupp (
    partkey, 
    suppkey, 
    availqty, 
    supplycost, 
    comment
) FROM '/Users/eric/Desktop/Data/partsupp-processed.csv' DELIMITER '|' CSV HEADER;

CREATE TABLE public.customer (
    custkey integer, 
    name character varying(100), 
    address character varying(250), 
    nationkey integer references public.nation(nationkey), 
    phone character varying(30), 
    acctbal float, 
    mktsegment character varying(100), 
    comment character varying(200), 
    PRIMARY KEY (custkey)
);

COPY public.customer (
    custkey, 
    name, 
    address, 
    nationkey, 
    phone, 
    acctbal, 
    mktsegment, 
    comment
) FROM '/Users/eric/Desktop/Data/customer-processed.csv' DELIMITER '|' CSV HEADER;

CREATE TABLE public.orders (
    orderkey integer, 
    custkey integer references public.customer(custkey),
    orderstatus character varying(1), 
    totalprice float, 
    orderdate date, 
    orderpriority character varying(20), 
    clerk character varying(20), 
    shippriority boolean, 
    comment character varying(200), 
    PRIMARY KEY (orderkey)
);

COPY public.orders (
    orderkey, 
    custkey, 
    orderstatus, 
    totalprice, 
    orderdate, 
    orderpriority, 
    clerk, 
    shippriority, 
    comment
) FROM '/Users/eric/Desktop/Data/orders-processed.csv' DELIMITER '|' CSV HEADER;

CREATE TABLE public.lineitem (
    orderkey integer references public.orders(orderkey), 
    partkey integer references public.part(partkey), 
    suppkey integer references public.supplier(suppkey), 
    linenumber integer, 
    quantity integer, 
    extendedprice float, 
    discount float, 
    tax float, 
    returnflag character varying(1), 
    linestatus character varying(1), 
    shipdate date, 
    commitdate date, 
    receiptdate date, 
    shipinstruct character varying(50), 
    shipmode character varying(30), 
    comment character varying(200)
);

COPY public.lineitem (
    orderkey, 
    partkey, 
    suppkey, 
    linenumber, 
    quantity, 
    extendedprice, 
    discount, 
    tax, 
    returnflag, 
    linestatus, 
    shipdate, 
    commitdate, 
    receiptdate, 
    shipinstruct, 
    shipmode, 
    comment
) FROM '/Users/eric/Desktop/Data/lineitem-processed.csv' DELIMITER '|' CSV HEADER;