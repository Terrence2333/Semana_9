import os
from flask import Flask, render_template_string, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_terrence_2026'

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
<html>
<head>
    <meta charset="UTF-8">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <title>Terrence.m | Portal</title>
    <style>
        body { background: #05080a; color: #00d2ff; font-family: monospace; }
        .glass { background: rgba(0, 210, 255, 0.05); border: 1px solid #00d2ff; border-radius: 10px; padding: 20px; }
        .btn-neon { border: 1px solid #00d2ff; color: #00d2ff; background: transparent; transition: 0.3s; }
        .btn-neon:hover { background: #00d2ff; color: #000; box-shadow: 0 0 20px #00d2ff; }
        input, select { background: #000 !important; color: #00d2ff !important; border: 1px solid #00d2ff !important; }
        .status-scan { font-size: 0.8rem; color: #00ff00; }
    </style>
</head>
<body class="p-4">
    <div class="container">
        <div class="d-flex justify-content-between mb-4 border-bottom border-info pb-3">
            <div>
                <h1><i class="fas fa-microchip"></i> TERRENCE.M</h1>
                <span class="status-scan">SISTEMA DE VISADO REAL ACTIVO</span>
            </div>
            <a href="/download" class="btn btn-neon">DESCARGAR REPORTE</a>
        </div>
        <div class="row g-4">
            <div class="col-md-4">
                <div class="glass">
                    <h6>NUEVO TRÁMITE REAL</h6>
                    <form action="/add" method="POST">
                        <input type="text" name="cliente" class="form-control mb-3" placeholder="Nombre Ciudadano" required>
                        <select name="tipo" class="form-select mb-3">
                            <option value="Visa Mercosur">Visa Mercosur</option>
                            <option value="Visa Nomada Digital">Visa Nomada Digital</option>
                            <option value="Residencia Permanente">Residencia Permanente</option>
                        </select>
                        <button type="submit" class="btn btn-neon w-100">PROCESAR</button>
                    </form>
                </div>
            </div>
            <div class="col-md-8">
                <div class="glass">
                    <table class="table table-dark table-hover">
                        <thead><tr><th>ID</th><th>CLIENTE</th><th>VISA</th><th>BORRAR</th></tr></thead>
                        <tbody>
                            {% for t in tramites %}
                            <tr>
                                <td>#{{ t.id }}</td>
                                <td>{{ t.cliente }}</td>
                                <td>{{ t.tipo }}</td>
                                <td><a href="/delete/{{ t.id }}" class="text-danger"><i class="fas fa-trash"></i></a></td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    tramites = Tramite.query.all()
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
    output = "REPORTE TERRENCE.M\\n"
    for t in tramites:
        output += f"ID: {t.id} - {t.cliente} - {t.tipo}\\n"
    return Response(output, mimetype="text/plain", headers={"Content-disposition": "attachment; filename=reporte.txt"})

# NUEVA RUTA DE NEGOCIO PERSONALIZADA
@app.route('/expediente/<cliente>')
def expediente(cliente):
    return f'''
    <body style="background: #05080a; color: #00d2ff; font-family: monospace; padding: 50px;">
        <div style="border: 1px solid #00d2ff; padding: 20px; border-radius: 10px;">
            <h2>CONSULTA DE EXPEDIENTE: {cliente}</h2>
            <hr style="border-color: #00d2ff;">
            <p>ESTADO: <span style="color: #00ff00;">VALIDANDO DOCUMENTACIÓN EN CANCILLERÍA</span></p>
            <a href="/" style="color: #00d2ff; text-decoration: none;">[ VOLVER AL PANEL ]</a>
        </div>
    </body>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)