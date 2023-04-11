use employees;

-- emp no, first name, last name, dept name, latest salary, latest title


SELECT 
    e.emp_no,
    e.first_name,
    e.last_name,
    s.salary,
    t.title
FROM
    employees e
        JOIN
    (SELECT 
        i.emp_no,
            MAX(j.from_date) AS max_date1,
            MAX(k.from_date) AS max_date2
    FROM
        employees i
    JOIN salaries j ON i.emp_no = j.emp_no
    JOIN titles k ON i.emp_no = k.emp_no
    GROUP BY i.emp_no) AS mandate ON mandate.emp_no = e.emp_no
        LEFT JOIN
    salaries s ON s.emp_no = mandate.emp_no
        AND s.from_date = mandate.max_date1
        LEFT JOIN
    titles t ON t.emp_no = mandate.emp_no
        AND t.from_date = mandate.max_date2
GROUP BY e.emp_no
ORDER BY e.emp_no;





