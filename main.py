# Imports
import json
from flask import Flask, render_template, abort, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
 
# Fetch configuration files
appConfiguration =  json.load(open('appConfig/appConfiguration.json','r'))
secretKey = appConfiguration['secretKey']

# Build the app
app = Flask(__name__)
app.config['SECRET_KEY'] = secretKey
app.debug = True

#Database configuration
db_name = 'ibis.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# Tables config
class hieroglyphs(db.Model):
    __tablename__ = 'hieroglyphs'
    index = db.Column(db.Integer, primary_key=True)
    translation = db.Column(db.String)
    transliteration = db.Column(db.String)
    gardiner = db.Column(db.String)
    tags = db.Column(db.String)
    transliterationAdjacencies = db.Column(db.String)
    notes = db.Column(db.String)
    references = db.Column(db.String)
 
# Ressources for static pages
@app.route('/')
def indexReroute():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')
 
@app.route('/references')
def references():
    return render_template('references.html')

# Ressources for form pages
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/search/translation', methods=('GET', 'POST'))
def translation():
    if request.method == 'POST':
        try:
            translationRequest = request.form['translation']
            if translationRequest:
                output = hieroglyphs.query.order_by(hieroglyphs.translation).all()
                print(output)
                return render_template('translationOutput.html',translationOutput = translationRequest)
            else:
                return render_template('translation.html')
        except Exception as error:
            error_text = str(error); print(error_text)
            return render_template('translation.html')
    return render_template('translation.html')

@app.route('/search/transliteration')
def translitertion():
    return render_template('transliteration.html')

@app.route('/search/hieroglyphics')
def hieroglyphics():
    return render_template('hieroglyphics.html')

# App runner
if __name__ == '__main__':
    app.run()