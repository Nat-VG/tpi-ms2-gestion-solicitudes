# Gestión de solicitudes académicas

Registramos solicitudes de estudiantes, las derivamos al área que corresponde, les asignamos un responsable y seguimos el estado hasta cerrarlas. También podemos buscarlas y armar un reporte simple.

Los datos del sistema son inventados.

## Cómo correrlo

Hace falta Python 3.10 o superior.

```bash
python app.py init
python app.py registrar 1001 certificado alta "Constancia de examen" 2026-10-01
python app.py asignar 4 R1
python app.py estado 4 en_proceso
python app.py estado 4 resuelta
python app.py buscar estado=pendiente
python app.py reporte
python app.py reporte csv
```

`init` carga estudiantes, responsables y tres solicitudes de ejemplo en `datos.json`.

## Qué acepta

| Dato | Valores |
|---|---|
| Tipo | `certificado` y `cambio_comision` van a Bedelia. `equivalencia` va a Departamento Academico. `reclamo_nota` va a Docencia. |
| Prioridad | `alta` (2 días), `media` (5 días), `baja` (10 días) |
| Estado | `pendiente`, `en_proceso`, `resuelta`, `rechazada` |
| Filtros | `estado=`, `tipo=`, `prioridad=`, `legajo=` |

Una solicitud pendiente puede pasar a `en_proceso` si ya tiene un responsable del área, o rechazarse directo. Para resolverla tiene que estar en proceso. Un trámite cerrado no vuelve atrás.

## Ejemplo cargado con init

| Legajo | Estudiante |
|---|---|
| 1001 | Martina Ruiz |
| 1002 | Lucas Pereyra |
| 1003 | Sofia Benitez |

| Id | Responsable | Área |
|---|---|---|
| R1 | Elena Vargas | Bedelia |
| R2 | Pablo Medina | Departamento Academico |
| R3 | Nora Acosta | Docencia |
