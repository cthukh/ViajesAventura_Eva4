from datetime import date

class DestinosPaquetes:
    id_destino_paquete: int
    id_paquete: int
    id_destino: int

class Paquete:
    id_paquete: int
    nombre_paquete: str
    precio_total: float
    duracion_dias: int
    servicios_incluidos: str
    fecha_inicio: date
    fecha_regreso: date

