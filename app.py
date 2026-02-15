import os
from flask import Flask, render_template_string, request, redirect, url_for
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
    estado = db.Column(db.String(50), default='Procesando...')
    prioridad = db.Column(db.String(20), default='Normal')
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# DISEÑO FUTURISTA (CSS INTERNO PARA ELEGANCIA)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <title>Terrence.m | Cyber-Legal Portal</title>
    <style>
        body { 
            background: radial-gradient(circle at top, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e945e3; font-family: 'Segoe UI', sans-serif; min-height: 100vh;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8); transition: 0.3s;
        }
        .navbar { background: rgba(15, 52, 96, 0.8); border-bottom: 2px solid #00d2ff; }
        .btn-neon {
            background: transparent; border: 2px solid #00d2ff; color: #00d2ff;
            font-weight: bold; text-transform: uppercase; letter-spacing: 2px;
            box-shadow: 0 0 10px #00d2ff; transition: 0.5s;
        }
        .btn-neon:hover { background: #00d2ff; color: #000; box-shadow: 0 0 30px #00d2ff; }
        .table { color: #fff; }
        .badge-neon { border: 1px solid #00d2ff; color: #00d2ff; background: rgba(0, 210, 255, 0.1); }
        input, select { 
            background: rgba(255,255,255,0.1) !important; border: 1px solid #00d2ff !important; color: white !important;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark sticky-top shadow">
        <div class="container">
            <a class="navbar-brand d-flex align-items-center" href="#">
                <i class="fas fa-microchip me-3 text-info"></i>
                <span class="fs-3 fw-bold">TERRENCE.M</span>
            </a>
            <span class="badge rounded-pill bg-success shadow-sm">CORE ONLINE</span>
        </div>
    </nav>

    <div class="container mt-5">
        <div class="row g-4">
            <div class="col-lg-4">
                <div class="glass-card p-4 h-100">
                    <h4 class="text-info mb-4"><i class="fas fa-terminal me-2"></i>Inyectar Trámite</h4>
                    <form action="/add" method="POST">
                        <div class="mb-3 text-start">
                            <label class="form-label small text-info">Identificación del Cliente</label>
                            <input type="text" name="cliente" class="form-control" placeholder="Nombre completo..." required>
                        </div>
                        <div class="mb-3 text-start">
                            <label class="form-label small text-info">Protocolo de Servicio</label>
                            <select name="tipo" class="form-select">
                                <option value="Ciudadanía Galáctica">Ciudadanía Galáctica</option>
                                <option value="Visa de Residencia">Visa de Residencia</option>
                                <option value="Asesoría Cyber-Legal">Asesoría Cyber-Legal</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-neon w-100 mt-3">Ejecutar Comando</button>
                    </form>
                </div>
            </div>

            <div class="col-lg-8">
                <div class="glass-card p-4">
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h4 class="text-info m-0"><i class="fas fa-database me-2"></i>Bitácora de Eventos</h4>
                        <i class="fas fa-sync fa-spin text-secondary"></i>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-borderless align-middle">
                            <thead class="text-info border-bottom">
                                <tr>
                                    <th>ID</th><th>Cliente</th><th>Servicio</th><th>Acción</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for t in tramites %}
                                <tr>
                                    <td class="small opacity-50">#{{ t.id }}</td>
                                    <td><strong>{{ t.cliente }}</strong></td>
                                    <td><span class="badge badge-neon">{{ t.tipo }}</span></td>
                                    <td>
                                        <a href="/delete/{{ t.id }}" class="btn btn-sm btn-outline-danger shadow-sm">
                                            <i class="fas fa-trash-alt"></i>
                                        </a>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="text-center mt-5 mb-4 text-info opacity-50">
        <small>System: Terrence.m v2.0-Alpha | Lex-Corp Intergaláctica &copy; 2026</small>
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

@app.route('/delete/<int:id>')
def delete(id):
    tramite = Tramite.query.get(id)
    if tramite:
        db.session.delete(tramite)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
