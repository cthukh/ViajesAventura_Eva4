from datetime import date
from .conexion import ConexionDB, oracledb

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

    def CrearPaquete(self, destinos_ids: list):
        """
        Crea un paquete y asocia los destinos indicados (lista de ids).
        Retorna el id del paquete creado o None en caso de error.
    
        :param destinos_ids: Descripción
        :type destinos_ids: list
        
        """
        try:
            c = ConexionDB()

            sql_insertar_paquete = """
            INSERT INTO paquetes (nombre_paquete, precio_total, duracion_dias, servicios_incluidos, fecha_inicio, fecha_regreso)
            VALUES (:nom, :precio, :duracion, :serv, TO_DATE(:fecha_ini, 'YYYY-MM-DD'), TO_DATE(:fecha_reg, 'YYYY-MM-DD'))
            """
            c.cursor.execute(sql_insertar_paquete,
                             nom       = self.nombre_paquete,
                             precio    = self.precio_total,
                             duracion  = self.duracion_dias,
                             serv      = self.servicios_incluidos,
                             fecha_ini = self.fecha_inicio,
                             fecha_reg = self.fecha_regreso)
            
            c.conexion.commit()

            sql_busq_paquete = """ SELECT id_paquete FROM paquetes WHERE nombre_paquete = :nom"""

            c.cursor.execute(sql_busq_paquete,
                             nom = self.nombre_paquete)
            
            fila = c.cursor.fetchone()
            if fila:
                self.id_paquete = fila[0]

            sql_insertar_relacion = """INSERT INTO destinos_paquetes (id_paquete, id_destino) 
                                        VALUES (:id_pac, :id_des)"""
            for id_d in destinos_ids:
                c.cursor.execute(sql_insertar_relacion,
                                 id_pac = self.id_paquete,
                                 id_des = id_d)
                
            c.conexion.commit()
            print(f"Paquete creado con id {self.id_paquete}")

        except oracledb.DatabaseError as e:
            print(f"Ocurrio un error al crear el paquete: {e}")
            c.conexion.rollback()
            return None
        except Exception as e:
            print(f"Ocurrio un error inesperado: {e}")
            try:
                c.conexion.rollback()
            except:
                pass
            return None
        finally:
            c.cursor.close()
            c.conexion.close()

    def listarPaquetes(self):
        try:
            c = ConexionDB()

            sql = "SELECT * FROM paquetes"

            c.cursor.execute(sql)
            lista = c.cursor.fetchall()
            if lista:
                for p in lista:
                    id_paquete = p[0]
                    sql_busq_destinos = """SELECT id_destino FROM destinos_paquetes WHERE id_paquete = :id_p"""

                    c.cursor.execute(sql_busq_destinos,
                                     id_p = id_paquete)
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


                    print("---------------------------------------------------------------------")
                    print(f"id paquete: {id_paquete}")
                    print(f"nombre: {p[1]}")
                    for d in lista_nombres_destinos:
                        print(f"destino: {d}")
                    print(f"precio total: {p[2]}")
                    print(f"duración dias: {p[3]}")
                    print(f"incluye: {p[4]}")
                    print(f"fecha inicio: {p[5]}")
                    print(f"fecha regreso: {p[6]}")
                    print("")

                print("---------------------------------------------------------------------")
                return lista

            else:
                print("No se encontraron registros")
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