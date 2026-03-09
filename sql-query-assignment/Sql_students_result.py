CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    score INTEGER,
    passed BOOLEAN,
    class INTEGER
); 

INSERT INTO students (id, name, score, passed, class) VALUES
(1, 'Aarav', 92, TRUE, 10),
(2, 'Diya', 76, TRUE, 10),
(3, 'Rohan', 65, FALSE, 9),
(4, 'Meera', 88, TRUE, 10),
(5, 'Kabir', 54, FALSE, 9),
(6, 'Ananya', 95, TRUE, 10),
(7, 'Rahul', 81, TRUE, 9),
(8, 'Sneha', 73, TRUE, 9),
(9, 'Arjun', 84, TRUE, 10),
(10, 'Kavya', 69, FALSE, 9);

Q1
SELECT * FROM students; 
Q2
SELECT name, score FROM students; 
Q3
SELECT * FROM students WHERE score > 80; 
Q4
SELECT * FROM students WHERE score > 80 AND passed = TRUE; 
Q5
SELECT * FROM students WHERE score > 85 OR class = 9; 
Q6
SELECT * FROM students WHERE NOT passed; 
Q7
SELECT DISTINCT class FROM students; 
Q8
SELECT * FROM students ORDER BY score DESC LIMIT 5; 
Q9
SELECT * FROM students ORDER BY class ASC, score DESC; 
Q10
SELECT name, score AS final_score FROM students; 
Q11
SELECT name, score 
FROM students 
WHERE score > 75 
ORDER BY score DESC 
LIMIT 3; 