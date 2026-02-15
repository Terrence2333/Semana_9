import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_terrence_m' # Clave para mensajes flash

# CONFIGURACIÓN PROFESIONAL DE DB
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'extranjeria.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELO EXPERTO (Añadimos fecha y validación básica)
class Tramite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(50), default='En Revisión')

# Inicializar DB
with app.app_context():
    db.create_all()

# RUTA PRINCIPAL CON DISEÑO PROFESIONAL
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <title>Terrence.m | Gestión Legal</title>
    </head>
    <body class="bg-light">
        <nav class="navbar navbar-dark bg-primary shadow">
            <div class="container"><a class="navbar-brand" href="#">Terrence.m - Consultoría de Extranjería</a></div>
        </nav>
        <div class="container mt-5">
            <div class="card shadow-lg p-4">
                <h1 class="text-primary">Panel de Control de Trámites</h1>
                <p class="lead">Gestión de visas y residencias con estándares legales internacionales.</p>
                <hr>
                <div class="alert alert-info">Sistema activo y conectado a la base de datos.</div>
                <table class="table table-hover mt-3">
                    <thead class="table-dark">
                        <tr><th>Servicio</th><th>Estado</th><th>Prioridad</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Visa de Residencia</td><td><span class="badge bg-success">Activo</span></td><td>Alta</td></tr>
                        <tr><td>Asesoría Migratoria</td><td><span class="badge bg-warning">Pendiente</span></td><td>Media</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """

# MANEJO DE ERRORES (Nivel Experto)
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>Error 404</h1><p>El trámite solicitado no existe en nuestra base legal.</p>", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
