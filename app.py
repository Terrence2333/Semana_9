import os
from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_terrence_m'

# Configuración de Base de Datos
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'extranjeria.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tramite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(50), default='En Proceso')
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <title>Terrence.m | Panel Profesional</title>
    <style>
        .navbar { background: #002d5a; }
        .btn-primary { background: #0056b3; border: none; }
        .card { border-radius: 15px; border: none; }
        .table-dark { background: #002d5a; }
    </style>
</head>
<body class="bg-light">
    <nav class="navbar navbar-dark shadow">
        <div class="container">
            <a class="navbar-brand" href="#"><i class="fas fa-balance-scale me-2"></i><strong>Terrence.m</strong> - Consultoría de Extranjería</a>
        </div>
    </nav>

    <div class="container mt-5">
        <div class="row g-4">
            <div class="col-lg-4">
                <div class="card shadow p-4">
                    <h5 class="text-primary mb-4"><i class="fas fa-user-plus me-2"></i>Nuevo Registro</h5>
                    <form action="/add" method="POST">
                        <div class="mb-3">
                            <label class="form-label text-secondary">Nombre del Solicitante</label>
                            <input type="text" name="cliente" class="form-control form-control-lg" placeholder="Nombre completo" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label text-secondary">Servicio Requerido</label>
                            <select name="tipo" class="form-select form-control-lg">
                                <option value="Visa de Residencia">Visa de Residencia</option>
                                <option value="Asesoría Migratoria">Asesoría Migratoria</option>
                                <option value="Renovación de Permiso">Renovación de Permiso</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary btn-lg w-100 shadow-sm">Registrar Trámite</button>
                    </form>
                </div>
            </div>

            <div class="col-lg-8">
                <div class="card shadow p-4">
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h5 class="m-0"><i class="fas fa-list-ul me-2"></i>Panel de Control de Trámites</h5>
                        <span class="badge bg-success">Sistema Conectado</span>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-hover align-middle">
                            <thead class="table-dark">
                                <tr>
                                    <th>Servicio</th>
                                    <th>Cliente</th>
                                    <th>Estado</th>
                                    <th>Prioridad</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for t in tramites %}
                                <tr>
                                    <td><strong>{{ t.tipo }}</strong></td>
                                    <td>{{ t.cliente }}</td>
                                    <td><span class="badge rounded-pill bg-info text-dark">En Revisión</span></td>
                                    <td><span class="text-danger"><i class="fas fa-circle me-1"></i> Alta</span></td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="mt-5 py-4 bg-white text-center text-secondary border-top">
        <small>&copy; 2026 Terrence.m | Servicios Legales de Extranjería | <i class="fas fa-shield-alt"></i> Datos Encriptados</small>
    </footer>
</body>
</html>
"""

@app.route('/')
def index():
    tramites = Tramite.query.order_by(Tramite.id.desc()).all()
    return render_template_string(HTML_TEMPLATE, tramites=tramites)

@app.route('/add', methods=['POST'])
def add():
    nuevo = Tramite(cliente=request.form['cliente'], tipo=request.form['tipo'])
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
