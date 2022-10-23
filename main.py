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

# App runner
if __name__ == '__main__':
    app.run()