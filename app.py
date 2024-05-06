from flask import Flask, render_template, request 
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from collections import Counter
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key = True)
    email_ = db.Column(db.String(120), unique = True)
    name_ = db.Column(db.String(120))

    def __init__(self, email_, name_):
        self.email_ = email_
        self.name_ = name_

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods = ['POST'])
def success():
    if request.method == 'POST':
        email = request.form["email_name"]
        ani_name = request.form["anime_name"]
        max_anim_name = max_anime()
        # print(ani_name)
        
        if db.session.query(Data).filter(Data.email_ == email).count() == 0:
            data = Data(email , ani_name )
            db.session.add(data)
            db.session.commit()
            send_email(email,ani_name,max_anim_name)
            return render_template("success.html") 
    return render_template("index.html", text = "Seems like we have already collected your data")

def max_anime():
    all_anime = db.session.query(Data.name_).all()
    ani_count = Counter(ani_name for ani_name in all_anime)
    max_freq = max(ani_count, key = ani_count.get)
    return max_freq 

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False)
