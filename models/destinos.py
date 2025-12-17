from .conexion import ConexionDB, oracledb

class Destino:
    id_destino: int
    nombre_destino: str
    pais: str
    ciudad: str
    descripcion: str # descripcion del destino como "lugar paradisiaco con vistas increibles".
    actividades: str # actividades dentro del destino como "surf, natación, parapente"
    precio: int

    def agregarDestino(self):
        try:
            c = ConexionDB()
            sql = """INSERT INTO destinos (nombre_destino, pais, ciudad, descripcion, actividades, precio)
                     VALUES (:nom_d, :pais, :ciud, :descr, :act, :precio)"""

            c.cursor.execute(sql,
                             nom_d  = self.nombre_destino,
                             pais   = self.pais,
                             ciud   = self.ciudad,
                             descr   = self.descripcion,
                             act    = self.actividades,
                             precio = self.precio)
            
            c.conexion.commit()
            print("Destino agregado")

        except oracledb.DatabaseError as e:
            print(f"Ocurrio un error al insertar destino {self.nombre_destino}")
            print(e)
            c.conexion.rollback()
        except Exception as e:
            print(f"Ocurrio un problema con la base de datos {e}")
        finally:
            c.cursor.close()
            c.conexion.close()

    def listarDestinos(self):
        try:
            c = ConexionDB()

            sql = "SELECT * FROM destinos"

            c.cursor.execute(sql)
            lista = c.cursor.fetchall()
            if lista:
                for d in lista:
                    print("---------------------------------------------------------------------")
                    print(f"id destino: {d[0]}")
                    print(f"Destino: {d[1]}                     precio: ${d[6]}")
                    print(f"pais: {d[2]}                     ciudad: {d[3]}")
                    print(f"Actividades disponibles: {d[5]}\n")

                    print(f"Descripcion: {d[4]}")
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


    def buscarDestino(id_destino:int):
        pass

    def modificarDestino(self):
        pass

    def eliminarDestino(self):
        pass

    def __str__(self):
        return f"""
Destino: {self.nombre_destino}            precio: ${self.precio}
pais: {self.pais}                      ciudad: {self.ciudad}
actividades disponibles: {self.actividades}

descripcion: {self.descripcion}
"""

