# simulation.py
import time
from models import Empresa, PuntoAtencion, Escritorio, Transaccion, Cliente
from xml_parser import parse_configuracion_sistema, parse_configuracion_inicial
from tda import LinkedList

class SistemaAtencion:
    def __init__(self):
        # Se almacena la información de las empresas usando el TDA LinkedList
        self.empresas = LinkedList()

    def limpiar_sistema(self):
        self.empresas = LinkedList()

    def cargar_configuracion_sistema(self, xml_file):
        nuevas_empresas = parse_configuracion_sistema(xml_file)
        for empresa in nuevas_empresas:
            self.empresas.append(empresa)

    def cargar_configuracion_inicial(self, xml_file):
        # Convertir temporalmente el TDA a una lista para el parseo
        empresas_temp = [e for e in self.empresas]
        empresas_temp = parse_configuracion_inicial(xml_file, empresas_temp)
        self.empresas = LinkedList()
        for empresa in empresas_temp:
            self.empresas.append(empresa)

    def crear_empresa(self, id_empresa, nombre, abreviatura):
        empresa = Empresa(id_empresa, nombre, abreviatura)
        self.empresas.append(empresa)
        return empresa

    def buscar_empresa(self, id_empresa):
        for empresa in self.empresas:
            if empresa.id == id_empresa:
                return empresa
        return None

    def ver_estado_punto(self, id_empresa, id_punto):
        empresa = self.buscar_empresa(id_empresa)
        if not empresa:
            return "Empresa no encontrada."
        punto = None
        for p in empresa.puntos_atencion:
            if p.id == id_punto:
                punto = p
                break
        if not punto:
            return "Punto de atención no encontrado."
        # Contar clientes en espera recorriendo la cola
        clientes_en_espera = 0
        for _ in punto.cola_clientes:
            clientes_en_espera += 1
        # Contar escritorios activos e inactivos
        escritorios_activos = 0
        escritorios_inactivos = 0
        for escritorio in punto.escritorios:
            if escritorio.activo:
                escritorios_activos += 1
            else:
                escritorios_inactivos += 1
        estado = (f"Punto: {punto.nombre}\n"
                  f"Escritorios activos: {escritorios_activos}\n"
                  f"Escritorios inactivos: {escritorios_inactivos}\n"
                  f"Clientes en espera: {clientes_en_espera}\n")
        return estado

    def activar_escritorio(self, id_empresa, id_punto, id_escritorio):
        empresa = self.buscar_empresa(id_empresa)
        if not empresa:
            return "Empresa no encontrada."
        punto = None
        for p in empresa.puntos_atencion:
            if p.id == id_punto:
                punto = p
                break
        if not punto:
            return "Punto de atención no encontrado."
        for escritorio in punto.escritorios:
            if escritorio.id == id_escritorio:
                escritorio.activar()
                return f"Escritorio {id_escritorio} activado."
        return "Escritorio no encontrado."

    def desactivar_escritorio(self, id_empresa, id_punto, id_escritorio):
        empresa = self.buscar_empresa(id_empresa)
        if not empresa:
            return "Empresa no encontrada."
        punto = None
        for p in empresa.puntos_atencion:
            if p.id == id_punto:
                punto = p
                break
        if not punto:
            return "Punto de atención no encontrado."
        for escritorio in punto.escritorios:
            if escritorio.id == id_escritorio:
                escritorio.desactivar()
                return f"Escritorio {id_escritorio} desactivado."
        return "Escritorio no encontrado."

    def atender_cliente(self, id_empresa, id_punto):
        empresa = self.buscar_empresa(id_empresa)
        if not empresa:
            return "Empresa no encontrada."
        punto = None
        for p in empresa.puntos_atencion:
            if p.id == id_punto:
                punto = p
                break
        if not punto:
            return "Punto de atención no encontrado."
        mensaje = ""
        # Asigna a cada escritorio activo que esté libre el siguiente cliente de la cola
        for escritorio in punto.escritorios:
            if escritorio.activo and escritorio.cliente_actual is None:
                cliente = punto.cola_clientes.dequeue()
                if cliente:
                    escritorio.cliente_actual = cliente
                    escritorio.tiempo_restante = self.calcular_tiempo_atencion(cliente, empresa)
                    mensaje += f"Cliente {cliente.nombre} asignado a escritorio {escritorio.identificacion}.\n"
                else:
                    mensaje += "No hay clientes en espera.\n"
        return mensaje

    def calcular_tiempo_atencion(self, cliente, empresa):
        tiempo_total = 0
        # Suma el tiempo requerido de todas las transacciones solicitadas por el cliente
        for trans_tuple in cliente.listado_transacciones:
            transaccion, cantidad = trans_tuple
            tiempo_total += transaccion.tiempo_atencion * cantidad
        return tiempo_total

    def solicitud_atencion(self, id_empresa, id_punto, cliente):
        empresa = self.buscar_empresa(id_empresa)
        if not empresa:
            return "Empresa no encontrada."
        punto = None
        for p in empresa.puntos_atencion:
            if p.id == id_punto:
                punto = p
                break
        if not punto:
            return "Punto de atención no encontrado."
        tiempo_espera = 0
        for cli in punto.cola_clientes:
            tiempo_espera += self.calcular_tiempo_atencion(cli, empresa)
        punto.encolar_cliente(cliente)
        return f"Cliente encolado. Tiempo de espera estimado: {tiempo_espera} minutos."

    def simular_actividad(self, id_empresa, id_punto):
        mensaje = ""
        empresa = self.buscar_empresa(id_empresa)
        if not empresa:
            return "Empresa no encontrada."
        punto = None
        for p in empresa.puntos_atencion:
            if p.id == id_punto:
                punto = p
                break
        if not punto:
            return "Punto de atención no encontrado."

        simulation_time = 0  # contador en minutos simulados
        # Asignación inicial de clientes a escritorios vacíos
        for escritorio in punto.escritorios:
            if escritorio.activo and escritorio.cliente_actual is None and not punto.cola_clientes.is_empty():
                nuevo_cliente = punto.cola_clientes.dequeue()
                escritorio.cliente_actual = nuevo_cliente
                escritorio.tiempo_restante = self.calcular_tiempo_atencion(nuevo_cliente, empresa)
                mensaje += f"[{simulation_time} min] Cliente {nuevo_cliente.nombre} asignado a escritorio {escritorio.identificacion}.\n"

        # Ciclo de simulación: se procesa mientras haya clientes en cola o algún escritorio esté ocupado.
        while (not punto.cola_clientes.is_empty()) or any(e.cliente_actual for e in punto.escritorios):
            simulation_time += 1
            for escritorio in punto.escritorios:
                if escritorio.activo and escritorio.cliente_actual:
                    escritorio.tiempo_restante -= 1
                    if escritorio.tiempo_restante <= 0:
                        mensaje += f"[{simulation_time} min] Cliente {escritorio.cliente_actual.nombre} atendido en escritorio {escritorio.identificacion}.\n"
                        escritorio.cliente_actual = None
                        if not punto.cola_clientes.is_empty():
                            nuevo_cliente = punto.cola_clientes.dequeue()
                            escritorio.cliente_actual = nuevo_cliente
                            escritorio.tiempo_restante = self.calcular_tiempo_atencion(nuevo_cliente, empresa)
                            mensaje += f"[{simulation_time} min] Cliente {nuevo_cliente.nombre} asignado a escritorio {escritorio.identificacion}.\n"
            time.sleep(0.1)
        return mensaje

# Se crea una instancia global del sistema para utilizar en la interfaz
sistema = SistemaAtencion()

