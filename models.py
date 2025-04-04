# models.py
from tda import LinkedList, Queue
import time

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
        # Nuevos atributos para métricas
        self.tiempos_atencion = LinkedList()  # Historial de tiempos de atención
        self.clientes_atendidos = 0          # Contador de clientes atendidos

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
        # Nuevo atributo para métricas de espera
        self.tiempos_espera = LinkedList()  # Tiempos de espera de clientes

    def agregar_escritorio(self, escritorio):
        self.escritorios.append(escritorio)

    def encolar_cliente(self, cliente):
        self.cola_clientes.enqueue(cliente)

    # Nuevo método para cálculo de métricas
    def calcular_metricas_punto(self):
        metricas = {
            'escritorios_activos': sum(1 for e in self.escritorios if e.activo),
            'escritorios_inactivos': sum(1 for e in self.escritorios if not e.activo),
            'tiempos_espera': [],
            'tiempos_atencion': []
        }
        
        # Convertir LinkedList a lista para cálculos
        metricas['tiempos_espera'] = [t for t in self.tiempos_espera]
        
        # Recopilar tiempos de atención de todos los escritorios
        for escritorio in self.escritorios:
            metricas['tiempos_atencion'].extend([t for t in escritorio.tiempos_atencion])
            
        return metricas

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
        # Nuevos atributos para registro de tiempos
        self.tiempo_llegada = time.time()        # Timestamp de llegada a la cola
        self.tiempo_inicio_atencion = 0          # Timestamp de inicio de atención

    def agregar_transaccion(self, transaccion, cantidad):
        # Se guarda la transacción junto a la cantidad solicitada
        self.listado_transacciones.append((transaccion, int(cantidad)))