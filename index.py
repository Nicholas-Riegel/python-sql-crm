import psycopg2

connection = psycopg2.connect(database="crm_python")

cursor = connection.cursor()

print("Welcome to our CRM")
answer = input("What would you like to do? \n1. See all employees. \n2. See all companies.\n3. Enter new Employee.\nPlease enter 1, 2 or 3.\n")


# read all employees
if answer == '1':
    cursor.execute("SELECT employees.name AS name, age, companies.name AS company FROM employees JOIN companies ON employees.company_id = companies.id")
    response = cursor.fetchall()
    for employee in response:
        print(*employee)

# read all companies
elif answer == '2':
    cursor.execute("SELECT name FROM companies")
    response = cursor.fetchall()
    for company in response:
        print(*company)

# create one employee
elif answer == '3':
    name = input("Please enter employee's name.")
    age = input("Please enter employee's age.")
    company = input("Please enter employee's company.")
   
    cursor.execute("SELECT id FROM companies WHERE name = %s", [company])
    
    if cursor.fetchone():
        companyId = cursor.fetchone()
        cursor.execute("INSERT INTO employees (name, age, company_id) VALUES (%s, %s, %s)", [name, age, companyId])
        connection.commit()
    
    else:
        cursor.execute("INSERT INTO companies (name) VALUES (%s)", [company])
        connection.commit()
        
        cursor.execute("SELECT id FROM companies WHERE name = %s", [company])
        companyId = cursor.fetchone()
        cursor.execute("INSERT INTO employees (name, age, company_id) VALUES (%s, %s, %s)", [name, age, companyId])
        connection.commit()
        
'''
read one employee
read one company
create on company
delete one employee
delete one company
update one employee
update one company
'''

# cursor.execute("INSERT INTO companies (name) VALUES (%s)", ['first_company'])

# cursor.execute("DELETE FROM people WHERE id = %s", [5]);
# connection.commit()

# cursor.execute("UPDATE people SET first_name = %s, age = %s WHERE id = %s", ['Matt', 43, 3])
# connection.commit()

cursor.close()
connection.close()