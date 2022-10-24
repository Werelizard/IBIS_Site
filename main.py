# Imports
from flask import Flask, render_template, abort, redirect, url_for
 
# Build the app
app = Flask(__name__)
app.debug = True
 
# Ressources
@app.route('/')
def indexReroute():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')
 
@app.route('/references')
def references():
    return render_template('references.html')

@app.route('/search/translation')
def translation():
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