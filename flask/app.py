from flask import Flask, request, redirect, url_for, render_template
from flask_mysqldb import MySQL
import sys
sys.path.append("/config/")
from config import configsql as config
import time
from flask import send_file
import mysql.connector
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import io
import base64
import pandas as pd
import re

app = Flask(__name__)
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB
app.config['MYSQL_PORT'] = config.MYSQL_PORT
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/createproduct', methods=['GET', 'POST'])
def create_product():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT categoryid, category_name FROM category")
    data = cur.fetchall()
    if request.method == 'POST':
        # Retrieve form data
        productid = request.form['productid']
        product_name = request.form['product_name']
        actual_price = request.form['actual_price']
        discount_percentage = request.form['discount_percentage']
        product_desc = request.form['product_desc']
        img_link = request.form['img_link']
        product_link = request.form['product_link']
        rating_count = request.form['rating_count']
        rating = request.form['rating']
        categorychoice = request.form['categorychoice']

        print("cc: ", categorychoice)

        # Insert new product into database
        cur.execute("INSERT INTO product VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (productid, product_name, actual_price, discount_percentage, product_desc, img_link, product_link, rating_count, rating))
        conn.commit()
        cur.execute("INSERT INTO is_category VALUES (%s, %s)", (productid, categorychoice))
        conn.commit()
    return render_template('create/createproduct.html', data=data)

@app.route('/createreview', methods=['GET', 'POST'])
def create_review():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT productid FROM product")
    data = cur.fetchall()
    cur.execute("SELECT userid, username FROM user")
    data2 = cur.fetchall()
    if request.method == 'POST':
        # Retrieve form data
        reviewid = request.form['reviewid']
        review = request.form['review']
        userchoice = request.form['userchoice']
        productchoice = request.form['productchoice']

        # Insert new product into database
        cur.execute("INSERT INTO review VALUES (%s, %s)", (reviewid, review))
        conn.commit()

        print("pc: ", productchoice)
        
        cur.execute("INSERT INTO has_review VALUES (%s, %s)", (productchoice, reviewid))
        conn.commit()

        print("uc: ", userchoice)

        cur.execute("INSERT INTO written_by VALUES (%s, %s)", (userchoice, reviewid))
        conn.commit()
    return render_template('create/createreview.html', data=data, data2=data2)

@app.route('/createuser', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        userid = request.form['userid']
        username = request.form['username']

        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("INSERT INTO user (userid, username) VALUES (%s, %s)", (userid, username))
        conn.commit()
        cur.close()
    return render_template('create/createuser.html')

@app.route('/createcategory', methods=['GET', 'POST'])
def create_category():
    if request.method == 'POST':
        categoryid = request.form['categoryid']
        category_name = request.form['category_name']

        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("INSERT INTO category (categoryid, category_name) VALUES (%s, %s)", (categoryid, category_name))
        conn.commit()
        cur.close()
    return render_template('create/createcategory.html')

@app.route('/dashboard')
def dashboard():
    conn = mysql.connection
    cur = conn.cursor()
    
    # 4 Top Cards

    # Total number of products
    dash1 = "SELECT count(productid) FROM product;"
    cur.execute(dash1)
    conn.commit()
    data1=cur.fetchone()[0]

    # Total number of category
    dash2 = "SELECT count(categoryid) FROM category;"
    cur.execute(dash2)
    conn.commit()
    data2=cur.fetchone()[0]

    # Average rating
    dash3 = "SELECT ROUND(AVG(rating), 1) FROM product;"
    cur.execute(dash3)
    conn.commit()
    data3=cur.fetchone()[0]

    # Average discount percentage
    dash4 = "SELECT ROUND(AVG(discount_percentage), 2) FROM product;"
    cur.execute(dash4)
    conn.commit()
    data4=cur.fetchone()[0]

    # Tables

    # Top 10 highest discount products
    tabledash1 = "SELECT product_name, ROUND(((100-discount_percentage) * actual_price), 2) as 'discount_price', discount_percentage FROM product ORDER BY  discount_percentage DESC LIMIT 10;"
    cur.execute(tabledash1)
    conn.commit()
    tabledata1=cur.fetchall()

    # Top 10 highest rating products
    tabledash2 = "SELECT product_name, rating FROM product ORDER BY rating DESC LIMIT 10;"
    cur.execute(tabledash2)
    conn.commit()
    tabledata2=cur.fetchall()

    # Product recommendations
    tabledash3 = '''
    SELECT product_name, category_name, rating, rating_count
    FROM product
    LEFT JOIN is_category
    ON is_category.productid = product.productid
    LEFT JOIN category
    ON category.categoryid = is_category.categoryid
    GROUP BY product_name
    ORDER BY rating DESC
    LIMIT 10;
    '''
    cur.execute(tabledash3)
    conn.commit()
    tabledata3=cur.fetchall()

    # Graphs

    # Top 10 product category pie chart
    cur.execute("SELECT count(productid), category_name FROM is_category LEFT JOIN category ON is_category.categoryid = category.categoryid GROUP BY is_category.categoryid ORDER BY count(productid) DESC LIMIT 10;")
    data = cur.fetchall()
 
    NoOfProducts = []
    CategoryLabels = []
 
    for i in data:
        NoOfProducts.append(i[0])
        CategoryLabels.append(i[1])
     
    print("No of Products = ", NoOfProducts)
    print("Category Name = ", CategoryLabels)
 
    # Visualizing Data using Matplotlib
    fig = plt.figure(figsize =(10, 7))
    plt.pie(NoOfProducts, labels = CategoryLabels)
    plt.title("Top 10 Product Category")

    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', transparent=True)
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    plt.close(fig)

    # Product ratings bar chart

    # define the SQL statements
    sql_statements = [
        "SELECT count(rating) FROM product WHERE rating <= 3.0;",
        "SELECT count(rating) FROM product WHERE rating >= 3.0 AND rating <= 3.5;",
        "SELECT count(rating) FROM product WHERE rating >= 3.5 AND rating <= 4.0;",
        "SELECT count(rating) FROM product WHERE rating >= 4.0 AND rating <= 4.5;",
        "SELECT count(rating) FROM product WHERE rating >= 4.5 AND rating <= 5.0;"
    ]

    # execute the SQL statements and store the results in a list
    results = []
    for statement in sql_statements:
        cur.execute(statement)
        conn.commit()
        result = cur.fetchone()[0]
        results.append(result)

    # plot the bar chart
    x_labels = ["<=3.0", "3.0-3.5", "3.5-4.0", "4.0-4.5", "4.5-5.0"]
    fig2 = plt.figure(figsize =(10, 7))
    plt.bar(x_labels, results)
    plt.xlabel("Rating")
    plt.ylabel("Count")
    plt.title("Product Ratings Barchart")
    # plt.show()

    buffer = io.BytesIO()
    fig2.savefig(buffer, format='png', transparent=True)
    buffer.seek(0)
    img_str2 = base64.b64encode(buffer.getvalue()).decode()
    plt.close(fig2)

    return render_template('dashboard.html', img_data=img_str, img_data2=img_str2, data1=data1, data2=data2, data3=data3, data4=data4, tabledata1=tabledata1, tabledata2=tabledata2, tabledata3=tabledata3)

# Search for products by product keyword

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        input = request.form['searchres']
        if not input:
            print("null")
            return redirect('/')
        query = "SELECT productid, product_name, product_desc, img_link, product_link FROM product WHERE product_name LIKE '%" + input + "%';"
        conn = mysql.connection
        start =  time.time()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        elapse = time.time() - start
        string = "You are currently viewing products with keyword: '"+ input + "'"
        headers = [i[0] for i in cur.description]
        data = cur.fetchall()
        string2 = "{} results in {timer:.3f}s".format(len(data), timer=elapse)
        for i in headers:
            print(i)
        for i in data:
            print(i)
        return render_template('searchres/productres.html', data=data, headers=headers, string=string, string2=string2)
    return render_template('index.html')

# Search for product by category name

@app.route('/category/search', methods=['GET', 'POST'])
def searchcat():
    if request.method == "POST":
        input = request.form['searchres']
        if not input:
            print("null")
            return redirect('/category')
        query = "SELECT is_category.productid, product_name, img_link, category_name, product_link, category.categoryid FROM product LEFT JOIN is_category ON product.productid = is_category.productid RIGHT JOIN category ON is_category.categoryid = category.categoryid WHERE category_name LIKE '%" + input + "%'"
        conn = mysql.connection
        start = time.time()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        elapse = time.time() - start
        string = "You are currently viewing products in category: '"+ input + "'"
        headers = [i[0] for i in cur.description]
        data = cur.fetchall()
        string2 = "{} results in {timer:.3f}s".format(len(data), timer=elapse)
        print(string2)
        return render_template('searchres/categoryres.html', data=data, headers=headers, string=string, string2=string2)
    return render_template('index.html')

# Search for products by review keyword

@app.route('/review/search', methods=['GET', 'POST'])
def searchreview():
    if request.method == "POST":
        input = request.form['searchres']
        if not input:
            print("null")
            return redirect('/review')
        query = "SELECT has_review.productid, product_name, img_link, review, username, review.reviewid FROM product LEFT JOIN has_review ON product.productid = has_review.productid RIGHT JOIN review ON has_review.reviewid = review.reviewid LEFT JOIN written_by ON review.reviewid = written_by.reviewid RIGHT JOIN user ON written_by.userid = user.userid WHERE review LIKE '%" + input + "%'"
        conn = mysql.connection
        start = time.time()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        elapse = time.time() - start
        string = "You are currently viewing reviews that has: '"+ input + "'"
        headers = [i[0] for i in cur.description]
        data = cur.fetchall()
        string2 = "{} results in {timer:.3f}s".format(len(data), timer=elapse)
        print(string2)
        return render_template('searchres/reviewres.html', data=data, headers=headers, string=string, string2=string2)
    return render_template('index.html')

# Search for products by a range of ratings

@app.route('/ratings/search', methods=['GET', 'POST'])
def searchrating():
    if request.method == "POST":
        input = request.form['searchres']
        if not input:
            print("null")
            return redirect('/ratings/search')
        
        if re.search(r'=<|=>', input):
            return redirect('/ratings/search')
        
        if not re.search(r'[<>]=?|=', input):
            input = "=" + input
        query = "SELECT productid, product_name, img_link, product_link, rating FROM product WHERE rating " + input #= CAST('" + input + "' AS FLOAT)"
        conn = mysql.connection
        start = time.time()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        elapse = time.time() - start
        string = "You are currently viewing products that has ratings: '"+ input + "'"
        headers = [i[0] for i in cur.description]
        data = cur.fetchall()
        string2 = "{} results in {timer:.3f}s".format(len(data), timer=elapse)
        print(string2)
        return render_template('searchres/ratingsres.html', data=data, headers=headers, string=string, string2=string2)
    return render_template('index.html')

# Delete product (in product search result table)

@app.route('/product/delete', methods=['GET', 'POST'])
def deleteProductId():
    if request.method == "POST":
        input = request.form['productdelete']
        start = time.time()
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("DELETE FROM has_review WHERE productid = \""+ input + "\"")
        cur.execute("DELETE FROM is_category WHERE productid = \""+ input + "\"")
        cur.execute("DELETE FROM product WHERE productid = \""+ input + "\"")
        conn.commit()
        elapse = time.time() - start
        print("Timer for deleting in MySQL: " + str(elapse)+"s")        
    return redirect("/search")

# Edit and update product name and description (in product search result table)

@app.route('/product/update', methods=['GET', 'POST'])
def updateProductId():
    if request.method == "POST":
        id = request.form['id']
        name = request.form['name']
        product_desc = request.form['description']
        start =  time.time()
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("UPDATE product SET product_name = \'" + name + "\', product_desc = \'" + product_desc + "\' WHERE productid = \'" + id + "\'")
        conn.commit()
        elapse = time.time() - start
        print("Time for MySQL: " + str(elapse)+"s")
    return redirect("/")

# Delete category (in category search results table)

@app.route('/category/delete', methods=['GET', 'POST'])
def deleteCategory():
    if request.method == "POST":
        input = request.form['categorydelete']
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("DELETE FROM is_category WHERE categoryid = \""+ input + "\"")
        cur.execute("DELETE FROM category WHERE categoryid = \""+ input + "\"")
        conn.commit()
    return redirect("/category/search")

# Delete review (in review search results table)

@app.route('/review/delete', methods=['GET', 'POST'])
def deleteReview():
    if request.method == "POST":
        input = request.form['reviewdelete']
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("DELETE FROM has_review WHERE reviewid = \""+ input + "\"")
        cur.execute("DELETE FROM written_by WHERE reviewid = \""+ input + "\"")
        cur.execute("DELETE FROM review WHERE reviewid = \""+ input + "\"")
        conn.commit()
    return redirect("/review/search")
    
if __name__ == "__main__":
    app.run(debug=True)