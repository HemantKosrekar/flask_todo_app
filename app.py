from flask import Flask, render_template ,request ,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import pytz

app = Flask(__name__) # To initialize the app
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

india_timezone = pytz.timezone('Asia/Kolkata')

# Get the current date and time in the specified timezone
# current_time_india = datetime.now(india_timezone)
# current_time_india.strftime("%Y-%m-%d %H:%M:%S")


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key =True)
    title = db.Column(db.String(200), nullable =False)
    desc = db.Column(db.String(500), nullable =False)
    date_created = db.Column(db.DateTime, default=datetime.now(india_timezone))


    def __repr__(self):
        return f"{self.sno} - {self.title}"

@app.route("/",methods=["GET","POST"]) # create a route [endpoints]
def hello_world():

    # check sqllite database working or not
    if request.method == "POST":
        title_value = request.form['title']
        desc_value = request.form['desc']
        if title_value and desc_value:
            todo = Todo(title = title_value,desc = desc_value )
            db.session.add(todo)
            db.session.commit()

    allTodo = Todo.query.all()

    return render_template('index.html',allTodo=allTodo)


@app.route("/delete/<int:sno>",methods=["GET"])
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect("/")

@app.route("/update/<int:sno>",methods=["GET","POST"])
def update(sno):

    if request.method == "POST":
        title_value = request.form['title']
        desc_value = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title_value
        todo.desc = desc_value
        db.session.commit()

        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)