from datetime import datetime

class Reservacion:
    id_reservacion: int
    id_paquete: int
    id_usuario: int
    fecha_reserva: datetime
    estado_reservacion: str