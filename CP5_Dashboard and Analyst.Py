# The data analysis plan includes two important components, first is to explore average salary information by
# different variables, the second component involves looking at how salary varies by variables of interest given
# a specific job title. These tasks will be accomplished based on the establishment of a number of views so that
# analysts can appraoch requests more efficiently.

# After the ETL process when all tables have been loaded to SQL, data analysts will be using Python to interact
# with database system for data analysis purposes.
# The data analysis plan includes two important components, first we aim to look at average salary information
# by different variables, such as job title in particular, which is of greatest interest of our clients.
# We then plan on taking a deep dive into each specific job title to see how salary varies by other variables
# such as company, location, education, experience, etc., to provide a 360 view of salary information for our
# clients depending on a specific job title. These tasks will be accomplished based on the establishment of a
# number of views so that analysts can appraoch requests more efficiently.
# Below are examples of codes for data analysis after the ETL process.

# Importing necessary packages and re-establish connection

import pandas as pd
from sqlalchemy import create_engine

# Pass the connection string to a variable, conn_url
conn_url = 'postgresql://("USERNAME"):("PASSWORD")@localhost/("DATABASE")'

# Create an engine that connects to PostgreSQL server
engine = create_engine(conn_url)

# Establish a connection
connection = engine.connect()

## Create Analyst Username and Password with Privleges

stmt = """

CREATE GROUP analyst_read_only;

CREATE USER analyst1 WITH
    IN GROUP analyst_read_only
	VALID UNTIL '2025-04-03T11:50:38+05:30'
	PASSWORD '123456';

GRANT SELECT ON
    COMPANY, EDUCATION, EMPLOYEE, EMPLOYEE_COMPANY, EMPLOYEE_DEMOGRAPHICS,
    EMPLOYEE_LEVEL, EMPLOYEE_QUALIFICATION, EMPLOYEE_SPECIALIZATION, EMPLOYEE_TITLE,
    GENDER, LEVEL, LOCATION, OTHER, RACE, SPECIALIZATION, TITLE
    TO ANALYST1;

CREATE USER analyst2 WITH
    SUPERUSER
    CREATEDB
    VALID UNTIL '2025-04-03T11:50:38+05:30'
	PASSWORD '111';


"""

connection.execute(stmt)

## Below are the codes that we run for the analyses that are also visualized in dashboard

#### #1 Average salary by company

# Pass the SQL statement to filter data

stmt = """

select avg(totalyearlycompensation)as Avg_salary,company
from employee,employee_company,company
where employee.employee_id = employee_company.employee_id and company.company_id = employee_company.company_id
group by company
order by Avg_salary DESC;

"""

# Execute the statement and get the results
results = connection.execute(stmt).fetchall()

# Extract column names
column_names = results[0].keys()

# Store results in a new dataframe
temp_df = pd.DataFrame(results, columns=column_names)

# Show results
temp_df

#### 1.1 Function to get Average salary for company

# Pass the SQL statement to filter data

stmt = """
create or replace function avg_salary_company(state varchar(100))
    returns table (
        company varchar(100),
        avg_salary numeric(10,2)) as
    $$
        begin
            return query
            select distinct co.company, avg(em.totalyearlycompensation) as avg_salary
            from employee em
            join employee_company ec on ec.employee_id = em.employee_id
            join company co on ec.company_id = co.company_id
            group by co.company;
        end
    $$
language plpgsql;

select * from avg_salary_company('Amazon');

"""


# Execute the statement and get the results
results = connection.execute(stmt).fetchall()

# Extract column names
column_names = results[0].keys()

# Store results in a new dataframe
temp_df = pd.DataFrame(results, columns=column_names)

# Show results
temp_df

#### #2 Average salary by job title

# Pass the SQL statement to filter data
stmt = """

select avg(totalyearlycompensation)as Avg_salary,title
from employee,employee_title,title
where employee.employee_id = employee_title.employee_id and title.title_id = employee_title.title_id
group by title
order by Avg_salary DESC;


"""

# Execute the statement and get the results
results1 = connection.execute(stmt).fetchall()

# Extract column names
column_names = results1[0].keys()

# Store results in a new dataframe
temp_df1 = pd.DataFrame(results1, columns=column_names)

# Show results
temp_df1

#### 2.1 Function to get Average salary for job title

# Pass the SQL statement to filter data
stmt = """
create or replace function avg_salary_title(state varchar(100))
    returns table (
        title varchar(100),
        avg_salary numeric(10,2)) as
    $$
        begin
            return query
            select distinct ti.title, avg(em.totalyearlycompensation) as avg_salary
            from employee em
            join employee_title et on em.employee_id = et.employee_id
            join title ti on et.title_id = ti.title_id
            group by ti.title;
        end
    $$
language plpgsql;

select * from avg_salary_title('Product Manager');

"""

# Execute the statement and get the results
results1 = connection.execute(stmt).fetchall()

# Extract column names
column_names = results1[0].keys()

# Store results in a new dataframe
temp_df1 = pd.DataFrame(results1, columns=column_names)

# Show results
temp_df1

#### #3 Average salary by state

# Pass the SQL statement to filter data
stmt = """

select avg(totalyearlycompensation)as Avg_salary,location_state
from employee,employee_company,location
where employee.employee_id = employee_company.employee_id and location.location_id = employee_company.location_id
group by location_state
order by Avg_salary DESC;


"""

# Execute the statement and get the results
results2 = connection.execute(stmt).fetchall()

# Extract column names
column_names = results2[0].keys()

# Store results in a new dataframe
temp_df2 = pd.DataFrame(results2, columns=column_names)

# Show results
temp_df2

#### 3.1 Function to get Average salary for a state

# Pass the SQL statement to filter data
stmt = """
create or replace function avg_salary_state(state varchar(100))
    returns table (
        location_name varchar(100),
        avg_salary numeric(10,2)) as
    $$
        begin
            return query
            select distinct lo.location_state, avg(em.totalyearlycompensation) as avg_salary
            from location lo
            join employee_company ec on lo.location_id = ec.location_id
            join employee em on em.employee_id = ec.employee_id
            group by lo.location_state;
        end
    $$
language plpgsql;


select * from avg_salary_state('CA');
"""

# Execute the statement and get the results
results2 = connection.execute(stmt).fetchall()


# Extract column names
column_names = results2[0].keys()

# Store results in a new dataframe
temp_df2 = pd.DataFrame(results2, columns=column_names)

# Show results
temp_df2

#### #4 Average salary by years of experience

# Pass the SQL statement to filter data
stmt = """

select avg(totalyearlycompensation)as Avg_salary, years_experience
from employee join employee_qualification using (employee_id)
group by years_experience
order by Avg_salary DESC;


"""

# Execute the statement and get the results
results3 = connection.execute(stmt).fetchall()

# Extract column names
column_names = results3[0].keys()

# Store results in a new dataframe
temp_df3 = pd.DataFrame(results3, columns=column_names)

# Show results
temp_df3

#### #5 Average salary by degree

# Pass the SQL statement to filter data
stmt = """

select avg(totalyearlycompensation)as Avg_salary, education
from employee join employee_qualification using (employee_id)
join education using (education_id)
group by education
order by Avg_salary DESC;


"""

# Execute the statement and get the results
results4 = connection.execute(stmt).fetchall()

# Extract column names
column_names = results4[0].keys()

# Store results in a new dataframe
temp_df4 = pd.DataFrame(results4, columns=column_names)

# Show results
temp_df4

#### #6 Average salary by gender

# Pass the SQL statement to filter data
stmt = """

select avg(totalyearlycompensation)as Avg_salary, gender
from employee join employee_demographics using (employee_id)
group by gender
order by Avg_salary DESC;


"""

# Execute the statement and get the results
results5 = connection.execute(stmt).fetchall()

# Extract column names
column_names = results5[0].keys()

# Store results in a new dataframe
temp_df5 = pd.DataFrame(results5, columns=column_names)

# Show results
temp_df5

#### #7 Average salary by race

# Pass the SQL statement to filter data
stmt = """

select avg(totalyearlycompensation)as Avg_salary, race
from employee join employee_demographics using (employee_id)
group by race
order by Avg_salary DESC;


"""

# Execute the statement and get the results
results6 = connection.execute(stmt).fetchall()

# Extract column names
column_names = results6[0].keys()

# Store results in a new dataframe
temp_df6 = pd.DataFrame(results6, columns=column_names)

# Show results
temp_df6
