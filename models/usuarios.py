from .conexion import ConexionDB,oracledb
import bcrypt
from datetime import date, datetime

class TipoUsuario:
    id_tipo_usuario: int
    tipo: str

class Usuario:
    id_usuario: int
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    rut: str
    fecha_nacimiento: date
    correo_electronico: str
    telefono: str
    id_tipo_usuario: int
    estado: int
    password: str

    def encriptar_psw(self, password: str):
        """
        pasamos la contraseña como str y nos retornará un hash de esta
        
        :param password: contraseña cualquiera
        :type password: str
        """
        try:
            password_bytes = password.encode()
            password_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
            hash = password_bytes.decode()
            return hash
        except:
            print("No se pudo encriptar la contraseña")
            return None
        
    def verificarRut(self,rut:str):
        """
        Docstring para verificarRut
        
        :param rut: Descripción
        :type rut: str
        """
        rut = rut.strip().replace(".","").replace("-","")
        if len(rut) < 7:
            return False
        numero = rut[:-1]
        dv = rut[-1].upper()
        suma = 0
        multi = 2
        for i in reversed(range(len(numero))):
            suma += int(numero[i]) * multi
            multi = multi + 1 if multi < 7 else 2
        dv_calculado = 11 - (suma % 11)
        if dv_calculado == 11:
            dv_calculado = '0'
        elif dv_calculado == 1:
            dv_calculado == 'K'

    def insetar(self):
        try:
            c = ConexionDB()

            sql = """INSERT INTO USUARIOS 
                        (nombre, apellido_paterno, apellido_materno, rut, fecha_nacimiento, correo_electronico, telefono, id_tipo_usuario, password)
                    VALUES (:nom, :ape_p, :ape_m, :rut, TO_DATE(:fecha_n, 'YYYY-MM-DD'), :email, :fono, :tipo_u, :passw)"""
            
            # print(self.fecha_nacimiento)

            c.cursor.execute(sql,
                             nom     = self.nombre,
                             ape_p   = self.apellido_paterno,
                             ape_m   = self.apellido_materno,
                             rut     = self.rut,
                             fecha_n = self.fecha_nacimiento,
                             email   = self.correo_electronico,
                             fono    = self.telefono,
                             tipo_u  = self.id_tipo_usuario,
                             passw   = self.password)
            c.conexion.commit()
            print("Cuenta creada")
            return self

        except oracledb.DatabaseError as e:
            print(f"Ocurrio un error al insertar usuario {self.nombre}")
            print(e)
            c.conexion.rollback()
        except Exception as e:
            print(f"Ocurrio un problema con la base de datos {e}")
            return None
        finally:
            c.cursor.close()
            c.conexion.close()


    def login(self, correo_e:str, password_en_bytes:bytes):
        try:
            c = ConexionDB()

            sql = "SELECT * FROM usuarios WHERE correo_electronico = :email"
            c.cursor.execute(sql,
                            email = correo_e)
            
            fila = c.cursor.fetchone()

            if fila:
                self.id_usuario         = fila[0]
                self.nombre             = fila[1]
                self.apellido_paterno   = fila[2]
                self.apellido_materno   = fila[3]
                self.rut                = fila[4]
                self.fecha_nacimiento   = fila[5]
                self.correo_electronico = fila[6]
                self.telefono           = fila[7]
                self.id_tipo_usuario    = fila[8]
                self.estado             = fila[9]
                self.password           = fila[10]

                password_bd = self.password.encode()
                autenticado = bcrypt.checkpw(password_en_bytes, password_bd)
                return autenticado

            else:
                print("No existe usuario")
                return None

        except oracledb.DatabaseError as e:
            print(f"Ocurrio un error al iniciar sesión")
            print(e)
            c.conexion.rollback()
        except:
            print("Ocurrio un problema con la base de datos ")
        finally:
            c.cursor.close()
            c.conexion.close()