from flask import Flask, request

app = Flask(__name__)


@app.route('/hello')
def hello():
    """
    Endpoint para saludar al usuario.

    Parámetros:
    name (str): Nombre del usuario.

    Retorna:
    str: Mensaje de saludo.
    """
    name = request.args.get('name')
    return f"Hello, {name}!"


if __name__ == '__main__':
    # host 0.0.0.0 para que la app sea accesible fuera del contenedor.
    # debug=False: el modo debug no debe usarse en un entorno desplegado.
    app.run(host='0.0.0.0', port=5000, debug=False)
