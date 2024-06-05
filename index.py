import psycopg2

connection = psycopg2.connect(database="crm_python")

cursor = connection.cursor()

print("Welcome to our CRM")
answer = input("What would you like to do? \n1. See all employees. \n2. See all companies.\n3. See one employee. \n4. See one company. \n5. Creat new Employee. \n6. Create new company. \n7. Update an employee.  \n8. Update a company. \n9.Delete an Employee. \n10. Delete a Company. \nPlease enter 1, 2, 3, 4, 5, 6, 7, 8, 9, or 10.\n")


# read all employees
if answer == '1':
    cursor.execute("SELECT employees.name AS name, age, companies.name AS company FROM employees JOIN companies ON employees.company_id = companies.id")
    response = cursor.fetchall()
    for employee in response:
        name, age, company = employee
        print(f"Name: {name}, Age: {age}, Company: {company}")
        # print(*employee)

# read all companies
elif answer == '2':
    cursor.execute("SELECT name FROM companies")
    response = cursor.fetchall()
    for company in response:
        name, age, company = employee
        print(f"Company: {name}")
        # print(*company)

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
        # we got RETURNING id from chatGPT. It saves us having to query the db for the id 
        cursor.execute("INSERT INTO companies (name) VALUES (%s) RETURNING id", [company])
        connection.commit()
        
        companyId = cursor.fetchone()[0]
        cursor.execute("INSERT INTO employees (name, age, company_id) VALUES (%s, %s, %s)", [name, age, companyId])
        connection.commit()

    print("Employee created.")

# read one employee
elif answer == '4':
    
    answer2 = input("Please enter employee's name.")

    cursor.execute("SELECT employees.name AS name, age, companies.name AS company FROM employees LEFT JOIN companies ON employees.company_id = companies.id WHERE employees.name = %s", [answer2])

    response = cursor.fetchall()

    if response:
        for employee in response:
            name, age, company = employee
            print(f"Name: {name}, Age: {age}, Company: {company}")
    else:
        print("Employee not found.")

# read one company
elif answer == '5':
    
    answer = input("Please enter company's name.")

    cursor.execute("SELECT name FROM companies WHERE name = %s", [answer])

    response = cursor.fetchall()

    if response:
        for company in response:
            name = company[0]
            print(f"Company: {name}")
    else:
        print("Company not found.")
# create one company
elif answer == '6':
    name = input("Please enter company's name.")
    cursor.execute("INSERT INTO companies (name) VALUES (%s)", [name])
    connection.commit()
    print("Company created.")
# delete one employee
elif answer == '7':
    name = input("Please enter employee's name.")
    cursor.execute("DELETE FROM employees WHERE name = %s", [name])
    connection.commit()
    print("Employee deleted.")
# delete one company
elif answer == '8':
    name = input("Please enter company's name.")
    cursor.execute("DELETE FROM companies WHERE name = %s", [name])
    connection.commit()
    print("Company deleted.")
# update one employee
elif answer == '9':
    name = input("Please enter employee's name.")
    cursor.execute("SELECT * FROM employees WHERE name = %s", [name])
    employee = cursor.fetchone()
    if employee:
        id, name, age, companyId = employee
        
        cursor.execute("SELECT name FROM companies WHERE id = %s", [companyId])
        company = cursor.fetchone()[0]

        print(f"Name: {name}, Age: {age}, Company: {company}")
        newName = input("Please enter new employee's name.")
        newAge = input("Please enter new employee's age.")
        newCompany = input("Please enter new employee's company.")
        if newCompany == company:
            cursor.execute("UPDATE employees SET name = %s, age = %s WHERE id = %s", [newName, newAge, id])
            connection.commit()
            print("Employee updated.")
        else:
            cursor.execute("SELECT id FROM companies WHERE name = %s", [newCompany])
            companyId = cursor.fetchone()
            if companyId:
                cursor.execute("UPDATE employees SET name = %s, age = %s, company_id = %s WHERE id = %s", [newName, newAge, companyId, id])
                connection.commit()
                print("Employee updated.")
            else:
                cursor.execute("INSERT INTO companies (name) VALUES (%s) RETURNING id", [newCompany])
                connection.commit()
                companyId = cursor.fetchone()[0]
                cursor.execute("UPDATE employees SET name = %s, age = %s, company_id = %s WHERE id = %s", [newName, newAge, companyId, id])
                connection.commit()
                print("Employee updated.")
    else:
        print("Employee not found.")
# update one company
elif answer == '10':
    name = input("Please enter company's name.")
    cursor.execute("SELECT * FROM companies WHERE name = %s", [name])
    company = cursor.fetchone()
    if company:
        id, name = company
        print(f"Name: {name}")
        newName = input("Please enter new company's name.")
        cursor.execute("UPDATE companies SET name = %s WHERE id = %s", [newName, id])
        connection.commit()
        print("Company updated.")
    else:
        print("Company not found.")

cursor.close()
connection.close()