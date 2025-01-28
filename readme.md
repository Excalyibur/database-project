# Amazin
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)

## _One stop shopping portal_


## Getting Started
* `git clone https://github.com/whathellahor/2008-db.git`
* in directory, create virtual environment in python `py -m venv venv`
* in the directory, activate the virtual environment `./venv/Scripts/activate`

### Install libraries / dependencies
* `pip install Flask`
* `pip install Flask-MySQLdb`
* `pip install mysql-connector-python`
* `pip install numpy`
* `pip install matplotlib`
* `pip install pandas`
* `pip install pymongo` 
* `pip install re` 

### To run the web application
Remember to check your MySQL configurations in `config > configsql.py` and in `python-sql > script.py`
* cd flask
* open 1 terminal and run `py app.py`
* open another terminal and run `py appMongo.py`
* run website which uses MySQL implementation at: http://localhost:5000/
* run website which uses MongoDB implementation at: http://localhost:5001/

-----------------------------------------------------------------------------------------------------------------------------------------
# How to use web application
* `http://localhost:5000/createcategory` : Create a new category (e.g. 00000009, AWatchCategory)
* `http://localhost:5000/createuser` : Create a new user (e.g. AAAAAUser1, UserA)
* `http://localhost:5000/createproduct` : Create a new product (e.g. B002WATCHA, WatchA, 20.45, 0.45, This is a watch, https://m.media-amazon.com/images/I/61LO6l4zB4L._UX522_.jpg, https://www.amazon.in/LOUIS-DEVIN-Silicone-Analog-LD-BK054-BLACK/dp/B0BD5R89RQ/ref=sr_1_6?crid=27JSY6235EDPN&keywords=watch&qid=1679929122&sprefix=wat%2Caps%2C564&sr=8-6, 5378, 4.3, select AWatchCategory in dropdown)
* `http://localhost:5000/createreview` : Create a new review (e.g. select B002PWATCHA in dropdown, R100AAAAREVIEW, Good watch will buy again, select UserA in dropdown)
* `http://localhost:5000/` : Search for a product in the search bar (e.g Watch)
* `http://localhost:5000/search` : See a list of products that contains 'watch' as the keyword. Click on 'Edit' button and edit the Name and Description column, afterwards click update and search for 'Watch' in `http://localhost:5000/` to see updates. Click on 'Delete' button and see product being deleted from database.
* `http://localhost:5000/` : Click on 'Category' button and search for 'Computers'
* `http://localhost:5000/category/search` : See a list of products in the category that contains 'Computers' as the keyword.
* `http://localhost:5000/` : Click on 'Review' button and search for 'Good'
* `http://localhost:5000/review/search`: See a list of products that has 'Good' in their reviews and show the username of the user who left the review.
* `http://localhost:5000/` : Click on 'Ratings' button and search for '>=4.1'. Remember to include any operators before the rating number in the searchbar.
* `http://localhost:5000/ratings/search` : See a list of products that have ratings more than or equals to 4.1
* `http://localhost:5000/dashboard` : View dashboard insights

-----------------------------------------------------------------------------------------------------------------------------------------
# Code Structure

| File  | Description |
| ------------- | ------------- |
| `datasets` | A folder containing the list of datasets used for this web application. Will be used later on to insert into MySQL database. |
| `flask` | A folder containing the codes for the Flask web application. |

## flask

| File  | Description |
| ------------- | ------------- |
| `static` | Contains images and `stylesheet.css` which is used to design the web application. |
| `templates` > `create` | Contains the respective HTML files used to show create forms for: creating new category (`createcategory.html`), create new product (`createproduct.html`), create new review (`createreview.html`) and create new user (`createuser.html`). |
| `templates` > `searchres` | Contains the respective HTML files used to display search results for: search for products by category (`categoryres.html`), search for products by product keyword (`productres.html`), search for products by ratings (`ratingsres.html`), search for products by review keyword (`reviewres.html`)  |
| `dashboard.html` | HTML file used to design the dashboard UI. |
| `index.html` | HTML file used to create and design the main page for the web application. |

# MySQL Code Structure

First, create tables in MySQL Workbench using the `create_tables_queries.sql` and insert data from the datasets into the MySQL database by running the respective functions in `scripts.py`.

## python-sql

| File  | Description |
| ------------- | ------------- |
| `create_tables_queries.sql`  | Run these create table sql queries in MySQL Workbench |
| `functions.py`  | Optional use but you can run the functions one by one to cross check the number of rows with the datasets under the `datasets` folder. |
| `script.py`  | Used to run the functions one by one to insert data from datasets into the tables created in MySQL using `create_tables_queries.sql`. |

To execute queries via the web application using MySQL implementation, `cd flask` in project directory and run the command `app.py`. Afterwards, go to http://localhost:5000/ to view the web application.

In the web application, you can try to search for a product name at http://localhost:5000/ which is also the Home page. In the product search results, you can click on the 'Edit' buttton to edit the product name and product description which after you click on the 'Update' button to update the changes. You can click on 'Category' button to search for a category name, 'Review' button to search for a review keyword, and 'Rating' button to search for a range of ratings (for example: >=4.1). 

You can click on Dashboard and it will redirect you to http://localhost:5000/dashboard which displays some insightful statistics and graphs based on the datasets.

You can also click on the respective create pages to create new products, reviews, users and categories.

# MongoDB Code Structure

Ensure MongoDB is running at `mongodb://localhost:27017/`. cd into `2008-DB/python-mongo` and run `script.py`. 
## python-mongo

| File  | Description |
| ------------- | ------------- |
| `script.py`  | Used to run the functions one by one to insert data from json files into seperate collections in MongoDB. |

To execute queries via the web application using MongoDB implementation, `cd flask` in project directory and run the command `appMongo.py`. Afterwards, go to http://localhost:5001/ to view the web application.

Similiar to the SQL Implementaion of the Web Application, the actions to run the queries are the same. However, `the MongoDB implementation does not have a function for viewing the Dashboard insights.`
