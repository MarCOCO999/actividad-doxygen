"""
Pruebas unitarias para la aplicación Flask.
"""
from app import app


def test_hello_con_nombre():
    """Verifica que el endpoint /hello salude con el nombre recibido."""
    client = app.test_client()
    respuesta = client.get('/hello?name=Marco')
    assert respuesta.status_code == 200
    assert respuesta.data.decode() == "Hello, Marco!"


def test_hello_sin_nombre():
    """Verifica que el endpoint responda aunque no se envíe nombre."""
    client = app.test_client()
    respuesta = client.get('/hello')
    assert respuesta.status_code == 200
