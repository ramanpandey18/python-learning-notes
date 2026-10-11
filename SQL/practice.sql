SELECT salary
FROM (
    SELECT salary,
           DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees
) ranked
WHERE rnk = N;


SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET N-1;


SELECT MAX(salary) AS nth_highest_salary
FROM employees
WHERE salary < (
    SELECT MAX(salary)
    FROM employees
    WHERE salary < (
        SELECT MAX(salary)
        FROM employees
    )
);

SELECT name, salary,
  RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk,
  ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn,
  LAG(salary) OVER (ORDER BY salary) AS prev_salary
FROM employees;




