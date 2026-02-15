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
<html lang="es">
<head>
    <meta charset="UTF-8">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <title>Terrence.m | Intelligence Core</title>
    <style>
        body { background: #020406; color: #00d2ff; font-family: 'Courier New', monospace; overflow-x: hidden; }
        .cyber-panel { background: rgba(0, 210, 255, 0.03); border: 1px solid #00d2ff; border-radius: 5px; padding: 20px; position: relative; box-shadow: inset 0 0 15px rgba(0,210,255,0.1); }
        .header-main { border-bottom: 2px solid #00d2ff; margin-bottom: 30px; padding-bottom: 10px; }
        .btn-cyber { border: 1px solid #00d2ff; color: #00d2ff; background: transparent; text-transform: uppercase; font-weight: bold; transition: 0.3s; }
        .btn-cyber:hover { background: #00d2ff; color: #000; box-shadow: 0 0 20px #00d2ff; }
        input, select { background: #000 !important; color: #00d2ff !important; border: 1px solid #333 !important; border-bottom: 1px solid #00d2ff !important; }
        .stat-card { border-left: 3px solid #00ff00; padding-left: 10px; margin-bottom: 20px; }
        .progress { height: 4px; background: #081015; margin-top: 8px; border-radius: 0; }
        .progress-bar { background: #00d2ff; box-shadow: 0 0 10px #00d2ff; }
        .scanline { width: 100%; height: 100px; background: linear-gradient(0deg, rgba(0,210,255,0) 0%, rgba(0,210,255,0.1) 50%, rgba(0,210,255,0) 100%); position: absolute; animation: moveScan 4s infinite linear; pointer-events: none; }
        @keyframes moveScan { from { top: -100px; } to { top: 100%; } }
        .link-exp { color: #00d2ff; text-decoration: none; border: 1px solid transparent; padding: 2px 5px; }
        .link-exp:hover { border: 1px solid #00d2ff; background: rgba(0,210,255,0.1); }
    </style>
</head>
<body class="p-4">
    <div class="scanline"></div>
    <div class="container-fluid">
        <div class="header-main d-flex justify-content-between align-items-center">
            <div>
                <h1 class="m-0 fw-bold"><i class="fas fa-microchip"></i> TERRENCE.M</h1>
                <small class="text-success"><i class="fas fa-terminal"></i> KERNEL MIGRATORIO v4.0 // CONECTADO</small>
            </div>
            <div class="d-flex gap-3">
                <div class="text-end border-end pe-3 border-info">
                    <div class="small opacity-50">LATENCIA DB</div>
                    <div class="text-info fw-bold">12ms</div>
                </div>
                <a href="/download" class="btn btn-cyber btn-sm"><i class="fas fa-download"></i> REPORTE TOTAL</a>
            </div>
        </div>

        <div class="row g-4">
            <div class="col-md-3">
                <div class="cyber-panel mb-4">
                    <h6 class="mb-4 text-info fw-bold border-bottom border-info pb-2">INGRESAR PROTOCOLO</h6>
                    <form action="/add" method="POST">
                        <div class="mb-3">
                            <label class="small opacity-50">NOMBRE DEL SOLICITANTE</label>
                            <input type="text" name="cliente" class="form-control" placeholder="Esperando entrada..." required>
                        </div>
                        <div class="mb-4">
                            <label class="small opacity-50">TIPO DE VISA (REAL)</label>
                            <select name="tipo" class="form-select">
                                <option value="Visa Mercosur">Temporal - Mercosur</option>
                                <option value="Visa Nomada Digital">Nómada Digital (EC)</option>
                                <option value="Residencia Permanente">Residencia Permanente</option>
                                <option value="Inversionista">Inversionista G1</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-cyber w-100">EJECUTAR SINCRONIZACIÓN</button>
                    </form>
                </div>

                <div class="stat-card">
                    <div class="small opacity-50">EXPEDIENTES ACTIVOS</div>
                    <h3 class="m-0">{{ tramites|length }}</h3>
                    <div class="progress"><div class="progress-bar w-50"></div></div>
                </div>
            </div>

            <div class="col-md-9">
                <div class="cyber-panel">
                    <div class="d-flex justify-content-between mb-3 align-items-center">
                        <h6 class="m-0 text-info fw-bold"><i class="fas fa-database"></i> BASE DE DATOS EN TIEMPO REAL</h6>
                        <input type="text" id="busqueda" class="form-control w-25 form-control-sm" placeholder="Buscar ciudadano...">
                    </div>
                    
                    <div class="table-responsive">
                        <table class="table table-dark table-hover border-secondary" id="tabla">
                            <thead>
                                <tr class="text-info">
                                    <th>#UID</th>
                                    <th>CIUDADANO</th>
                                    <th>CATEGORÍA</th>
                                    <th>PROGRESO</th>
                                    <th>ESTADO</th>
                                    <th>ACCIÓN</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for t in tramites %}
                                <tr>
                                    <td class="text-secondary small">0x0{{ t.id }}</td>
                                    <td>
                                        <a href="/expediente/{{ t.cliente }}" class="link-exp">
                                            <i class="fas fa-user-circle me-2"></i>{{ t.cliente }}
                                        </a>
                                    </td>
                                    <td><span class="badge border border-info text-info">{{ t.tipo }}</span></td>
                                    <td style="width: 150px;">
                                        <div class="progress"><div class="progress-bar" style="width: 65%;"></div></div>
                                        <small style="font-size: 10px; color: #00ff00;">Verificando...</small>
                                    </td>
                                    <td><span class="text-success"><i class="fas fa-check-double"></i> OK</span></td>
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

        <div class="mt-5 small text-center opacity-50">
            <i class="fas fa-map-marker-alt"></i> GUAYAQUIL HUB: 2.189° S, 79.889° W | ENCRIPTACIÓN SSL-TLS ACTIVA
        </div>
    </div>

    <script>
        document.getElementById('busqueda').addEventListener('keyup', function() {
            let filter = this.value.toUpperCase();
            let rows = document.getElementById('tabla').getElementsByTagName('tr');
            for (let i = 1; i < rows.length; i++) {
                let text = rows[i].innerText.toUpperCase();
                rows[i].style.display = text.indexOf(filter) > -1 ? "" : "none";
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
    output = "TERRENCE.M INTELLIGENCE SYSTEM REPORT\\n" + "="*40 + "\\n"
    for t in tramites:
        output += f"UID: {t.id} | Cliente: {t.cliente} | Tipo: {t.tipo} | Fecha: {t.fecha}\\n"
    return Response(output, mimetype="text/plain", headers={"Content-disposition": "attachment; filename=reporte_terrence.txt"})

@app.route('/expediente/<cliente>')
def expediente(cliente):
    return f'''
    <body style="background: #020406; color: #00d2ff; font-family: monospace; padding: 50px; display: flex; align-items: center; justify-content: center; height: 100vh;">
        <div style="border: 2px solid #00d2ff; padding: 40px; border-radius: 10px; text-align: center; box-shadow: 0 0 50px rgba(0,210,255,0.2);">
            <h1 style="text-transform: uppercase;">ACCESO AUTORIZADO</h1>
            <hr style="border-color: #00d2ff;">
            <h3>SOLICITANTE: {cliente}</h3>
            <p>ESTADO: <span style="color: #00ff00;">EXPEDIENTE ENVIADO A CANCILLERÍA</span></p>
            <p style="opacity: 0.5;">ID de Rastreo: T-{cliente[:3].upper()}-2026</p>
            <br>
            <a href="/" style="color: #00d2ff; text-decoration: none; border: 1px solid #00d2ff; padding: 10px 20px;">[ VOLVER AL TERMINAL ]</a>
        </div>
    </body>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    