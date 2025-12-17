from datetime import datetime
from .conexion import ConexionDB, oracledb

class Reservacion:
    id_reservacion: int
    id_paquete: int
    id_usuario: int
    fecha_reserva: datetime
    estado_reservacion: str

    def reservarPaquete(self, id_paquete:int, id_usuario:int):
        try:
            c = ConexionDB()
            sql = "INSERT INTO reservaciones (id_paquete, id_usuario,) VALUES (:id_pac, :id_user)"
            c.cursor.execute(sql,
                             id_pac = id_paquete,
                             id_user = id_usuario)
            
            c.conexion.commit()
            print("Reservacion completa")

        except oracledb.DatabaseError as e:
            print(f"Ocurrio un error al consultar a la base de datos")
            print(e)
            c.conexion.rollback()
        except Exception as e:
            print(f"Ocurrio un problema con la base de datos {e}")
        finally:
            c.cursor.close()
            c.conexion.close()