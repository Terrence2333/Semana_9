import os
import io
from flask import Flask, render_template_string, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_terrence_m_2026'

# Base de Datos
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
    <title>Terrence.m | Cyber-Legal</title>
    <style>
        body { background: #0a0b10; color: #00d2ff; font-family: 'Courier New', monospace; }
        .glass-card { background: rgba(0, 210, 255, 0.05); border: 1px solid #00d2ff; border-radius: 15px; box-shadow: 0 0 20px rgba(0, 210, 255, 0.2); }
        .btn-neon { border: 2px solid #00d2ff; color: #00d2ff; background: transparent; transition: 0.3s; font-weight: bold; }
        .btn-neon:hover { background: #00d2ff; color: #000; box-shadow: 0 0 40px #00d2ff; }
        .table { color: #fff; }
        input, select { background: transparent !important; color: white !important; border: 1px solid #00d2ff !important; }
    </style>
</head>
<body class="p-4">
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-5 border-bottom pb-3">
            <h1 class="m-0"><i class="fas fa-atom"></i> TERRENCE.M</h1>
            <a href="/download" class="btn btn-neon"><i class="fas fa-file-export me-2"></i>DESCARGAR REPORTE .TXT</a>
        </div>
        
        <div class="row g-4">
            <div class="col-md-4">
                <div class="glass-card p-4">
                    <h5 class="text-info mb-4">INGRESAR PROTOCOLO</h5>
                    <form action="/add" method="POST">
                        <input type="text" name="cliente" class="form-control mb-3" placeholder="Nombre del Solicitante" required>
                        <select name="tipo" class="form-select mb-3">
                            <option value="Visa Galáctica">Visa Galáctica</option>
                            <option value="Residencia Cyber">Residencia Cyber</option>
                            <option value="Asesoría Legal AI">Asesoría Legal AI</option>
                        </select>
                        <button type="submit" class="btn btn-neon w-100">SINCRONIZAR DATOS</button>
                    </form>
                </div>
            </div>
            <div class="col-md-8">
                <div class="glass-card p-4">
                    <h5 class="text-info mb-4">BASE DE DATOS EN TIEMPO REAL</h5>
                    <div class="table-responsive">
                        <table class="table table-borderless">
                            <thead class="border-bottom border-info text-info">
                                <tr><th>ID</th><th>CLIENTE</th><th>SERVICIO</th><th>ACCIÓN</th></tr>
                            </thead>
                            <tbody>
                                {% for t in tramites %}
                                <tr>
                                    <td class="opacity-50">#{{ t.id }}</td>
                                    <td>{{ t.cliente }}</td>
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
    output = "SISTEMA TERRENCE.M - REPORTE DE GESTIÓN\\n" + "="*40 + "\\n"
    for t in tramites:
        output += f"[{t.fecha.strftime('%Y-%m-%d %H:%M')}] ID: {t.id} | Cliente: {t.cliente} | Trámite: {t.tipo}\\n"
    return Response(output, mimetype="text/plain", headers={"Content-disposition": "attachment; filename=reporte_terrence_m.txt"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))