import os
from models.destinos import Destino
from models.usuarios import Usuario
from models.paquetes import Paquete
from models.reservaciones import Reservacion

def index():
    print("¡Bienvenido a Viajes Aventura!")
    print("Inicia sesión para ver las opciones de viaje ")
    print("")
    print("1. Iniciar sesion")
    print("2. Crear cuenta")
    print("0. Salir")
    print("")

def menuAdminDestinos():
    print("menu de adminstracion\n")

    print("1. Agregar destino")
    print("2. Agregar Paquetes")

    opcionAdmin = int(input("Ingrese opcion: "))
        
    if opcionAdmin == 1: # Agregar destino
        os.system("cls")
        print("Agregar destino\n")

        destino.nombre_destino = input("Ingrese nombre del destino: ")
        destino.pais = input("Ingrese pais: ")
        destino.ciudad = input("Ingrese ciudad: ")
        destino.descripcion  = input("Ingrese descripcion del destino: ")
        destino.actividades = input("Ingrese actividades posibles a realizar: ")
        destino.precio = input("Ingrese precio: ")

        destino.agregarDestino()

    elif opcionAdmin == 2:                  # Agregar paquete
        print("Agregar paquetes \n")
        print("-----------------------------")
        
        print("Listado de destinos\n")
        destino.listarDestinos()

        print("")
        cantidad_destinos = int(input("Ingrese la cantidad de destinos quiera agregar: "))
        lista_ids = []
        c = 1

        print("")
        while c <= cantidad_destinos:
            id_destino = int(input(f"Ingrese la id del destino {c}: "))
            lista_ids.append(id_destino)
            c += 1
        print(lista_ids)

        print("")
        paquete.nombre_paquete = input("Ingrese nombre del paquete: ")
        paquete.precio_total = input("Ingrese precio del paquete: ")
        paquete.duracion_dias = int(input("Ingrese la duración del viaje en dias: "))
        paquete.servicios_incluidos = input("Ingrese los servicios incluidos (Ejemplo: Alojamiento, desayuno): ")
        paquete.fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
        paquete.fecha_regreso = input("Ingrese la fecha de retorno/termino (YYYY-MM-DD): ")

        paquete.CrearPaquete(lista_ids)


def menuHome(usuario:object):
    os.system("cls")
    tipo_usuario = usuario.id_tipo_usuario

    print(f"Hola {usuario.nombre}")
    print("¿Qué vamos a hacer hoy?\n")

    print("1. Explorar paquetes")
    print("2. ver destinos")
    print("3. Reservar paquete")
    print("5. ver reservas")

    if tipo_usuario!= 1:
        print("4. panel de administración")
    print("0. Cerrar sesión")
    print("")

    opcionHome = int(input("Ingrese opcion: "))
    while opcionHome < 0 or opcionHome > 4:
        print("Opcion invalida")
        opcionHome = int(input("Ingrese opcion: "))

    while opcionHome == 4 and tipo_usuario == 1:
        print("opcion invalida")
        opcionHome = int(input("Ingrese opcion: "))

    if opcionHome == 1: # Ver paquetes
        print("Listado de paquetes\n")

        paquete.listarPaquetes()
        back = input("Presione ENTER para continuar ")
        menuHome(usuario)

    elif opcionHome == 3: # reservar paquete
        print("Generar reservación")
        print("----------------------------------\n")

        paquete.listarPaquetes()

        id_paquete_a_reservar = int(input("Ingrese la id del paquete que quiera reservar: "))
        id_usuario = usuario.id_usuario

        reservacion.reservarPaquete(id_paquete_a_reservar, id_usuario)
        back = input("Presione ENTER para continuar ")
        menuHome(usuario)



    elif opcionHome == 2: # Ver destinos
        print("Listado de destinos\n")
        destino.listarDestinos()
        back = input("Presione ENTER para continuar ")
        menuHome(usuario)

    elif opcionHome == 3 and tipo_usuario != 1:
            menuAdminDestinos()
            back = input("Presione ENTER para continuar ")
            menuHome(usuario)

    elif opcionHome == 0:
        index()


def menuIniciarSesion():
    os.system("cls")
    print("Inicio de sesión\n")

    correo = input("Ingrese su correo electronico: ")
    password = input("Ingrese su contraseña: ")
    password_bytes = password.encode()

    autenticado = usuario.login(correo, password_bytes)
    
    if autenticado:
        menuHome(usuario)

    elif not autenticado:
        print("No se pudo inciar sesión")
        back = input("Presione ENTER para continuar ")


def menuCrearCuenta():
    print("Crear una cuenta \n")
    
    nombre             = input("Ingrese su nombre: ")
    apellido_paterno   = input("Ingrese apellido paterno: ")
    apellido_materno   = input("Ingrese apellido materno: ")
    rut                = input("Ingrese su RUT: ")

    while usuario.verificarRut(rut) == False :
        print("RUT no valido, vuelva a ingresar")
        rut = input("Ingrese su RUT: ")

    print("-- Fecha de nacimiento --")
    year               = input("Año de nacimiento: ")
    mes                = input("Mes de nacimiento: ")
    dia                = input("Dia de nacimiento: ")
    fecha_nacimiento = f"{year}-{mes}-{dia}"
    correo_electronico = input("Ingrese su correo electronico: ")
    telefono           = input("Ingrese su número de teléfono: ")
    password           = input("Ingrese una contraseña para la cuenta: ")
    while len(password) < 4:
        print("Contraseña demasiado corta")
        password = input("Ingrese una contraseña para la cuenta: ")

    password_hash = usuario.encriptar_psw(password)


    usuario.nombre             = nombre
    usuario.apellido_paterno   = apellido_paterno
    usuario.apellido_materno   = apellido_materno
    usuario.rut                = rut
    usuario.fecha_nacimiento   = fecha_nacimiento
    usuario.correo_electronico = correo_electronico
    usuario.telefono           = telefono
    usuario.id_tipo_usuario    = 1
    usuario.estado             = 1
    usuario.password           = password_hash

    usuario_creado = usuario.insetar()
    back = input("Presione ENTER para continuar ")
    if usuario_creado:
        menuHome(usuario)



reservacion = Reservacion() 
paquete = Paquete()
destino = Destino()
usuario = Usuario()



while True:
    os.system("cls")
    index()
    opcion_inicio = int(input("Ingrese una opción: "))

    while opcion_inicio > 2 or opcion_inicio < 0:
        print("opcion invalida")
        opcion_inicio = int(input("Ingrese una opción: "))

    if opcion_inicio == 1:      # iniciar sesion
        menuIniciarSesion()

    elif opcion_inicio == 2:    # crear cuenta
        menuCrearCuenta()

    elif opcion_inicio == 0:
        exit()
