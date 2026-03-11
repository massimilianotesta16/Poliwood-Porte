# seed.py
from app import app
from db import Utente, db, Collezione
from werkzeug.security import generate_password_hash, check_password_hash


def popola_database():
    with app.app_context():


        print("Inserimento dati in corso...")

        # Creazione di un utente admin
        admin_user1 = Utente(nome_utente='Massimiliano', password=generate_password_hash("MT03112007_S"))
        admin_user2 = Utente(nome_utente='Maurizio', password=generate_password_hash("MT04061968_F"))
        admin_user3 = Utente(nome_utente='Giuseppe', password=generate_password_hash("G17061966_F"))
        admin_user4 = Utente(nome_utente='Stefania', password=generate_password_hash("S13031969_S"))

        db.session.add(admin_user1)
        db.session.add(admin_user2)
        db.session.add(admin_user3)
        db.session.add(admin_user4)
        db.session.commit()

        print("Utenti creati con successo")

if __name__ == '__main__':
    popola_database()