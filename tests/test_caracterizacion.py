import json
from pathlib import Path

from escenario import correr, transcripcion

RAIZ = Path(__file__).resolve().parents[1]
GOLDEN = Path(__file__).resolve().parent / "golden"


def _texto(path):
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def test_la_consola_conserva_la_salida_que_ya_revisamos(tmp_path):
    obtenido = transcripcion(tmp_path)
    datos = _texto(tmp_path / "datos.json")
    assert obtenido == _texto(GOLDEN / "salida_esperada.txt")
    assert json.loads(datos) == json.loads(_texto(GOLDEN / "datos_esperados.json"))
    assert datos == _texto(GOLDEN / "datos_esperados.json")


def test_init_parte_de_una_carpeta_vacia(tmp_path):
    resultado = correr(tmp_path, ["init"])
    assert resultado.returncode == 0
    assert "Listo: cargamos los datos de ejemplo" in resultado.stdout
    guardado = json.loads((tmp_path / "datos.json").read_text(encoding="utf-8"))
    assert len(guardado["estudiantes"]) == 3
    assert len(guardado["solicitudes"]) == 3
