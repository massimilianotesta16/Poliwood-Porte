import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, url_for, jsonify, request, session, redirect
from db import Utente, db, Collezione, Finitura, Modello, ModelloVariante, Variante, Articolo, GalleriaImmagini
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from wtforms import PasswordField

basedir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(basedir, '../Client/templates')
static_dir = os.path.join(basedir, '../Client/static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poliwood.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chiave_di_emergenza_molto_sicura_2026')

db.init_app(app)

with app.app_context():
    db.create_all()

# --- CLASSI DI SICUREZZA PER L'ADMIN ---

class SecureModelView(ModelView):
    def is_accessible(self):
        return session.get('logged_in') == True
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return session.get('logged_in') == True
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
    
class UtenteModelView(SecureModelView):
    column_exclude_list = ['password']
    form_extra_fields = {
        'password': PasswordField('Password (scrivi per impostare/cambiare)')
    }
    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.set_password(form.password.data)

# --- INIZIALIZZAZIONE ADMIN ---

admin = Admin(
    app, 
    name='Poliwood Admin', 
    index_view=MyAdminIndexView(endpoint='admin'),
    url='/admin'
)

admin.add_view(SecureModelView(Collezione, db.session, name="Le mie Collezioni", category="Catalogo"))
admin.add_view(SecureModelView(Modello, db.session, name="Porte/Modelli", category="Catalogo"))
admin.add_view(SecureModelView(Finitura, db.session, name="Finiture", category="Dettagli"))
admin.add_view(SecureModelView(Variante, db.session, name="Varianti", category="Dettagli"))
admin.add_view(SecureModelView(Articolo, db.session, name="Articoli Completi", category="Catalogo"))
admin.add_view(UtenteModelView(Utente, db.session, name="Gestione Admin", category="Sicurezza"))

admin.add_link(MenuLink(name='Vai al Sito', url='/'))
admin.add_link(MenuLink(name='Esci (Logout)', url='/logout'))

# --- CONTEXT PROCESSOR (Globali) ---

@app.context_processor
def inject_collezioni():
    return dict(collezioni=Collezione.query.all())

# --- ROTTE DELL'APPLICAZIONE ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/collezioni')
def collezioni():
    return render_template('collezioni.html')

@app.route('/collezione/<int:collezione_id>')
def collezione(collezione_id):
    collezione_singola = Collezione.query.get_or_404(collezione_id)
    return render_template('collezione.html', collezione=collezione_singola)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_inserito = request.form.get('username')
        password_inserita = request.form.get('password')
        utente = Utente.query.filter_by(nome_utente=username_inserito).first()
        if utente and utente.check_password(password_inserita):
            session['logged_in'] = True
            session['user_id'] = utente.id_utente
            session['username'] = utente.nome_utente
            return redirect(url_for('admin.index'))
        else:
            return render_template('login.html', error="Credenziali non valide")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('login'))

@app.route('/chi-siamo')
def chi_siamo():
    return render_template('chi-siamo.html')

@app.route('/qualita')
def qualita():
    return render_template('qualita.html')

@app.route('/personalizzazioni')
def personalizzazioni():
    return render_template('personalizzazioni.html')

@app.route('/journal')
def journal():
    return render_template('journal.html')

@app.route('/contatti')
def contatti():
    return render_template('contatti.html')

# --- AVVIO ---

if __name__ == '__main__':
    app.run(debug=True)