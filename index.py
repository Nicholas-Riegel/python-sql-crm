import psycopg2

connection = psycopg2.connect(database="crm_python")

cursor = connection.cursor()

print("Welcome to our CRM")
answer = input("What would you like to do? \n1. See all employees. \n2. See all companies.\n3. See one employee. \n4. See one company. \n5. Create new Employee. \n6. Create new company. \n7. Update an employee.  \n8. Update a company. \n9.Delete an Employee. \n10. Delete a Company. \nPlease enter 1, 2, 3, 4, 5, 6, 7, 8, 9, or 10.\n")


if answer == '1':
    # read all employees
    cursor.execute("SELECT employees.name AS name, age, companies.name AS company FROM employees JOIN companies ON employees.company_id = companies.id")
    response = cursor.fetchall()
    for employee in response:
        name, age, company = employee
        print(f"Name: {name}, Age: {age}, Company: {company}")
        # print(*employee)

elif answer == '2':
    # read all companies
    cursor.execute("SELECT name FROM companies")
    response = cursor.fetchall()
    for companyName in response:
        print(f"Company: {companyName[0]}")

elif answer == '3':
    # read one employee
    answer2 = input("Please enter employee's name.")
    cursor.execute("SELECT employees.name AS name, age, companies.name AS company FROM employees LEFT JOIN companies ON employees.company_id = companies.id WHERE employees.name = %s", [answer2])
    response = cursor.fetchall()

    if response:
        for employee in response:
            name, age, company = employee
            print(f"Name: {name}, Age: {age}, Company: {company}")
    else:
        print("Employee not found.")

elif answer == '4':
    # read one company    
    answer = input("Please enter company's name.")
    cursor.execute("SELECT name FROM companies WHERE name = %s", [answer])
    response = cursor.fetchall()
    if response:
        for company in response:
            name = company[0]
            print(f"Company: {name}")
    else:
        print("Company not found.")

elif answer == '5':
    # create one employee
    name = input("Please enter employee's name.")
    age = input("Please enter employee's age.")
    company = input("Please enter employee's company.")
   
    cursor.execute("SELECT id FROM companies WHERE name = %s", [company])
    companyId = cursor.fetchone()
    
    if companyId:
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

elif answer == '6':
    # create one company
    name = input("Please enter company's name.")
    cursor.execute("INSERT INTO companies (name) VALUES (%s)", [name])
    connection.commit()
    print("Company created.")

elif answer == '7':
    # update one employee
    name = input("Please enter employee's name.")
    cursor.execute("SELECT * FROM employees WHERE name = %s", [name])
    employee = cursor.fetchone()
    if employee:
        id, name, age, companyId = employee
        
        company = ''
        
        if companyId:
            cursor.execute("SELECT name FROM companies WHERE id = %s", [companyId])
            company = cursor.fetchone()[0]
            print(f"Name: {name}, Age: {age}, Company: {company}")
        else:
            print(f"Name: {name}, Age: {age} Company: None")
        
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

elif answer == '8':
    # update one company
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

elif answer == '9':
    # delete one employee
    name = input("Please enter employee's name.")
    cursor.execute("DELETE FROM employees WHERE name = %s", [name])
    connection.commit()
    print("Employee deleted.")

elif answer == '10':
    # delete one company
    name = input("Please enter company's name.")
    cursor.execute("SELECT id FROM companies WHERE name = %s", [name])
    companyId = cursor.fetchone()
    if companyId:
        cursor.execute('UPDATE employees SET company_id = NULL WHERE company_id = %s', [companyId])
        connection.commit()
    cursor.execute("DELETE FROM companies WHERE name = %s", [name])
    connection.commit()
    print("Company deleted.")

cursor.close()
connection.close()