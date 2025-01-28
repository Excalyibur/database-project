import csv

# cross check number of rows with .csv

def category():

    counter = 0
    filename = "datasets\\amazon - CATEGORY.csv"

    with open(filename, "r", encoding='utf-8', errors='replace') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            string = row[0] + ":" + row[1]
            counter += 1
            print(string)
        print(counter)


def user():
    counter = 0
    filename = "datasets\\amazon - USER.csv"

    with open(filename, "r", encoding='utf-8', errors='replace') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            string = str(counter) + ":" + str(row[0]) + ":" + row[1]
            counter += 1
            print(string)
        print(counter)


def review():
    counter = 0
    filename = "datasets\\amazon - REVIEW.csv"

    with open(filename, "r", encoding='utf-8', errors='replace') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            string = str(counter) + ":" + str(row[0]) + ":" + row[1]
            counter += 1
            print(string)
        print(counter)


def written_by():
    counter = 0
    filename = "datasets\\amazon - WRITTEN_BY.csv"

    with open(filename, "r", encoding='utf-8', errors='replace') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            string = str(counter) + ":" + str(row[0]) + ":" + row[1]
            counter += 1
            print(string)
        print(counter)

def product():
    counter = 0
    filename = "datasets\\amazon - PRODUCT.csv"

    with open(filename, "r", encoding='utf-8', errors='replace') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            string = str(counter) + ":" + str(row[0]) + ":" + row[1]
            counter += 1
            print(row[-1])
        print(counter)

def is_category():
    counter = 0
    filename = "datasets\\amazon - IS_CATEGORY.csv"

    with open(filename, "r", encoding='utf-8', errors='replace') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            string = str(counter) + ":" + str(row[0]) + ":" + row[1]
            counter += 1
            print(row[-1])
        print(counter)

def has_review():
    counter = 0
    filename = "datasets\\amazon - HAS_REVIEW.csv"

    with open(filename, "r", encoding='utf-8', errors='replace') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            string = str(counter) + ":" + str(row[0]) + ":" + row[1]
            counter += 1
            print(row[-1])
        print(counter)

# change this function to run and check if the number of rows matches the excel dataset
has_review()
