import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CONFIGURACIÓN DE BASE DE DATOS (Soporta SQLite local y MySQL en la nube vía variables de entorno)
# Según la nota, usamos SQLite por ahora; en la fase final usaremos DATABASE_URL para MySQL.
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'extranjeria.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELO DE DATOS (Ejemplo: Tabla para gestionar Trámites)
class Tramite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(50), default='Pendiente')

# Crear la base de datos al iniciar
with app.app_context():
    db.create_all()

# 1. RUTA PRINCIPAL (/)
@app.route('/')
def home():
    return """
    <h1>Sistema de Gestión de Extranjería - Asesoría Kandy Vera</h1>
    <p>Propósito: Gestión integral de visas, residencias y trámites legales para extranjeros.</p>
    <hr>
    <p>Use la ruta <b>/tramite/nombre_del_tramite</b> para consultar estados.</p>
    """

# 2. RUTA DINÁMICA (/tramite/<tipo_tramite>)
@app.route('/tramite/<tipo_tramite>')
def tramite(tipo_tramite):
    return f"<h1>Trámite: {tipo_tramite.capitalize()}</h1><p>Bienvenido. Su solicitud de {tipo_tramite} está siendo procesada exitosamente por nuestro equipo legal.</p>"

if __name__ == '__main__':
    # Configuración para que funcione tanto local como en Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)