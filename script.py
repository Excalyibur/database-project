import mysql.connector
import csv

# insert into mysql

# mysql connection configuration (need change)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="2008",
    port="3306"
)

# Create a cursor object
cursor = mydb.cursor()

def insert_user():
    counter = 0
    filename = "datasets\\amazon - USER.csv"

    with open(filename, "r", encoding='utf-8', errors='replace') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            query = "INSERT INTO user (userid, username) VALUES (%s, %s)"
            values = (row[0], row[1])
            cursor.execute(query, values)

        # Commit the changes to the database
        mydb.commit()
        print(counter)

    cursor.close()
    mydb.close()

# insert_user()

def insert_review():
    counter = 0
    filename = "datasets\\amazon - REVIEW.csv"

    with open(filename, "r", encoding='utf-8', errors='replace') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            query = "INSERT INTO review (reviewid, review) VALUES (%s, %s)"
            values = (row[0], row[1])
            cursor.execute(query, values)

        # Commit the changes to the database
        mydb.commit()
        print(counter)

    cursor.close()
    mydb.close()

# insert_review()

def insert_written_by():
    counter = 0
    filename = "datasets\\amazon - WRITTEN_BY.csv"

    with open(filename, "r", encoding='utf-8', errors='replace') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            query = "INSERT INTO written_by (userid, reviewid) VALUES (%s, %s)"
            values = (row[0], row[1])
            cursor.execute(query, values)

        # Commit the changes to the database
        mydb.commit()
        print(counter)

    cursor.close()
    mydb.close()

# insert_written_by()

def insert_category():
    counter = 0
    filename = "datasets\\amazon - CATEGORY.csv"

    with open(filename, "r", encoding='utf-8', errors='replace') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            query = "INSERT INTO category (categoryid, category_name) VALUES (%s, %s)"
            values = (row[0], row[1])
            cursor.execute(query, values)

        # Commit the changes to the database
        mydb.commit()
        print(counter)

    cursor.close()
    mydb.close()

# insert_category()

def insert_product():
    counter = 0
    filename = "datasets\\amazon - PRODUCT.csv"

    with open(filename, "r", encoding='utf-8', errors='replace') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            query = "INSERT INTO product (productid, product_name, actual_price, discount_percentage, product_desc, img_link, product_link, rating_count, rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[8], row[7])
            if counter == 742:
                print(row[2])
            cursor.execute(query, values)
            print(counter)
            counter+=1

        # Commit the changes to the database
        mydb.commit()
        print(counter)

    cursor.close()
    mydb.close()

def insert_is_category():
    counter = 0
    filename = "datasets\\amazon - IS_CATEGORY.csv"

    with open(filename, "r", encoding='utf-8', errors='replace') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            query = "INSERT INTO is_category (productid, categoryid) VALUES (%s, %s)"
            values = (row[0], row[1])
            cursor.execute(query, values)

        # Commit the changes to the database
        mydb.commit()
        print(counter)

    cursor.close()
    mydb.close()

# insert_is_category()

def insert_has_review():
    counter = 0
    filename = "datasets\\amazon - HAS_REVIEW.csv"

    with open(filename, "r", encoding='utf-8', errors='replace') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            query = "INSERT INTO has_review (productid, reviewid) VALUES (%s, %s)"
            values = (row[0], row[1])
            cursor.execute(query, values)

        # Commit the changes to the database
        mydb.commit()
        print(counter)

    cursor.close()
    mydb.close()

# change this function to run the respective functions above
# run the functions one by one from top to bottom to insert the data into the tables created in MySQL Workbench
insert_has_review()