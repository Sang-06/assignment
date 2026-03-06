SQL Theory Assigment 
1. why database are important in real-world AI systems
Databases are essential in AI systems because they store large amounts of structured and organized data. AI models require data to learn patterns, make predictions, and generate insights.

For example:
- User information in an e-commerce website
- Product details and prices
- Customer orders and transactions
- Sensor data in smart devices

If this data is not stored in an organized way, AI systems cannot easily access or analyze it. Structured storage allows fast searching, filtering, and processing of data which improves the performance of AI applications.

Example:
A recommendation system in an online shopping platform stores:
- User data
- Purchase history
- Product catalog

This structured data helps the AI suggest relevant products.

---

## 2. Relational database mental model

A relational database stores data in tables.

Each table consists of:

- **Rows** – represent individual records
- **Columns** – represent attributes or properties of the data

Example table: Users

| user_id | name | email |
|--------|------|------|
| 1 | Rahul | rahul@email.com |
| 2 | Priya | priya@email.com |

In this table:
- Each **row** represents one user
- Each **column** represents a property like name or email

Each table should represent **one single entity**.  
For example:
- Users table → stores user information
- Orders table → stores order details
- Products table → stores product information

This keeps the database organized and avoids duplication.

---

## 3. Primary Key

A **Primary Key** is a column that uniquely identifies each record in a table.

Characteristics of a primary key:
- Must be **unique**
- Cannot contain **NULL values**

Example:

| user_id | name |
|--------|------|
| 1 | Rahul |
| 2 | Priya |

Here **user_id** is the primary key.

Why primary keys are important:
- They prevent duplicate records
- They allow databases to quickly locate specific records
- They help connect tables with relationships

---

## 4. Database Schema

A **Database Schema** defines the structure of the database.

It describes:
- Tables
- Columns
- Data types
- Primary keys
- Relationships between tables

Example schema for a Users table:

Users Table
- user_id (Primary Key)
- name (VARCHAR)
- email (VARCHAR)

Schemas are important because they ensure:
- Consistent data structure
- Organized database design
- Easy understanding for developers and systems

---

## 5. Relationships between tables

In relational databases, tables are connected using **foreign keys**.

A **Foreign Key** is a column in one table that references the primary key in another table.

Example:

Users table

| user_id | name |
|--------|------|
| 1 | Rahul |
| 2 | Priya |

Orders table

| order_id | user_id | product |
|---------|--------|---------|
| 101 | 1 | Laptop |
| 102 | 2 | Phone |

Here:
- **user_id** in the Orders table is a **foreign key**
- It connects orders to the user who placed them