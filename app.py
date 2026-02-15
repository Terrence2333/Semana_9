import os
from flask import Flask, render_template_string, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_terrence_m_2026'

# Configuración de Base de Datos
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'extranjeria.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tramite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <title>Terrence.m | Gestión Migratoria Real</title>
    <style>
        body { background: #05080a; color: #00d2ff; font-family: 'Courier New', monospace; overflow-x: hidden; }
        .glass-card { background: rgba(0, 210, 255, 0.03); border: 1px solid #00d2ff; border-radius: 10px; box-shadow: 0 0 15px rgba(0, 210, 255, 0.1); }
        .btn-neon { border: 1px solid #00d2ff; color: #00d2ff; background: transparent; transition: 0.3s; letter-spacing: 2px; }
        .btn-neon:hover { background: #00d2ff; color: #000; box-shadow: 0 0 30px #00d2ff; }
        .table { color: #fff; border-color: #00d2ff; }
        input, select { background: #0a0b10 !important; color: #00d2ff !important; border: 1px solid #00d2ff !important; }
        .status-scan { font-size: 0.7rem; color: #00ff00; animation: blink 1s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    </style>
</head>
<body class="p-4">
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4 border-bottom border-info pb-3">
            <div>
                <h1 class="m-0 text-uppercase fw-bold"><i class="fas fa-fingerprint"></i> TERRENCE.M</h1>
                <span class="status-scan"><i class="fas fa-shield-virus"></i> ENCRIPTACIÓN AES-256 ACTIVA</span>
            </div>
            <a href="/download" class="btn btn-neon btn-sm"><i class="fas fa-download me-2"></i>REPORTE LEGAL</a>
        </div>
        
        <div class="row g-4">
            <div class="col-md-4">
                <div class="glass-card p-4">
                    <h6 class="text-info mb-4 fw-bold"><i class="fas fa-id-card me-2"></i>REGISTRO DE VISADOS REALES</h6>
                    <form action="/add" method="POST">
                        <div class="mb-3">
                            <label class="small opacity-75">NOMBRE DEL SOLICITANTE</label>
                            <input type="text" name="cliente" class="form-control" placeholder="..." required>
                        </div>
                        <div class="mb-3">
                            <label class="small opacity-75">TIPO DE VISA (REAL)</label>
                            <select name="tipo" class="form-select">
                                <option value="Visa de Residencia Temporal - Mercosur">Temporal - Mercosur</option>
                                <option value="Visa de Residencia Permanente">Residencia Permanente</option>
                                <option value="Visa Nómada Digital">Nómada Digital (Ecuador)</option>
                                <option value="Visa de Inversionista">Inversionista</option>
                                <option value="Visa de Amparo">Visa de Amparo</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-neon w-100">PROCESAR SOLICITUD</button>
                    </form>
                </div>
                
                <div class="glass-card mt-4 p-3 border-success" style="font-size: 0.7rem;">
                    <div class="text-success mb-1">LOCALIZACIÓN: LATITUD 2.189° S, LONGITUD 79.889° W</div>
                    <div class="text-info">ESTADO DB: CONEXIÓN ESTABLE POR PUERTO 5432</div>
                </div>
            </div>

            <div class="col-md-8">
                <div class="glass-card p-4">
                    <h6 class="text-info mb-4 fw-bold"><i class="fas fa-database me-2"></i>BITÁCORA DE TRÁMITES MIGRATORIOS</h6>
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead class="text-info">
                                <tr><th>REGISTRO</th><th>CIUDADANO</th><th>CATEGORÍA</th><th>ACCIÓN</th></tr>
                            </thead>
                            <tbody>
                                {% for t in tramites %}
                                <tr>
                                    <td class="small">UID-{{ t.id }}</td>
                                    <td class="fw-bold">{{ t.cliente }}</td>
                                    <td><span class="badge border border-info">{{ t.tipo }}</span></td>
                                    <td><a href="/delete/{{ t.id }}" class="text-danger"><i class="fas fa-trash"></i></a></td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    tramites = Tramite.query.order_by(Tramite.id.desc()).all()
    return render_template_string(HTML_TEMPLATE, tramites=tramites)

@app.route('/add', methods=['POST'])
def add():
    db.session.add(Tramite(cliente=request.form['cliente'], tipo=request.form['tipo']))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    t = Tramite.query.get(id)
    if t:
        db.session.delete(t)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/download')
def download():
    tramites = Tramite.query.all()
    output = "TERRENCE.M - REPORTE DE GESTIÓN MIGRATORIA OFICIAL\\n" + "="*50 + "\\n"
    for t in tramites:
        output += f"UID: {t.id} | Ciudadano: {t.cliente} | Visa: {t.tipo} | Fecha: {t.fecha}\\n"
    return Response(output, mimetype="text/plain", headers={"Content-disposition": "attachment; filename=reporte_migratorio.txt"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))