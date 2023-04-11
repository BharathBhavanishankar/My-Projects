-- checking the max number of departments worked by an employee

SELECT 
    emp_no, COUNT(DISTINCT dept_no) AS count_dept
FROM
    dept_emp
GROUP BY emp_no
ORDER BY count_dept DESC
LIMIT 1;

-- selecting one of the two departments that employee has worked using function

drop function if exists emp_dept1;

delimiter $$
create function emp_dept1(empl_no int) returns varchar(25)
deterministic
begin
declare department1 varchar(25);
SELECT 
    (SELECT 
            dept_no
        FROM
            dept_emp
        WHERE
            emp_no = de.emp_no
        GROUP BY dept_no
        ORDER BY dept_no DESC
        LIMIT 1)
INTO department1 FROM
    dept_emp de
WHERE
    de.emp_no = empl_no
GROUP BY de.emp_no;
RETURN department1;
end $$
delimiter ;

-- selecting the other department that employee has worked using function

drop function if exists emp_dept2;

delimiter $$
create function emp_dept2(empl_no int) returns varchar(25)
deterministic
begin
declare department2 varchar(25);
SELECT 
    (SELECT 
            dept_no
        FROM
            dept_emp
        WHERE
            emp_no = de.emp_no
        GROUP BY dept_no
        ORDER BY dept_no ASC
        LIMIT 1)
INTO department2 FROM
    dept_emp de
WHERE
    de.emp_no = empl_no
GROUP BY de.emp_no;
return department2;
end $$
delimiter ;
        
-- getting avg salary of the first department of an employee worked

drop function if exists avg_dalary_dept1;

delimiter $$
create function avg_salary_dept1(empl_no int) returns decimal(10,2)
deterministic
begin
declare salary1 decimal(10,2);
select avg(s.salary) into salary1 from salaries s join dept_emp de on s.emp_no = de.emp_no where s.emp_no = empl_no and de.dept_no = emp_dept1(empl_no);
return salary1;
end $$
delimiter ;

-- getting avg salary of the second department an employee worked

drop function if exists avg_dalary_dept2;

delimiter $$
create function avg_salary_dept2(empl_no int) returns decimal(10,2)
deterministic
begin
declare salary2 decimal(10,2);
select avg(s.salary) into salary2 from salaries s join dept_emp de on s.emp_no = de.emp_no where s.emp_no = empl_no and de.dept_no = emp_dept2(empl_no);
return salary2;
end $$
delimiter ;

-- extracting years of experience in department 1 of an employee

drop function if exists exp_dept1;

delimiter $$
create function exp_dept1(e_num int, d_no varchar(10)) returns decimal(5,2)
deterministic
begin
declare exp_yrs1 decimal(5,2);
SELECT 
    ROUND((CASE
                WHEN
                    YEAR(to_date) = 9999
                THEN
                    TIMESTAMPDIFF(MONTH,
                        from_date,
                        SYSDATE()) / 12
                ELSE TIMESTAMPDIFF(MONTH, from_date, to_date) / 12
            END),
            2)
INTO exp_yrs1 FROM
    dept_emp de
WHERE
    de.emp_no = e_num AND de.dept_no = d_no;
return exp_yrs1;
end $$
delimiter ;

-- extracting years of experience in department 2 of an employee

drop function if exists exp_dept2;

delimiter $$
create function exp_dept2(e_num int, d_no varchar(10)) returns decimal(5,2)
deterministic
begin
declare exp_yrs2 decimal(5,2);
SELECT 
    ROUND((CASE
                WHEN
                    YEAR(to_date) = 9999
                THEN
                    TIMESTAMPDIFF(MONTH,
                        from_date,
                        SYSDATE()) / 12
                ELSE TIMESTAMPDIFF(MONTH, from_date, to_date) / 12
            END),
            2)
INTO exp_yrs2 FROM
    dept_emp de
WHERE
    de.emp_no = e_num AND de.dept_no = d_no;
return exp_yrs2;
end $$
delimiter ;

-- creating stored procedure to have employee number as input, departments employee worked, avg salary received and years of experience in that dept

drop procedure if exists emp_dept_avg_salary;

delimiter $$
create procedure emp_dept_avg_salary(in employee_number int)
begin
 SELECT 
    de.emp_no,
    emp_dept1(employee_number) AS dept1,
    avg_salary_dept1(employee_number) AS avg_dept1_salary,
    exp_dept1(employee_number, emp_dept1(employee_number)) as exp_dept1_yrs,
    (CASE
        WHEN emp_dept1(employee_number) = emp_dept2(employee_number) THEN 0
        ELSE emp_dept2(employee_number)
    END) AS dept2,
    (CASE
        WHEN emp_dept1(employee_number) = emp_dept2(employee_number) THEN 0
        ELSE avg_salary_dept2(employee_number)
    END) as avg_dept2_salary,
    (CASE 
		WHEN emp_dept1(employee_number) = emp_dept2(employee_number) THEN 0
        ELSE exp_dept2(employee_number, emp_dept2(employee_number))end) as exp_dept2_yrs
FROM
    dept_emp de
        JOIN
    salaries s ON s.emp_no = de.emp_no
WHERE
    de.emp_no = employee_number
GROUP BY de.emp_no;  
end $$
delimiter ;

call employees.emp_dept_avg_salary(10040);











