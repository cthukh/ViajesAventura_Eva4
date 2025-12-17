import oracledb

class ConexionDB:
    def __init__(self):
        user = "SUISEI" # cambiar por su usuario
        password = "inacap"
        dsn = "localhost/xe"
        
        try:
            self.conexion = oracledb.connect(user=user, password=password, dsn=dsn)
            self.cursor = self.conexion.cursor()
        except:
            print("No se pudo realizar la conexion a Oracle...")