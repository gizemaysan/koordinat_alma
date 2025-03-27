from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging
from flask_migrate import Migrate  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///koordinatlar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "gizli_anahtar" 

db = SQLAlchemy(app)
migrate = Migrate(app, db)  

# Koordinat Modeli
class Koordinat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    satici_id = db.Column(db.Integer, nullable=False)  
    enlem = db.Column(db.Float, nullable=False)
    boylam = db.Column(db.Float, nullable=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)
    aciklama = db.Column(db.String(255), nullable=True)  

    def __repr__(self):
        return f"<Koordinat {self.id} ({self.aciklama if self.aciklama else 'Açıklama Yok'})>"


# Ana sayfa (Koordinat Ekleme)
@app.route("/")
def index():
    seller_id = session.get("seller_id", "12345") 
    return render_template("index.html", seller_id=seller_id)

# Koordinat ekleme
@app.route('/ekle', methods=['POST'])
def add_koordinat():
    try:
        data = request.get_json() if request.is_json else request.form
        satici_id = int(data['satici_id'])
        enlem = float(data['enlem'])
        boylam = float(data['boylam'])
        aciklama = data.get('aciklama', '')

        yeni_koordinat = Koordinat(
            satici_id=satici_id,
            enlem=enlem,
            boylam=boylam,
            aciklama=aciklama
        )

        db.session.add(yeni_koordinat)
        db.session.commit()
        
        return jsonify({"mesaj": "Koordinat başarıyla eklendi!", "id": yeni_koordinat.id, "redirect": url_for('onay')}), 201

    except Exception as e:
        app.logger.error(f"Koordinat eklerken hata oluştu: {e}")
        return jsonify({"hata": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
