# Imports
from difflib import restore
import json
from turtle import pos
from flask import Flask, render_template,redirect, request, url_for
import sqlite3
 
# Fetch configuration files
appConfiguration =  json.load(open('appConfig/appConfiguration.json','r'))
secretKey = appConfiguration['secretKey']

# Build the app
app = Flask(__name__)
app.config['SECRET_KEY'] = secretKey
app.debug = True

#Database connection
db_name = 'ibis.db'

def get_db_connection():
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn
 
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

# Ressources for form pages
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/search/meta')
def meta():
    return render_template('meta.html')

@app.route('/search/translation', methods=('GET', 'POST'))
def translation():
    if request.method == 'POST':
        try:
            #Get variables from form
            translationRequest = request.form['translation']
            try:
                startWithQueryOnly = request.form['searchFirstMatchingOnly']; startWithQueryOnly = True
            except:
                startWithQueryOnly = False
            
            #Ping the SQL databse if argument, refresh page if nothing
            if translationRequest:
                conn = get_db_connection()
                #Determine whether to look for words starting with the request or words containing the request
                if startWithQueryOnly:
                    conn.execute("PRAGMA case_sensitive_like = 1")
                    output = conn.execute("SELECT * FROM hieroglyphs WHERE UPPER(hieroglyphs.translation) LIKE  UPPER('" + translationRequest.lower() +"%') OR UPPER(hieroglyphs.translationEnglish) LIKE  UPPER('" + translationRequest.lower() +"%')").fetchall()
                else:
                    conn.execute("PRAGMA case_sensitive_like = 1")
                    output = conn.execute("SELECT * FROM hieroglyphs WHERE UPPER(hieroglyphs.translation) LIKE  UPPER('%" + translationRequest.lower() +"%') OR UPPER(hieroglyphs.translationEnglish) LIKE  UPPER('%" + translationRequest.lower() +"%')").fetchall()
                conn.close()

                #Repackage the query results into a dictionary for later iterations
                if len(output) < 1:
                    entries = 'None'
                else:
                    entries = {}; index = 0
                    for entry in output:
                        entries[index] = {'translation': entry['translation'],'translationEnglish': entry['translationEnglish'],'transliteration': entry['transliteration'],'gardiner':entry['gardiner'],'tags':entry['tags'],'notes':entry['notes'],'index':entry['index'],'kings1':entry['kingsPersonal'],'kings2':entry['kingsHorus'],'kings3':entry['kingsGolden'],'kings4':entry['kingsNbti'],'kings5':entry['kingsNyswt']}
                        index = index + 1

                #Return template
                print(entries)
                return render_template('translationOutput.html', entries = entries)
        
        #If error, log error to console and return default page
        except Exception as error:
            error_text = str(error); print(error_text)
            return render_template('translation.html')

    #Default behavior
    return render_template('translation.html')

@app.route('/search/transliteration', methods=('GET', 'POST'))
def translitertion():
    if request.method == 'POST':
        try:
            #Get variables from form
            transliterationRequest = request.form['transliteration']
            try:
                startWithQueryOnly = request.form['searchFirstMatchingOnly']; startWithQueryOnly = True
            except:
                startWithQueryOnly = False
            
            #Ping the SQL databse if argument, refresh page if nothing
            if transliterationRequest:
                conn = get_db_connection()
                #Determine whether to look for words starting with the request or words containing the request
                if startWithQueryOnly:
                    conn.execute("PRAGMA case_sensitive_like = 1")
                    output = conn.execute("SELECT * FROM hieroglyphs WHERE hieroglyphs.transliteration LIKE '" + transliterationRequest +"%'").fetchall()
                # else:
                #     output = conn.execute("SELECT * FROM hieroglyphs WHERE hieroglyphs.transliteration LIKE '%" + transliterationRequest +"%' OR hieroglyphs.translationEnglish LIKE  '%" + transliterationRequest +"%'").fetchall()
                else:
                    conn.execute("PRAGMA case_sensitive_like = 1")
                    output = conn.execute("SELECT * FROM hieroglyphs WHERE hieroglyphs.transliteration LIKE '%" + transliterationRequest +"%'").fetchall()
                conn.close()

                #Repackage the query results into a dictionary for later iterations
                if len(output) < 1:
                    entries = 'None'
                else:
                    entries = {}; index = 0
                    for entry in output:
                        entries[index] = {'translation': entry['translation'],'translationEnglish': entry['translationEnglish'],'transliteration': entry['transliteration'],'gardiner':entry['gardiner'],'tags':entry['tags'],'notes':entry['notes'],'index':entry['index'],'kings1':['kingsPersonal'],'kings2':['kingsHorus'],'kings3':['kingsGolden'],'kings4':['kingsNbti'],'kings5':['kingsNyswt']}
                        index = index + 1

                #Return template
                return render_template('transliterationOutput.html', entries = entries)

        #If error, log error to console and return default page
        except Exception as error:
            error_text = str(error); print(error_text)
            return render_template('transliteration.html')
    
    #Default behavior
    return render_template('transliteration.html')

@app.route('/search/hieroglyphics')
def hieroglyphics():
    return render_template('hieroglyphics.html')
 
@app.route('/references')
def references():
    indexValue = request.args.get('index')
    #Ping the SQL databse if argument, refresh page if nothing
    if indexValue:
        conn = get_db_connection()
        #Look for matching ID
        output = conn.execute("SELECT * FROM hieroglyphs WHERE hieroglyphs.id =" + indexValue).fetchall()
        entries = {}
        for entry in output:
            entries['translation'] = entry['translation']
            try:
                entries['tags'] = entry['tags'].split(',')
            except:
                entries['tags'] = ['None']
            try:
                entries['outerLinks'] = entry['outerLinks'].split(',')
            except:
                entries['outerLinks'] = 'None'
            try:
                entries['bibliography'] = entry['bibliography'].split(',')
            except:
                entries['bibliography'] ='None'
            try:
                entries['grouping'] = entry['grouping'].split(',')
            except:
                entries['grouping'] ='None'
            entries['notes'] = entry['notes']

            #Kings name if there
            entries['kings1'] = entry['kingsPersonal']
            entries['kings2'] = entry['kingsHorus']
            entries['kings3'] = entry['kingsGolden']
            entries['kings4'] = entry['kingsNbti']
            entries['kings5'] = entry['kingsNyswt']
        #Fetch group info if there is any
        if entries['grouping'] != 'None':
            groupsIDs= {}

            for groupTag in entries['grouping']:
                groupsIDs[groupTag] = []
                conn = get_db_connection()
                output = conn.execute("SELECT hieroglyphs.id, hieroglyphs.translation FROM hieroglyphs WHERE hieroglyphs.grouping = '" + groupTag + "'").fetchall()
                conn.close()
                for result in output:
                    tempResultList = []
                    tempResultList.append(result['id'])
                    tempResultList.append(result['translation'])
                    groupsIDs[groupTag].append(tempResultList)
                print(groupTag)
            print(groupsIDs)
        
        #Make a default entry object / fallback
        if entries == {}:
            entries = 'None'

        #Render Template
        if groupsIDs:
            return render_template('references.html', index = indexValue, entries = entries, groupInfo = groupsIDs)
        else:
            return render_template('references.html', index = indexValue, entries = entries)
    else:
        return render_template('403.html')

# Error handling ressources
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(403)
def bad_request(e):
    return render_template('403.html')

# App runner
if __name__ == '__main__':
    app.run()