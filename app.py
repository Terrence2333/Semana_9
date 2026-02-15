from flask import Flask, render_template

app = Flask(__name__)

# 1. RUTA PRINCIPAL (/)
# Muestra el nombre del sistema y el propósito del negocio
@app.route('/')
def home():
    return """
    <h1>Sistema de Gestión de Extranjería - Asesoría Kandy Vera</h1>
    <p>Propósito: Gestión integral de visas, residencias y trámites legales para extranjeros.</p>
    <hr>
    <p>Use la ruta <b>/tramite/nombre_del_tramite</b> para consultar estados.</p>
    """

# 2. RUTA DINÁMICA (/tramite/<tipo_tramite>)
# Devuelve un mensaje coherente y adaptado al negocio
@app.route('/tramite/<tipo_tramite>')
def tramite(tipo_tramite):
    # El mensaje es coherente con el tipo de trámite ingresado
    return f"<h1>Trámite: {tipo_tramite.capitalize()}</h1><p>Bienvenido. Su solicitud de {tipo_tramite} está siendo procesada exitosamente por nuestro equipo legal.</p>"

if __name__ == '__main__':
    app.run(debug=True)