import os
from flask import Flask, render_template_string, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_terrence_2026'

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
    <title>Terrence.m | Intelligence Portal</title>
    <style>
        body { background: #030507; color: #00d2ff; font-family: 'Courier New', monospace; }
        .glass { background: rgba(0, 210, 255, 0.03); border: 1px solid #00d2ff; border-radius: 12px; padding: 25px; box-shadow: 0 0 25px rgba(0,210,255,0.1); transition: 0.3s; }
        .glass:hover { box-shadow: 0 0 35px rgba(0,210,255,0.2); }
        .btn-neon { border: 1px solid #00d2ff; color: #00d2ff; background: transparent; font-weight: bold; letter-spacing: 1px; }
        .btn-neon:hover { background: #00d2ff; color: #000; box-shadow: 0 0 30px #00d2ff; transform: scale(1.03); }
        input, select { background: #000 !important; color: #00d2ff !important; border: 1px solid #00d2ff !important; font-size: 0.9rem; }
        .table { color: #fff; border-color: #00d2ff; vertical-align: middle; }
        .link-expediente { color: #00d2ff; text-decoration: none; border-bottom: 1px dashed #00d2ff; font-weight: bold; }
        .link-expediente:hover { color: #fff; border-bottom: 1px solid #fff; }
        .badge-status { font-size: 0.65rem; background: rgba(0, 255, 0, 0.1); color: #00ff00; border: 1px solid #00ff00; }
        .progress { height: 6px; background: #0a0b10; border: 1px solid #00d2ff; border-radius: 10px; margin-top: 5px; }
        .progress-bar { background: #00d2ff; box-shadow: 0 0 10px #00d2ff; }
        .scan-line { width: 100%; height: 2px; background: #00d2ff; position: absolute; opacity: 0.2; animation: scan 3s infinite linear; }
        @keyframes scan { from { top: 0; } to { top: 100%; } }
    </style>
</head>
<body class="p-4">
    <div class="container">
        <div class="d-flex justify-content-between align-items-end mb-4 border-bottom border-info pb-3">
            <div>
                <h1 class="m-0 fw-bold"><i class="fas fa-brain"></i> TERRENCE.M <small style="font-size: 0.5em; opacity: 0.6;">CORE v3.0</small></h1>
                <div class="d-flex gap-3 small mt-1">
                    <span class="text-success"><i class="fas fa-circle" style="font-size: 8px;"></i> SISTEMA ONLINE</span>
                    <span class="text-info"><i class="fas fa-satellite"></i> SAT: GUAYAQUIL-EQ</span>
                </div>
            </div>
            <div class="text-end">
                <a href="/download" class="btn btn-neon btn-sm mb-2"><i class="fas fa-file-export me-1"></i> EXPORTAR DATA TXT</a>
            </div>
        </div>

        <div class="row g-4">
            <div class="col-md-4">
                <div class="glass mb-4">
                    <h6 class="text-info mb-3"><i class="fas fa-plus-circle me-2"></i>ALTA DE EXPEDIENTE</h6>
                    <form action="/add" method="POST">
                        <label class="small opacity-50">CIUDADANO</label>
                        <input type="text" name="cliente" class="form-control mb-3" placeholder="Nombre completo..." required>
                        <label class="small opacity-50">TIPO DE VISA SOLICITADA</label>
                        <select name="tipo" class="form-select mb-3">
                            <option value="Visa Mercosur">Visa Mercosur</option>
                            <option value="Visa Nomada Digital">Visa Nomada Digital (Ecuador)</option>
                            <option value="Residencia Permanente">Residencia Permanente</option>
                            <option value="Visa de Inversionista">Visa de Inversionista</option>
                        </select>
                        <button type="submit" class="btn btn-neon w-100">INICIAR PROCESO</button>
                    </form>
                </div>

                <div class="glass border-success p-3">
                    <h6 class="text-success fw-bold small"><i class="fas fa-chart-line me-2"></i>ANÁLISIS DE CARGA</h6>
                    <div class="d-flex justify-content-between small">
                        <span>Tramites Hoy:</span>
                        <span class="fw-bold">0{{ tramites|length }}</span>
                    </div>
                    <div class="progress mt-2">
                        <div class="progress-bar w-75" role="progressbar"></div>
                    </div>
                    <p class="text-center opacity-50 mt-2 mb-0" style="font-size: 0.6rem;">LATENCIA DE BASE DE DATOS: 14ms</p>
                </div>
            </div>

            <div class="col-md-8">
                <div class="glass position-relative overflow-hidden">
                    <div class="scan-line"></div>
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h6 class="text-info m-0 fw-bold"><i class="fas fa-database me-2"></i>EXPEDIENTES EN NUBE</h6>
                        <input type="text" id="busqueda" class="form-control w-50" placeholder="Filtrar por nombre...">
                    </div>
                    
                    <div class="table-responsive">
                        <table class="table table-dark table-hover" id="tablaTramites">
                            <thead class="text-info border-bottom border-info">
                                <tr>
                                    <th>#UID</th>
                                    <th>SOLICITANTE</th>
                                    <th>CATEGORÍA</th>
                                    <th>PROGRESO</th>
                                    <th>ACCIONES</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for t in tramites %}
                                <tr>
                                    <td class="small opacity-50">{{ t.id }}</td>
                                    <td>
                                        <a href="/expediente/{{ t.cliente }}" class="link-expediente">
                                            {{ t.cliente }}
                                        </a>
                                        <br><span class="badge badge-status">VERIFICADO</span>
                                    </td>
                                    <td><span class="small">{{ t.tipo }}</span></td>
                                    <td style="width: 120px;">
                                        <div class="progress">
                                            <div class="progress-bar" style="width: 45%;"></div>
                                        </div>
                                        <span style="font-size: 0.6rem; color: #00ff00;">Fase de Revisión</span>
                                    </td>
                                    <td>
                                        <a href="/delete/{{ t.id }}" class="text-danger"><i class="fas fa-trash-alt"></i></a>
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

    <script>
        document.getElementById('busqueda').addEventListener('keyup', function() {
            let filtro = this.value.toUpperCase();
            let filas = document.getElementById('tablaTramites').getElementsByTagName('tr');
            for (let i = 1; i < filas.length; i++) {
                let texto = filas[i].textContent || filas[i].innerText;
                filas[i].style.display = texto.toUpperCase().indexOf(filtro) > -1 ? "" : "none";
            }
        });
    </script>
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
    output = "TERRENCE.M INTELLIGENCE REPORT\\n" + "="*40 + "\\n"
    for t in tramites:
        output += f"UID: {t.id} | Cliente: {t.cliente} | Visa: {t.tipo} | Registro: {t.fecha}\\n"
    return Response(output, mimetype="text/plain", headers={"Content-disposition": "attachment; filename=reporte_terrence_m.txt"})

@app.route('/expediente/<cliente>')
def expediente(cliente):
    return f'''
    <body style="background: #030507; color: #00d2ff; font-family: monospace; padding: 50px;">
        <div style="border: 2px solid #00d2ff; padding: 40px; border-radius: 15px; max-width: 700px; margin: auto; box-shadow: 0 0 40px rgba(0,210,255,0.3);">
            <h1 style="text-transform: uppercase;"><i class="fas fa-user-check"></i> EXPEDIENTE: {cliente}</h1>
            <hr style="border-color: #00d2ff;">
            <div style="background: rgba(0,210,255,0.05); padding: 20px; border-radius: 10px;">
                <p><strong>ESTADO GLOBAL:</strong> <span style="color: #00ff00;">EN TRÁMITE DIPLOMÁTICO</span></p>
                <p><strong>UBICACIÓN:</strong> CANCILLERÍA - SEDE CENTRAL</p>
                <p><strong>NIVEL DE ACCESO:</strong> NIVEL 4 (CONFIDENCIAL)</p>
            </div>
            <br>
            <a href="/" style="color: #00d2ff; text-decoration: none; border: 1px solid #00d2ff; padding: 12px 25px; border-radius: 5px;">[ RETORNAR AL NÚCLEO ]</a>
        </div>
    </body>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)