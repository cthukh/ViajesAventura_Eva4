from datetime import date
from .models.conexion import ConexionDB

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

    def CrearPaquete(self,id_destino:int):
        try:
            c = ConexionDB()

            sql = """INSERT INTO PAQUETES (nombre_paquete,precio_total,duracion_dias,servicios_incluidos,fecha_inicio,fecha_regreso)
                    VALUES ()"""

        except:
            pass
