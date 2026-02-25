import os
from flask import Flask, render_template, url_for

# 1. Configurazione dei percorsi
basedir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(basedir, '../Client/templates')
static_dir = os.path.join(basedir, '../Client/static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# 2. Rotte

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chi-siamo')
def chi_siamo():
    return render_template('chi-siamo.html')

@app.route('/qualita')
def qualita():
    return render_template('qualita.html')

@app.route('/personalizzazioni')
def personalizzazioni():
    return render_template('personalizzazioni.html')

@app.route('/collezioni')
def collezioni():
    return render_template('collezioni.html')

@app.route('/journal')
def journal():
    return render_template('journal.html')

@app.route('/contatti')
def contatti():
    return render_template('contatti.html')

# 3. Avvio dell'applicazione

if __name__ == '__main__':
    app.run(debug=True)