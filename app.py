from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
 
# Creating Flask app
app = Flask(__name__)
 
# Creating SQLAlchemy instance
db = SQLAlchemy()
 
user = "admin"
pin = "admin3311"
host = "database1.c3awyky0axj2.us-west-2.rds.amazonaws.com"
db_name = "notebooks_db_guilherme_oliveira"
 
# Configuring database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{pin}@{host}/{db_name}"
 
# Disable modification tracking
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing Flask app with SQLAlchemy
db.init_app(app)


# Creating Models
class Notebooks(db.Model):
    __tablename__ = "notebooks"
 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, unique=True)
    author = db.Column(db.String(500), nullable=False)


def create_db():
    with app.app_context():
        db.create_all()

# Home route
@app.route("/")
def home():
    details = Notebooks.query.all()
    return render_template("home.html", details=details)
 
 
# Add data route
@app.route("/add", methods=['GET', 'POST'])
def add_notebooks():
    if request.method == 'POST':
        book_title = request.form.get('title')
        book_author = request.form.get('author')
 
        add_detail = Notebooks(
            title=book_title,
            author=book_author
        )
        db.session.add(add_detail)
        db.session.commit()
        return redirect(url_for('home'))
 
    return render_template("notebooks.html")

if __name__ == "__main__":
    create_db()
    app.run(debug=True)