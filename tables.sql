CREATE TABLE companies(
	id SERIAL PRIMARY KEY,
	name VARCHAR(20)  NOT NULL
);

CREATE TABLE employees(
	id SERIAL PRIMARY KEY,
	name VARCHAR(20),
    age INT,
	company_id INT REFERENCES companies(id)
);