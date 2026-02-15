import os
from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_terrence_m'

# CONFIGURACIÓN DE BASE DE DATOS
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'extranjeria.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELO DE DATOS
class Tramite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    tipo_tramite = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# PLANTILLA ÚNICA (HTML + BOOTSTRAP)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>Terrence.m | Gestión de Extranjería</title>
</head>
<body class="bg-light">
    <nav class="navbar navbar-dark bg-dark shadow-sm">
        <div class="container">
            <a class="navbar-brand" href="#"><strong>Terrence.m</strong> - Consultoría Legal</a>
        </div>
    </nav>

    <div class="container mt-5">
        <div class="row">
            <div class="col-md-4">
                <div class="card shadow-sm p-4">
                    <h5 class="text-primary mb-3">Nuevo Trámite</h5>
                    <form action="/agregar" method="POST">
                        <div class="mb-3">
                            <label class="form-label">Nombre del Cliente</label>
                            <input type="text" name="cliente" class="form-control" placeholder="Ej. Juan Pérez" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Tipo de Trámite</label>
                            <select name="tipo" class="form-select">
                                <option value="Visa de Residencia">Visa de Residencia</option>
                                <option value="Naturalización">Naturalización</option>
                                <option value="Asesoría Legal">Asesoría Legal</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Registrar en Sistema</button>
                    </form>
                </div>
            </div>

            <div class="col-md-8">
                <div class="card shadow-sm p-4">
                    <h5 class="mb-3">Historial de Gestiones</h5>
                    <table class="table table-striped">
                        <thead class="table-primary">
                            <tr>
                                <th>ID</th>
                                <th>Cliente</th>
                                <th>Trámite</th>
                                <th>Fecha</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for t in tramites %}
                            <tr>
                                <td>{{ t.id }}</td>
                                <td>{{ t.cliente }}</td>
                                <td><span class="badge bg-info text-dark">{{ t.tipo_tramite }}</span></td>
                                <td>{{ t.fecha_creacion.strftime('%d/%m/%Y') }}</td>
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
    tramites = Tramite.query.order_by(Tramite.id.desc()).all()
    return render_template_string(HTML_TEMPLATE, tramites=tramites)

@app.route('/agregar', method=['POST'])
def agregar():
    nuevo_tramite = Tramite(
        cliente=request.form['cliente'],
        tipo_tramite=request.form['tipo']
    )
    db.session.add(nuevo_tramite)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

