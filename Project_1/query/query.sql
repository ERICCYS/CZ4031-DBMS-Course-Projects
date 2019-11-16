/* Q1 FOR each type of publication, count the total number of publications of that type BETWEEN 2000-
2018. Your query should return a set of (publication-type, count) pairs. FOR example, (article,
20000), (inproceedings, 30000) */

SELECT pubtype, count(*)
FROM publication
WHERE pubyear BETWEEN 2000 AND 2018
GROUP BY pubtype;


/* Q2 Find all the conferences that have ever published mORe than 500 papers in one year. Note that
one conference may be held every year (e.g., KDD runs many years, AND each year the
conference hAS a number of papers)  */

SELECT DISTINCT confname FROM (
    SELECT count(*), SUBSTRING_INDEX(SUBSTRING_INDEX(publication.pubkey, 'conf/', -1), '/', 1) AS confname
    FROM publication
    WHERE pubsubtype ='conf'
    GROUP BY SUBSTRING_INDEX(SUBSTRING_INDEX(publication.pubkey, 'conf/', -1), '/', 1),pubYear 
    HAVING count(*)>500
) AS greater_than;


/* Q3 FOR each 10 consecutive years starting FROM 1970, i.e., [ 1970, 1979 ], [ 1980, 1989 ],…, [2010,
2019], compute the total number of conference publications in DBLP in that 10 years. Hint: fOR
this query you may want to compute a tempORary table with all distinct years */

SELECT (FLOOR(publication.pubYear/10) * 10) AS decade,COUNT(publication.pubId) AS count
FROM publication
WHERE publication.pubYear BETWEEN 1970 AND 2019
AND pubtype = 'inproceedings'
GROUP BY decade
ORDER BY decade ASC;


/*Q4 . Find the most collaborative authors who published in a conference or journal whose name
contains “data” (e.g., ACM SIGKDD International Conference on Knowledge
Discovery and Data Mining). That is, for each author determine its number of
collaborators, and then find the author with the most number of collaborators. Hint: for this
question you may want to compute a temporary table of coauthors. */

-- create table method

CREATE TABLE have_data AS (
SELECT pubid,pubkey
FROM publication
WHERE lower(publication.pubtitle) LIKE '%data%'
AND (publication.pubsubtype = 'conf' OR publication.pubsubtype = 'journals')
);

CREATE TABLE have_data_author AS (
SELECT have_data.pubid,authorship.personFullName
FROM have_data INNER JOIN AUTHORSHIP
ON have_data.pubkey = authorship.pubkey);

CREATE TABLE coauthor AS(
SELECT DISTINCT p1.personfullname AS author,p2.personfullname AS coauthor
FROM have_data_author AS p1 INNER JOIN have_data_author AS p2 ON p1.pubid=p2.pubid
WHERE p1.personfullname<>p2.personfullname);

CREATE TABLE max_coauthor AS (SELECT max(count) AS a FROM (SELECT count(coauthor) AS count FROM coauthor GROUP BY author) AS b);

SELECT author,count(coauthor) AS count
FROM coauthor
GROUP BY author
HAVING count(coauthor) = (SELECT a FROM max_coauthor);

-- nested query


/* Q5 Data analytics AND data science are very popular topics. Find the top 10 authORs with the largest
number of publications that are published in conferences AND journals whose titles contain wORd
“Data” in the lASt 5 years */

SELECT have_data_authOR_Q5.personFullName,count(have_data_authOR_Q5.pubid) AS count
FROM (
    SELECT have_data_Q5.pubid,authORship.personFullName
    FROM (
        SELECT pubid,pubkey
        FROM publication
        WHERE lower(publication.pubtitle) LIKE '%data%'
        AND (publication.pubsubtype = 'conf' OR publication.pubsubtype = 'journals')
        AND publication.pubyear BETWEEN 2015 AND 2019
    ) AS have_data_Q5 INNER JOIN AUTHORSHIP
    ON have_data_Q5.pubkey = authORship.pubkey
) AS have_data_authOR_Q5
GROUP BY have_data_authOR_Q5.personFullName
ORDER BY count(have_data_authOR_Q5.pubid) DESC
LIMIT 10;


/* Q6 List the name of the conferences such that it hAS ever been held in June, AND the cORresponding proceedings 
(in  the  year  WHERE  the  conferencewAS  held  in  June)  contain  mORe  than  100
publications */

SELECT DISTINCT pro_100.conference
FROM (
    SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(inprocrossref, 'conf/', -1), '/', 1) AS conference,inprocrossref 
    FROM (
        SELECT inprocrossref,COUNT(*) AS count
        FROM inproceeding
        GROUP BY inprocrossref
        HAVING COUNT(*) > 100
    ) AS count_100
) AS pro_100, (   
    SELECT DISTINCT SUBSTRING_INDEX(SUBSTRING_INDEX(pubKey, 'conf/', -1), '/', 1
) AS conference
FROM publication
WHERE lower(pubtitle) LIKE '%june%') AS conf
WHERE pro_100.conference = conf.conference;


/* Q7a Find authORs who have published at leASt 1 paper every year in the lASt 30 years, AND whose
family name start with ‘H’ */

SELECT authOR_wanted.personFullName
FROM 
(
    SELECT authORship.personfullname,thirtyyear_pub.pubyear
    FROM authORship, 
    (
        SELECT publication.pubkey,publication.pubyear
        FROM publication 
        WHERE pubyear BETWEEN 1990 AND 2019
    ) AS thirtyyear_pub 
    WHERE authORship.pubkey = thirtyyear_pub.pubkey
) AS authOR_wanted
WHERE substring_index(authOR_wanted.personfullname,' ',-1) LIKE 'H%'
GROUP BY authOR_wanted.personfullname
HAVING count(DISTINCT authOR_wanted.pubyear) = 30;


/* Q7b Find the names AND number of publications fOR authORs who have
the earliest publication recORd in DBLP */

SELECT author.personFullName, COUNT(authorship.pubkey)
FROM authorship, (
 SELECT distinct A.personFullName
 FROM authorship AS A, publication AS P
 WHERE A.pubkey = P.pubkey
 AND P.pubyear = (SELECT MIN(pubyear) FROM publication where not publication.pubyear = 0)
) AS author
where authorship.personFullName = author.personfullname
GROUP BY author.personFullName;

/* Q8 Find number of proceedings that have been posted on top 10 data conferences. 
Top 10 data conferences refers to conferences that have top 10 largest number of proceeding which titile contains "data" after 2010 */

SELECT count(d3.pubkey) 
FROM (
    SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(d2.pubKey, 'conf/', -1), '/', 1) AS conference, pubkey 
    FROM (
        SELECT * 
        FROM publication 
        WHERE pubtype='proceedings'
    ) AS d2
) AS d3,(
    SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(d1.pubKey, 'conf/', -1), '/', 1) AS conference, count(pubid) AS count 
    FROM (
        SELECT pubid,pubkey
        FROM publication
        WHERE lower(publication.pubtitle) LIKE '%data%'
        AND publication.pubyear >2010
        AND publication.pubtype = 'proceedings'
    ) AS d1 
    GROUP BY conference 
    ORDER BY count DESC 
    LIMIT 10
) AS d4 
WHERE d3.conference = d4.conference;
