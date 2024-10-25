--Create score table
CREATE TABLE score (
    id int,
    name varchar(255),
    phone varchar(255),
    county varchar(255), 
    email varchar(255), 
    score int);

SELECT id, name, score,
CASE 
    WHEN score >= 95 AND score <=100 THEN 'A'
    WHEN score >= 90 AND score <95 THEN 'A-'
    WHEN score >= 85 AND score <90 THEN 'B+'
    WHEN score >= 80 AND score <85 THEN 'B'
    WHEN score >= 75 AND score <80 THEN 'B-'
    WHEN score >= 70 AND score <75 THEN 'C+'
    WHEN score >= 65 AND score <70 THEN 'C'
    WHEN score >= 60 AND score <65 THEN 'C-'
    WHEN score >= 55 AND score <60 THEN 'D+'
    WHEN score >= 50 AND score <55 THEN 'D'
ELSE
    'FAIL'
END AS grade
FROM score;
