"""Pasos de la consola que ya revisamos y tienen que seguir saliendo igual."""

import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

PASOS = [
    ["init"],
    ["registrar", "1001", "certificado", "alta", "Constancia de examen", "2026-06-01"],
    ["registrar", "1002", "cambio_comision", "media", "Cambio a la comision B", "2026-06-01"],
    ["registrar", "1003", "equivalencia", "baja", "Equivalencia de bases de datos", "2026-06-01"],
    ["registrar", "1003", "reclamo_nota", "alta", "Revision del parcial", "2026-06-01"],
    ["asignar", "4", "R1"],
    ["asignar", "4", "R2"],
    ["estado", "4", "en_proceso"],
    ["estado", "4", "resuelta"],
    ["estado", "7", "resuelta"],
    ["estado", "3", "rechazada"],
    ["asignar", "7", "R3"],
    ["estado", "7", "en_proceso"],
    ["estado", "7", "pendiente"],
    ["buscar", "estado=pendiente"],
    ["buscar", "prioridad=alta", "legajo=1001"],
    ["buscar", "estado=en_proceso", "tipo=equivalencia"],
    ["buscar", "estado=pendiente", "prioridad=alta"],
    ["reporte"],
    ["reporte", "csv"],
    ["reporte", "pdf"],
    ["registrar", "9999", "certificado", "alta", "Nadie", "2026-06-01"],
    ["registrar", "1001", "foo", "alta", "Tipo malo", "2026-06-01"],
    ["registrar", "1001", "certificado", "urgente", "Prioridad mala", "2026-06-01"],
    ["registrar", "1001", "certificado", "alta", "   ", "2026-06-01"],
    ["asignar", "1", "R1"],
    ["zzz"],
]


def correr(cwd, args):
    entorno = os.environ.copy()
    entorno["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, str(RAIZ / "app.py"), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=entorno,
    )


def transcripcion(cwd):
    partes = []
    for paso in PASOS:
        resultado = correr(cwd, paso)
        partes.append("$ python app.py " + " ".join(paso))
        salida = (resultado.stdout or "").replace("\r\n", "\n")
        if salida and not salida.endswith("\n"):
            salida += "\n"
        partes.append(salida.rstrip("\n"))
        error = (resultado.stderr or "").replace("\r\n", "\n").strip()
        if error:
            partes.append(error)
        partes.append("exit: " + str(resultado.returncode))
        partes.append("")
    return "\n".join(partes).rstrip() + "\n"
