# Gestion de solicitudes academicas
# primera version: todo junto para poder usarla ya
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

ARCHIVO = "datos.json"

# estados: 0 pendiente, 1 en proceso, 2 resuelta, 3 rechazada
# prioridad: 1 alta, 2 media, 3 baja


class TipoSolicitud(str, Enum):
    CERTIFICADO = "certificado"
    CAMBIO_COMISION = "cambio_comision"
    EQUIVALENCIA = "equivalencia"
    RECLAMO_NOTA = "reclamo_nota"

    @property
    def area(self):
        return _AREA_POR_TIPO[self]


_AREA_POR_TIPO = {
    TipoSolicitud.CERTIFICADO: "Bedelia",
    TipoSolicitud.CAMBIO_COMISION: "Bedelia",
    TipoSolicitud.EQUIVALENCIA: "Departamento Academico",
    TipoSolicitud.RECLAMO_NOTA: "Docencia",
}


class Prioridad(str, Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"

    @property
    def codigo(self):
        return _CODIGO_POR_PRIORIDAD[self]

    @property
    def dias_vencimiento(self):
        return _DIAS_POR_PRIORIDAD[self]


_CODIGO_POR_PRIORIDAD = {
    Prioridad.ALTA: 1,
    Prioridad.MEDIA: 2,
    Prioridad.BAJA: 3,
}

_DIAS_POR_PRIORIDAD = {
    Prioridad.ALTA: 2,
    Prioridad.MEDIA: 5,
    Prioridad.BAJA: 10,
}


@dataclass(frozen=True)
class DatosRegistro:
    legajo: str
    tipo: str
    prioridad: str
    descripcion: str
    fecha: str | None = None


class Sistema:
    def __init__(self):
        self.d = {"estudiantes": [], "responsables": [], "solicitudes": []}
        try:
            f = open(ARCHIVO, "r", encoding="utf-8")
            self.d = json.load(f)
            f.close()
        except:
            pass

    def _guardar(self):
        with open(ARCHIVO, "w", encoding="utf-8") as archivo:
            json.dump(self.d, archivo, indent=2, ensure_ascii=False)

    def _buscar_solicitud(self, id_solicitud):
        for solicitud in self.d["solicitudes"]:
            if solicitud["id"] == int(id_solicitud):
                return solicitud
        return None

    def init(self):
        self.d = {
            "estudiantes": [
                {"legajo": "1001", "nombre": "Martina Ruiz", "email": "martina.ruiz@example.edu", "carrera": "TUP"},
                {"legajo": "1002", "nombre": "Lucas Pereyra", "email": "lucas.pereyra@example.edu", "carrera": "TUP"},
                {"legajo": "1003", "nombre": "Sofia Benitez", "email": "sofia.benitez@example.edu", "carrera": "TUPaD"},
            ],
            "responsables": [
                {"id": "R1", "nombre": "Elena Vargas", "area": "Bedelia"},
                {"id": "R2", "nombre": "Pablo Medina", "area": "Departamento Academico"},
                {"id": "R3", "nombre": "Nora Acosta", "area": "Docencia"},
            ],
            "solicitudes": [
                {
                    "id": 1,
                    "legajo": "1001",
                    "tipo": "certificado",
                    "prioridad": 2,
                    "descripcion": "Certificado de alumno regular",
                    "estado": 2,
                    "area": "Bedelia",
                    "responsable": "R1",
                    "fecha": "2026-03-01",
                    "vence": "2026-03-06",
                },
                {
                    "id": 2,
                    "legajo": "1002",
                    "tipo": "equivalencia",
                    "prioridad": 1,
                    "descripcion": "Equivalencia de Programacion I",
                    "estado": 1,
                    "area": "Departamento Academico",
                    "responsable": "R2",
                    "fecha": "2026-03-02",
                    "vence": "2020-03-04",
                },
                {
                    "id": 3,
                    "legajo": "1003",
                    "tipo": "reclamo_nota",
                    "prioridad": 3,
                    "descripcion": "Revision de nota del primer parcial",
                    "estado": 0,
                    "area": "Docencia",
                    "responsable": None,
                    "fecha": "2026-11-01",
                    "vence": "2099-01-20",
                },
            ],
        }
        self._guardar()
        print("Listo: cargamos los datos de ejemplo")
        return True

    def registrar(self, datos: DatosRegistro):
        legajo = datos.legajo
        tipo = datos.tipo
        prioridad = datos.prioridad
        descripcion = datos.descripcion
        fecha_str = datos.fecha
        est = None
        for e in self.d["estudiantes"]:
            if e["legajo"] == legajo:
                est = e
        if est == None:
            print("Error: el legajo " + legajo + " no existe")
            return -1
        try:
            tipo_solicitud = TipoSolicitud(tipo)
        except ValueError:
            print("Error: tipo de solicitud invalido: " + tipo)
            return -1
        area = tipo_solicitud.area
        try:
            prioridad_solicitud = Prioridad(prioridad)
        except ValueError:
            print("Error: prioridad invalida: " + prioridad)
            return -1
        p = prioridad_solicitud.codigo
        if descripcion == None or len(descripcion.strip()) == 0:
            print("Error: la descripcion es obligatoria")
            return -1
        if len(descripcion) > 200:
            print("Error: la descripcion supera los 200 caracteres")
            return -1
        if fecha_str == None:
            fecha = datetime.now()
        else:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        vence = fecha + timedelta(days=prioridad_solicitud.dias_vencimiento)
        nuevo_id = len(self.d["solicitudes"]) + 1
        s = {
            "id": nuevo_id,
            "legajo": legajo,
            "tipo": tipo,
            "prioridad": p,
            "descripcion": descripcion.strip(),
            "estado": 0,
            "area": area,
            "responsable": None,
            "fecha": fecha.strftime("%Y-%m-%d"),
            "vence": vence.strftime("%Y-%m-%d"),
        }
        # canal y observaciones por ahora no se usan
        self.d["solicitudes"].append(s)
        self._guardar()
        print(
            "Listo: solicitud #"
            + str(nuevo_id)
            + " registrada (area: "
            + area
            + ", vence: "
            + s["vence"]
            + ")"
        )
        return nuevo_id

    def cambiar_estado(self, id, nuevo):
        x = self._buscar_solicitud(id)
        if x == None:
            print("Error: no existe la solicitud #" + str(id))
            return False
        if nuevo == "pendiente":
            n = 0
        elif nuevo == "en_proceso":
            n = 1
        elif nuevo == "resuelta":
            n = 2
        elif nuevo == "rechazada":
            n = 3
        else:
            print("Error: estado invalido: " + nuevo)
            return False
        if x["estado"] == 2 or x["estado"] == 3:
            print("Error: la solicitud #" + str(id) + " ya esta cerrada")
            return False
        if x["estado"] == 0 and n == 2:
            print("Error: no se puede resolver una solicitud que no esta en proceso")
            return False
        if n == 1 and x["responsable"] == None:
            print("Error: la solicitud #" + str(id) + " no tiene responsable asignado")
            return False
        if n == x["estado"]:
            print("Error: la solicitud ya esta en ese estado")
            return False
        if n == 0:
            print("Error: no se puede volver a pendiente")
            return False
        x["estado"] = n
        self._guardar()
        for e in self.d["estudiantes"]:
            if e["legajo"] == x["legajo"]:
                print(
                    "[aviso a "
                    + e["email"]
                    + "] La solicitud #"
                    + str(x["id"])
                    + " paso a: "
                    + nuevo
                )
        print("Listo: solicitud #" + str(x["id"]) + " ahora esta " + nuevo)
        return True

    def asignar(self, id, resp_id):
        x = self._buscar_solicitud(id)
        if x == None:
            print("Error: no existe la solicitud #" + str(id))
            return False
        r = None
        for rr in self.d["responsables"]:
            if rr["id"] == resp_id:
                r = rr
        if r == None:
            print("Error: no existe el responsable " + resp_id)
            return False
        if x["estado"] == 2 or x["estado"] == 3:
            print("Error: la solicitud #" + str(id) + " ya esta cerrada")
            return False
        if r["area"] != x["area"]:
            print("Error: " + r["nombre"] + " no pertenece al area " + x["area"])
            return False
        x["responsable"] = resp_id
        self._guardar()
        print("Listo: solicitud #" + str(x["id"]) + " asignada a " + r["nombre"])
        return True

    def buscar(self, estado, tipo, prioridad, legajo):
        l = []
        for s in self.d["solicitudes"]:
            ok = True
            if estado != None:
                if estado == "pendiente" and s["estado"] != 0:
                    ok = False
                if estado == "en_proceso" and s["estado"] != 1:
                    ok = False
                if estado == "resuelta" and s["estado"] != 2:
                    ok = False
                if estado == "rechazada" and s["estado"] != 3:
                    ok = False
            if tipo != None and s["tipo"] != tipo:
                ok = False
            if prioridad != None:
                if prioridad == "alta" and s["prioridad"] != 1:
                    ok = False
                if prioridad == "media" and s["prioridad"] != 2:
                    ok = False
                if prioridad == "baja" and s["prioridad"] != 3:
                    ok = False
            if legajo != None and s["legajo"] != legajo:
                ok = False
            if ok:
                l.append(s)
        if len(l) == 0:
            print("No encontramos solicitudes")
        for s in l:
            est = ["pendiente", "en_proceso", "resuelta", "rechazada"][s["estado"]]
            pr = ["", "alta", "media", "baja"][s["prioridad"]]
            resp = "-"
            for rr in self.d["responsables"]:
                if rr["id"] == s["responsable"]:
                    resp = rr["nombre"]
            print(
                "#"
                + str(s["id"])
                + " | "
                + s["legajo"]
                + " | "
                + s["tipo"]
                + " | "
                + pr
                + " | "
                + est
                + " | "
                + resp
                + " | "
                + s["descripcion"]
            )
        return l

    def _resumen_reporte(self, hoy):
        resumen = {
            "total": len(self.d["solicitudes"]),
            "pendientes": 0,
            "en_proceso": 0,
            "resueltas": 0,
            "rechazadas": 0,
            "vencidas": 0,
            "por_area": {},
        }
        for s in self.d["solicitudes"]:
            if s["estado"] == 0:
                resumen["pendientes"] += 1
            if s["estado"] == 1:
                resumen["en_proceso"] += 1
            if s["estado"] == 2:
                resumen["resueltas"] += 1
            if s["estado"] == 3:
                resumen["rechazadas"] += 1
            if s["estado"] in (0, 1) and s["vence"] < hoy:
                resumen["vencidas"] += 1
            area = s["area"]
            resumen["por_area"][area] = resumen["por_area"].get(area, 0) + 1
        return resumen

    def _imprimir_reporte_texto(self, resumen):
        print("=== Reporte de solicitudes ===")
        print("Total: " + str(resumen["total"]))
        print("Pendientes: " + str(resumen["pendientes"]))
        print("En proceso: " + str(resumen["en_proceso"]))
        print("Resueltas: " + str(resumen["resueltas"]))
        print("Rechazadas: " + str(resumen["rechazadas"]))
        print("Vencidas sin cerrar: " + str(resumen["vencidas"]))
        print("Por area:")
        for area in sorted(resumen["por_area"]):
            print("  " + area + ": " + str(resumen["por_area"][area]))

    def _imprimir_reporte_csv(self, resumen):
        print("metrica,valor")
        print("total," + str(resumen["total"]))
        print("pendientes," + str(resumen["pendientes"]))
        print("en_proceso," + str(resumen["en_proceso"]))
        print("resueltas," + str(resumen["resueltas"]))
        print("rechazadas," + str(resumen["rechazadas"]))
        print("vencidas," + str(resumen["vencidas"]))
        for area in sorted(resumen["por_area"]):
            print("area:" + area + "," + str(resumen["por_area"][area]))

    def reporte(self, formato):
        hoy = datetime.now().strftime("%Y-%m-%d")
        resumen = self._resumen_reporte(hoy)
        if formato == "texto":
            self._imprimir_reporte_texto(resumen)
        elif formato == "csv":
            self._imprimir_reporte_csv(resumen)
        else:
            print("Error: formato de reporte invalido: " + formato)
            return False
        return True


def main():
    a = sys.argv
    s = Sistema()
    if len(a) < 2:
        print("Uso: python app.py [init|registrar|estado|asignar|buscar|reporte] ...")
        sys.exit(1)
    if a[1] == "init":
        r = s.init()
    elif a[1] == "registrar":
        if len(a) < 6:
            print("Uso: python app.py registrar LEGAJO TIPO PRIORIDAD DESCRIPCION [FECHA]")
            sys.exit(1)
        f = None
        if len(a) > 6:
            f = a[6]
        datos = DatosRegistro(a[2], a[3], a[4], a[5], f)
        r = s.registrar(datos)
    elif a[1] == "estado":
        r = s.cambiar_estado(a[2], a[3])
    elif a[1] == "asignar":
        r = s.asignar(a[2], a[3])
    elif a[1] == "buscar":
        filtros = {"estado": None, "tipo": None, "prioridad": None, "legajo": None}
        for x in a[2:]:
            k, v = x.split("=")
            filtros[k] = v
        r = s.buscar(filtros["estado"], filtros["tipo"], filtros["prioridad"], filtros["legajo"])
    elif a[1] == "reporte":
        fmt = "texto"
        if len(a) > 2:
            fmt = a[2]
        r = s.reporte(fmt)
    else:
        print("Error: comando desconocido " + a[1])
        sys.exit(1)
    if r == -1 or r == False:
        sys.exit(1)


if __name__ == "__main__":
    main()
