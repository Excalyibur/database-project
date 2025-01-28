from flask import Flask, request, redirect, url_for, render_template
from pymongo import MongoClient
import pymongo
import sys
from bson.objectid import ObjectId
sys.path.append("/config/")
from config import configsql as config
import time

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.db2008
products = db.products
users = db.users
categoryDB = db.category

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/createproduct', methods=['GET', 'POST'])
def create_product():
    products.find({}, {"_id": 0, "name": 1})
    allcategory = categoryDB.find({}, {"categoryid": 1, "category_name": 1})
    data = []
    for document in allcategory:
        category = (document["categoryid"], document["category_name"])
        data.append(category)
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
        categorychoice = int(request.form['categorychoice'])
        selectedCategory = categoryDB.find_one({"categoryid":categorychoice})
        categoryName = [selectedCategory["category_name"]]
        reviews = {}
        new_product = {
            "productid": productid,
            "product_name": product_name,
            "actual_price": actual_price,
            "discount_percentage": discount_percentage,
            "product_desc": product_desc,
            "img_link": img_link,
            "product_link": product_link,
            "rating_count": rating_count,
            "rating": rating,
            "category": categoryName,
            "reviews": reviews
        }

        # Insert the new product into the collection
        result = products.insert_one(new_product)

        # Print the ID of the inserted document
        print("Inserted product with ID:", result.inserted_id)
    return render_template('create/createproduct.html', data=data)

@app.route('/createreview', methods=['GET', 'POST'])
def create_review():
    allProductId = products.find({}, {"productid": 1, "product_name": 1})
    data = []
    for document in allProductId:
        productIds = (document["productid"],document["product_name"])
        data.append(productIds)
    
    allUserId = users.find({}, {"userid": 1, "username": 1}).sort("username",1)
    data2 = []
    for document in allUserId:
        userIds = (document["userid"],document["username"])
        data2.append(userIds)

    if request.method == 'POST':
        # Retrieve form data
        review = request.form['review']
        user = request.form['userchoice']
        productid = request.form['productchoice']
        new_review = {user:review}
        update_doc = {"$set": {}}
        for key, value in new_review.items():
            update_doc["$set"]["reviews." + key] = value
        result = products.update_one({"productid":productid}, update_doc)
        print("Modified items: ", result.modified_count)
    return render_template('create/createreview.html', data=data, data2=data2)

@app.route('/createuser', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        userid = request.form['userid']
        username = request.form['username']
        
        new_user = {
            "userid":userid,
            "username":username
        }
        result = users.insert_one(new_user)
        print("inserted user: ", result.inserted_id)
    return render_template('create/createuser.html')

@app.route('/createcategory', methods=['GET', 'POST'])
def create_category():
    if request.method == 'POST':
        categoryid = request.form['categoryid']
        category_name = request.form['category_name']
        new_category = {
            "categoryid":categoryid,
            "category_name":category_name
        }
        result = categoryDB.insert_one(new_category)

    return render_template('create/createcategory.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Search for products by product keyword

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        input = request.form['searchres']
        if not input:
            print("null")
            return redirect('/')
        start =  time.time()
        query = {"product_name":{"$regex": input,"$options":"i"}}
        result = products.find(query)
        data = []
        for document in result:
            productDetail = (document["productid"],document["product_name"],document["product_desc"],document["img_link"],document["product_link"])
            data.append(productDetail)
        elapse = time.time() - start
        string = "You are currently viewing products with keyword: '"+ input + "'"
        string2 = "{} results in {timer:.3f}s".format(len(data), timer=elapse)
        return render_template('searchres/productres.html', data=data, headers="", string=string, string2=string2)
    return render_template('index.html')

# Search for product by category name

@app.route('/category/search', methods=['GET', 'POST'])
def searchcat():
    if request.method == "POST":
        input = request.form['searchres']
        if not input:
            print("null")
            return redirect('/category')
        start = time.time()
        query = { "category": { "$regex": input, "$options": "i" } }
        result = products.find(query)
        data = []
        for document in result:
            for category in document["category"]:
                if input.lower() in category.lower():
                    categoryName = category
                    categoryObject = categoryDB.find_one({"category_name": categoryName} )
                    categoryId = categoryObject["categoryid"]
                    break
            
            productDetail = (document["productid"],document["product_name"],document["img_link"],categoryName,document["product_link"],categoryId)
            data.append(productDetail)
        elapse = time.time() - start
        string = "You are currently viewing products in category: '"+ input + "'"
        string2 = "{} results in {timer:.3f}s".format(len(data), timer=elapse)
        return render_template('searchres/categoryres.html', data=data, headers="", string=string, string2=string2)
    return render_template('index.html')

# Search for product by review keyword

@app.route('/review/search', methods=['GET', 'POST'])
def searchreview():
    if request.method == "POST":
        input = request.form['searchres']
        query = ([
                {
                    "$project": {
                    "rev": {
                        "$objectToArray": "$reviews"
                    }
                    }
                },
                {
                    "$project": {
                    "rev": {
                        "$filter": {
                        "input": "$rev",
                        "cond": {
                            "$regexMatch": {
                            "input": "$$this.v",
                            "regex": input,
                            "options": "i"
                            }
                        }
                        }
                    }
                    }
                },
                {
                    "$unwind": "$rev"
                }
                ])

        start = time.time()
        data = []
        result = products.aggregate(query)
        for item in result:
            objectId = ObjectId(item["_id"])
            currentProduct = products.find_one({'_id': objectId})
            review = item["rev"]
            reviewUser = users.find_one({'userid': review["k"]})
            productDetail = (currentProduct["productid"],currentProduct["product_name"],currentProduct["img_link"],review["v"],reviewUser["username"])
            data.append(productDetail)
        elapse = time.time() - start
        string = "You are currently viewing reviews that has: '"+ input + "'"
        string2 = "{} results in {timer:.3f}s".format(len(data), timer=elapse)
        return render_template('searchres/reviewres.html', data=data, headers="headers", string=string, string2=string2)
    return render_template('index.html')

# Search for product by a range of ratings

@app.route('/ratings/search', methods=['GET', 'POST'])
def searchrating():
    if request.method == "POST":
        input = request.form['searchres']
        if not input:
            print("null")
            return redirect('/')
        start =  time.time()
        query = {"rating":{'$gte':float(input)}}
        result = products.find(query).sort("rating", pymongo.ASCENDING)
        data = []
        for document in result:
            productDetail = (document["productid"],document["product_name"],document["img_link"],document["product_link"],document["rating"])
            data.append(productDetail)
        elapse = time.time() - start
        string2 = "{} results in {timer:.3f}s".format(len(data), timer=elapse)
        string = "You are currently viewing products that has ratings: >= '"+ input + "'"
        return render_template('searchres/ratingsres.html', data=data, headers="", string=string, string2=string2)
    return render_template('index.html')

# Delete product (in product search result table)

@app.route('/product/delete', methods=['GET', 'POST'])
def deleteProductId():
    if request.method == "POST":
        input = request.form['productdelete']
        start =  time.time()
        query = {"productid":input}
        products.delete_one(query)
        elapse = time.time() - start
        print("Timer for deleting in Mongo: " + str(elapse)+"s")
    return redirect("/")

# Edit and update product name and description (in product search result table)

@app.route('/product/update', methods=['GET', 'POST'])
def updateProductId():
    if request.method == "POST":
        id = request.form['id']
        product_desc = request.form['description']
        product_name = request.form['name']
        query = {"productid":id}
        updated_value = {"$set": {"product_desc":product_desc,"product_name":product_name}}
        start =  time.time()
        products.update_one(query,updated_value)
        elapse = time.time() - start
        print("Timer for Mongo: " + str(elapse)+"s")
    return redirect("/")

# Delete category (in category search result table)

@app.route('/category/delete', methods=['GET', 'POST'])
def deleteCategory():
    if request.method == "POST":
        input = request.form['categorydelete']
        print("input is: " + input)
        categoryObject = categoryDB.find_one({"categoryid": int(input)})
        categoryname = categoryObject["category_name"] 
        query = {"category":categoryname}
        new_value = {"$pull":{"category":categoryname}}
        result = products.update_many(query,new_value)
    return redirect("/category/search")

# Delete review (in review search result table)

@app.route('/review/delete', methods=['GET', 'POST'])
def deleteReview():
    if request.method == "POST":
        input = request.form['reviewdelete']
        query = {"review":{"$regex":input, "$options":"i"}}
        result = products.find(query)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port = 5001)
