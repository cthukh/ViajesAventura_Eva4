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
            sql = "INSERT INTO reservaciones (id_paquete, id_usuario) VALUES (:id_pac, :id_user)"
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

    def verReservaciones(self,id_usuario:int):
        try:
            c = ConexionDB()

            sql = "SELECT * FROM reservaciones WHERE id_usuario = :id_u"

            c.cursor.execute(sql,
                             id_u = id_usuario)
            lista = c.cursor.fetchall()
            if lista:
                for r in lista:
                    id_paquete = r[1]
                    sql_bus_nom_paq = "SELECT * FROM paquetes WHERE id_paquete = :id_p"
                    c.cursor.execute(sql_bus_nom_paq,id_p = id_paquete)
                    fila = c.cursor.fetchone()
                    if fila:
                        nombre_paquete = fila[1]


                    sql_busqueda_paquete = "SELECT id_destino FROM destinos_paquetes WHERE id_paquete = :id_p"
                    c.cursor.execute(sql_busqueda_paquete, id_p = id_paquete)
                    lista_d = c.cursor.fetchall()
                    lista_nombres_destinos = []
                    if lista_d:
                        for dest in lista_d:
                            id_destino = dest[0]
                            sql_destino = "SELECT nombre_destino FROM destinos WHERE id_destino = :id_d"
                            c.cursor.execute(sql_destino,id_d = id_destino)
                            fila_d = c.cursor.fetchone()
                            if fila_d:
                                lista_nombres_destinos.append(fila_d[0])
                    print("-------------------------------------------------------")
                    print(f"id reservacion: {r[0]}")
                    print(f"nombre paquete: {nombre_paquete}")
                print("-------------------------------------------------------")
            if not lista:
                print("No se encotraro registros")
                return None



        except oracledb.DatabaseError as e:
            print(f"Ocurrio un error al consultar a la base de datos")
            print(e)
            c.conexion.rollback()
        except Exception as e:
            print(f"Ocurrio un problema con la base de datos {e}")
        finally:
            c.cursor.close()
            c.conexion.close()