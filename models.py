# models.py
from tda import LinkedList, Queue

class Transaccion:
    def __init__(self, id_transaccion, nombre, tiempo_atencion):
        self.id = id_transaccion
        self.nombre = nombre
        self.tiempo_atencion = int(tiempo_atencion)  # en minutos

class Escritorio:
    def __init__(self, id_escritorio, identificacion, encargado):
        self.id = id_escritorio
        self.identificacion = identificacion
        self.encargado = encargado
        self.activo = False  # estado: activo/inactivo
        self.cliente_actual = None
        self.tiempo_restante = 0  # tiempo pendiente de atención

    def activar(self):
        self.activo = True

    def desactivar(self):
        self.activo = False

class PuntoAtencion:
    def __init__(self, id_punto, nombre, direccion):
        self.id = id_punto
        self.nombre = nombre
        self.direccion = direccion
        self.escritorios = LinkedList()   # Lista de Escritorios (TDA propia)
        self.cola_clientes = Queue()      # Cola de clientes esperando atención

    def agregar_escritorio(self, escritorio):
        self.escritorios.append(escritorio)

    def encolar_cliente(self, cliente):
        self.cola_clientes.enqueue(cliente)

class Empresa:
    def __init__(self, id_empresa, nombre, abreviatura):
        self.id = id_empresa
        self.nombre = nombre
        self.abreviatura = abreviatura
        self.puntos_atencion = LinkedList()      # Lista de Puntos de Atención
        self.transacciones = LinkedList()        # Lista de Transacciones

    def agregar_punto_atencion(self, punto):
        self.puntos_atencion.append(punto)

    def agregar_transaccion(self, transaccion):
        self.transacciones.append(transaccion)

class Cliente:
    def __init__(self, dpi, nombre):
        self.dpi = dpi
        self.nombre = nombre
        # Cada elemento de "listado_transacciones" es una tupla (Transaccion, cantidad)
        self.listado_transacciones = LinkedList()
        self.numero_atencion = None  # número asignado al solicitar atención

    def agregar_transaccion(self, transaccion, cantidad):
        # Se guarda la transacción junto a la cantidad solicitada
        self.listado_transacciones.append((transaccion, int(cantidad)))
