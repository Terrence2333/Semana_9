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
        body { 
            background: linear-gradient(rgba(2, 4, 6, 0.88), rgba(2, 4, 6, 0.88)), 
                        url('https://images.unsplash.com/photo-1503221043305-f7498f8b7888?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80'); 
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #00d2ff; 
            font-family: 'Courier New', monospace; 
            overflow-x: hidden; 
        }
        .cyber-panel { 
            background: rgba(0, 210, 255, 0.05); 
            backdrop-filter: blur(10px);
            border: 1px solid #00d2ff; 
            border-radius: 5px; 
            padding: 20px; 
            box-shadow: inset 0 0 15px rgba(0,210,255,0.1); 
        }
        .header-main { border-bottom: 2px solid #00d2ff; margin-bottom: 30px; padding-bottom: 10px; }
        .btn-cyber { border: 1px solid #00d2ff; color: #00d2ff; background: transparent; text-transform: uppercase; font-weight: bold; transition: 0.3s; }
        .btn-cyber:hover { background: #00d2ff; color: #000; box-shadow: 0 0 20px #00d2ff; }
        input, select { background: rgba(0, 0, 0, 0.7) !important; color: #00d2ff !important; border: 1px solid #333 !important; border-bottom: 1px solid #00d2ff !important; }
        .progress { height: 4px; background: #081015; margin-top: 8px; border-radius: 0; }
        .progress-bar { background: #00d2ff; box-shadow: 0 0 10px #00d2ff; }
        .link-exp { color: #00d2ff; text-decoration: none; font-weight: bold; }
        .link-exp:hover { text-shadow: 0 0 10px #00d2ff; color: #fff; }
        
        /* Estilo Redes Sociales */
        .social-box a {
            color: #00d2ff;
            font-size: 1.5rem;
            margin: 0 10px;
            transition: 0.4s;
            text-shadow: 0 0 5px rgba(0,210,255,0.5);
        }
        .social-box a:hover {
            color: #fff;
            transform: translateY(-3px);
            text-shadow: 0 0 15px #00d2ff;
        }
    </style>
</head>
<body class="p-4">
    <div class="container-fluid">
        <div class="header-main d-flex justify-content-between align-items-center">
            <div>
                <h1 class="m-0 fw-bold"><i class="fas fa-globe-americas"></i> TERRENCE.M</h1>
                <small class="text-success"><i class="fas fa-shield-alt"></i> SISTEMA DE GESTIÓN MIGRATORIA // v4.2</small>
            </div>
            <a href="/download" class="btn btn-cyber btn-sm"><i class="fas fa-file-pdf"></i> GENERAR REPORTE</a>
        </div>

        <div class="row g-4">
            <div class="col-md-3">
                <div class="cyber-panel mb-4">
                    <h6 class="mb-4 text-info fw-bold border-bottom border-info pb-2">NUEVO EXPEDIENTE</h6>
                    <form action="/add" method="POST">
                        <div class="mb-3">
                            <label class="small opacity-75">CIUDADANO</label>
                            <input type="text" name="cliente" class="form-control" placeholder="..." required>
                        </div>
                        <div class="mb-4">
                            <label class="small opacity-75">TIPO DE SOLICITUD</label>
                            <select name="tipo" class="form-select">
                                <option value="Visa Mercosur">Temporal - Mercosur</option>
                                <option value="Visa Nomada Digital">Nómada Digital (EC)</option>
                                <option value="Residencia Permanente">Residencia Permanente</option>
                                <option value="Inversionista">Inversionista G1</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-cyber w-100">REGISTRAR TRÁMITE</button>
                    </form>
                </div>

                <div class="cyber-panel mb-4 text-center">
                    <h6 class="small fw-bold text-info mb-3">CANALES DE ENLACE</h6>
                    <div class="social-box">
                        <a href="https://facebook.com/tu_perfil" target="_blank"><i class="fab fa-facebook"></i></a>
                        <a href="https://instagram.com/tu_perfil" target="_blank"><i class="fab fa-instagram"></i></a>
                        <a href="https://wa.me/tu_numero" target="_blank"><i class="fab fa-whatsapp"></i></a>
                        <a href="https://tiktok.com/@tu_perfil" target="_blank"><i class="fab fa-tiktok"></i></a>
                    </div>
                </div>

                <div class="cyber-panel p-3 text-center">
                    <div class="small opacity-75">REGISTROS TOTALES</div>
                    <h2 class="text-center m-0">{{ tramites|length }}</h2>
                </div>
            </div>

            <div class="col-md-9">
                <div class="cyber-panel">
                    <div class="d-flex justify-content-between mb-3 align-items-center">
                        <h6 class="m-0 text-info fw-bold"><i class="fas fa-stream"></i> BITÁCORA DE CONTROL</h6>
                        <input type="text" id="busqueda" class="form-control w-25 form-control-sm" placeholder="Filtrar datos...">
                    </div>
                    <div class="table-responsive">
                        <table class="table table-dark table-hover" id="tabla">
                            <thead>
                                <tr class="text-info">
                                    <th>ID</th>
                                    <th>CIUDADANO</th>
                                    <th>VISA</th>
                                    <th>ESTADO</th>
                                    <th>ACCIÓN</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for t in tramites %}
                                <tr>
                                    <td class="small opacity-50">#{{ t.id }}</td>
                                    <td><a href="/expediente/{{ t.cliente }}" class="link-exp">{{ t.cliente }}</a></td>
                                    <td><span class="badge border border-info">{{ t.tipo }}</span></td>
                                    <td style="width: 150px;">
                                        <div class="progress"><div class="progress-bar" style="width: 75%;"></div></div>
                                        <small style="font-size: 10px; color: #00ff00;">Sincronizado</small>
                                    </td>
                                    <td><a href="/delete/{{ t.id }}" class="text-danger"><i class="fas fa-trash-alt"></i></a></td>
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
    output = "REPORTE TERRENCE.M\\n"
    for t in tramites:
        output += f"ID: {t.id} - {t.cliente} - {t.tipo}\\n"
    return Response(output, mimetype="text/plain", headers={"Content-disposition": "attachment; filename=reporte.txt"})

@app.route('/expediente/<cliente>')
def expediente(cliente):
    return f'''
    <body style="background: #020406; color: #00d2ff; font-family: monospace; display: flex; align-items: center; justify-content: center; height: 100vh;">
        <div style="border: 2px solid #00d2ff; padding: 40px; text-align: center; background: rgba(0,0,0,0.8);">
            <h1>GESTIÓN PARA: {cliente}</h1>
            <p>ESTADO: <span style="color: #00ff00;">PROTOCOLO ACTIVO</span></p>
            <br><a href="/" style="color: #00d2ff; text-decoration: none; border: 1px solid #00d2ff; padding: 10px;">[ VOLVER ]</a>
        </div>
    </body>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    

