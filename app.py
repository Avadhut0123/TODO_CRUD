from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

# MySQL Database Connection
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://admin2:abcd1234'@localhost/avengers"

# sqlite Database Connection
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"

# Security Purpose SET Yes for the Modification
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

# Storing Data in the database
db = SQLAlchemy(app)
app.app_context().push()


# Creating the columns in the database with their Data Types
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"


# Main route
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    all_todo = Todo.query.all()
    # print(all_todo)
    return render_template("index.html", all_todo=all_todo)


# update Page
@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)


# delete route
@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


# Running the application with the port number as 80
if __name__ == "__main__":
    app.run(debug=True, port="80")
