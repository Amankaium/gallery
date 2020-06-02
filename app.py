from flask import Flask, render_template, request
from openpyxl import load_workbook
from database import *

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        images = session.query(Picture).all()
    elif request.method == "POST":
        search_key = request.form.get("search_key")
        images = session.query(Picture).\
            filter(Picture.name.like("%{}%".format(search_key))).all()
    return render_template("index.html", images=images)

@app.route("/add")
def add():
    authors = session.query(Author)
    session.commit()
    return render_template("form.html", authors=authors)

@app.route("/reciever", methods=["POST"])
def reciever():
    url = request.form.get("url")
    name = request.form.get("name")
    description = request.form.get("description")
    price = int(request.form.get("price"))
    author = request.form.get("author")
    if author:
        author = int(author)

    new_image = Picture(
        name=name,
        url=url,
        description=description,
        price=price,
        author=author  
    )

    session.add(new_image)
    session.commit()

    return render_template("success.html")

@app.route("/author_reciever", methods=["GET", "POST"])
def author_reciever():
    if request.method == "POST":
        name = request.form.get("name")
        country = request.form.get("country")
        new_author = Author(
            name=name,
            country=country
        )

        session.add(new_author)
        session.commit()

        return render_template("success.html")
    
    elif request.method == "GET":
        return render_template("author_form.html")


@app.route("/details/<int:id>", methods=["GET", "POST"])
def details(id):
    if request.method == "POST":
        image = session.query(Picture).get(id)
        session.delete(image)
        session.commit()
        return render_template("success.html")
       
    image = session.execute('''
        SELECT p.name, a.name AS author, p.price, p.description, p.url
        FROM Picture AS p
        JOIN Author AS a
        ON p.author = a.id
        WHERE p.id=%d
    ''' % id).first()
    session.commit()
    return render_template("details.html", image=image)