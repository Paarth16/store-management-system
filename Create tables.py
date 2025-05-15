import pymysql

HOST = "localhost"
USER = "root"
PASSWORD = "1029384756" 

conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD)
cursor = conn.cursor()

# Create the database
cursor.execute("CREATE DATABASE IF NOT EXISTS shop;")
cursor.execute("USE shop;")

# Employee Table
cursor.execute("""
CREATE TABLE `employee` (
   `Emp_ID` int NOT NULL AUTO_INCREMENT,
   `Name` varchar(45) NOT NULL,
   `Mobile_no` bigint DEFAULT NULL,
   `DOB` date NOT NULL,
   `Email` varchar(45) NOT NULL,
   `Address` varchar(100) NOT NULL,
   `Post` varchar(45) NOT NULL,
   `Salary` decimal(10,2) DEFAULT NULL,
   PRIMARY KEY (`Emp_ID`),
   UNIQUE KEY `Email_UNIQUE` (`Email`),
   UNIQUE KEY `Mobile_no_UNIQUE` (`Mobile_no`)
 );
""")

# Customer Table
cursor.execute("""
CREATE TABLE `customer` (
   `Mobile_no` bigint NOT NULL,
   `Name` varchar(45) NOT NULL,
   `DOB` date NOT NULL,
   `Gender` varchar(45) NOT NULL,
   PRIMARY KEY (`Mobile_no`)
 );
""")

# Inventory Table
cursor.execute("""
CREATE TABLE `inventory` (
   `Product_ID` varchar(45) NOT NULL,
   `Name` varchar(45) NOT NULL,
   `Brand` varchar(45) NOT NULL,
   `Category` varchar(45) NOT NULL,
   `Price` float NOT NULL,
   `Quantity` int NOT NULL,
   PRIMARY KEY (`Product_ID`)
 );
""")

# Cart Table
cursor.execute("""
CREATE TABLE `cart` (
   `Cart_no` int NOT NULL,
   `Product_ID` varchar(45) NOT NULL,
   `Name` varchar(45) NOT NULL,
   `Brand` varchar(45) NOT NULL,
   `Category` varchar(45) NOT NULL,
   `Price` float NOT NULL,
   `Quantity` int NOT NULL
 );
""")

# Receipt Table
cursor.execute("""
CREATE TABLE `receipt` (
   `Receipt_no` int NOT NULL AUTO_INCREMENT,
   `Emp_ID` int NOT NULL,
   `Date_time` datetime NOT NULL,
   `CMobile_no` bigint DEFAULT NULL,
   `CName` varchar(45) NOT NULL,
   `Cart_no` int NOT NULL,
   `Total` float NOT NULL,
   PRIMARY KEY (`Receipt_no`),
   KEY `Emp_ID_idx` (`Emp_ID`),
   KEY `Customer_idx` (`CMobile_no`,`CName`),
   KEY `Cart_idx` (`Cart_no`)
 );
""")

print("Database and tables created successfully!")

conn.commit()
cursor.close()
conn.close()