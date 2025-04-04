import time
from models import Empresa, PuntoAtencion, Escritorio, Transaccion, Cliente
from xml_parser import parse_configuracion_sistema, parse_configuracion_inicial
from tda import LinkedList

class SistemaAtencion:
    def __init__(self):
        self.empresas = LinkedList()

    def limpiar_sistema(self):
        self.empresas = LinkedList()

    def cargar_configuracion_sistema(self, xml_file):
        nuevas_empresas = parse_configuracion_sistema(xml_file)
        for empresa in nuevas_empresas:
            self.empresas.append(empresa)

    def cargar_configuracion_inicial(self, xml_file):
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
        
        punto = next((p for p in empresa.puntos_atencion if p.id == id_punto), None)
        if not punto:
            return "Punto de atención no encontrado."
        
        return (f"Punto: {punto.nombre}\n"
                f"Escritorios activos: {sum(1 for e in punto.escritorios if e.activo)}\n"
                f"Escritorios inactivos: {sum(1 for e in punto.escritorios if not e.activo)}\n"
                f"Clientes en espera: {punto.cola_clientes.size()}\n")

    def activar_escritorio(self, id_empresa, id_punto, id_escritorio):
        empresa = self.buscar_empresa(id_empresa)
        if not empresa:
            return "Empresa no encontrada."
        
        punto = next((p for p in empresa.puntos_atencion if p.id == id_punto), None)
        if not punto:
            return "Punto de atención no encontrado."
        
        for escritorio in punto.escritorios:
            if escritorio.id == id_escritorio:
                escritorio.activar()
                return f"Escritorio {escritorio.identificacion} activado."
        return "Escritorio no encontrado."

    def desactivar_escritorio(self, id_empresa, id_punto, id_escritorio):
        empresa = self.buscar_empresa(id_empresa)
        if not empresa:
            return "Empresa no encontrada."
        
        punto = next((p for p in empresa.puntos_atencion if p.id == id_punto), None)
        if not punto:
            return "Punto de atención no encontrado."
        
        for escritorio in punto.escritorios:
            if escritorio.id == id_escritorio:
                escritorio.desactivar()
                return f"Escritorio {escritorio.identificacion} desactivado."
        return "Escritorio no encontrado."

    def atender_cliente(self, id_empresa, id_punto):
        empresa = self.buscar_empresa(id_empresa)
        if not empresa:
            return "Empresa no encontrada."
        
        punto = next((p for p in empresa.puntos_atencion if p.id == id_punto), None)
        if not punto:
            return "Punto de atención no encontrado."
        
        mensaje = ""
        for escritorio in punto.escritorios:
            if escritorio.activo and escritorio.cliente_actual is None:
                cliente = punto.cola_clientes.dequeue()
                if cliente:
                    cliente.tiempo_inicio_atencion = time.time()
                    tiempo_espera = (cliente.tiempo_inicio_atencion - cliente.tiempo_llegada) / 60
                    punto.tiempos_espera.append(tiempo_espera)
                    
                    escritorio.cliente_actual = cliente
                    escritorio.tiempo_restante = self._calcular_tiempo_atencion(cliente, empresa)
                    mensaje += f"Cliente {cliente.nombre} asignado a {escritorio.identificacion}\n"
                else:
                    mensaje += "No hay clientes en espera\n"
        return mensaje

    def _calcular_tiempo_atencion(self, cliente, empresa):
        tiempo_total = 0
        for trans_tuple in cliente.listado_transacciones:
            transaccion, cantidad = trans_tuple
            tiempo_total += transaccion.tiempo_atencion * cantidad
        return tiempo_total

    def solicitud_atencion(self, id_empresa, id_punto, cliente):
        empresa = self.buscar_empresa(id_empresa)
        if not empresa:
            return "Empresa no encontrada."
        
        punto = next((p for p in empresa.puntos_atencion if p.id == id_punto), None)
        if not punto:
            return "Punto de atención no encontrado."
        
        tiempo_espera = sum(self._calcular_tiempo_atencion(cli, empresa) for cli in punto.cola_clientes)
        punto.encolar_cliente(cliente)
        return f"Cliente {cliente.nombre} encolado. Tiempo estimado: {tiempo_espera} minutos"

    def simular_actividad(self, id_empresa, id_punto):
        empresa = self.buscar_empresa(id_empresa)
        if not empresa:
            return "Empresa no encontrada."
        
        punto = next((p for p in empresa.puntos_atencion if p.id == id_punto), None)
        if not punto:
            return "Punto de atención no encontrado."
        
        mensaje = []
        simulation_time = 0
        
        # Asignación inicial
        for escritorio in punto.escritorios:
            if escritorio.activo and not escritorio.cliente_actual:
                if not punto.cola_clientes.is_empty():
                    cliente = punto.cola_clientes.dequeue()
                    cliente.tiempo_inicio_atencion = time.time()
                    tiempo_espera = (cliente.tiempo_inicio_atencion - cliente.tiempo_llegada) / 60
                    punto.tiempos_espera.append(tiempo_espera)
                    
                    escritorio.cliente_actual = cliente
                    escritorio.tiempo_restante = self._calcular_tiempo_atencion(cliente, empresa)
                    mensaje.append(f"[{simulation_time} min] {cliente.nombre} asignado a {escritorio.identificacion}")

        # Ciclo de simulación
        while not punto.cola_clientes.is_empty() or any(e.cliente_actual for e in punto.escritorios):
            simulation_time += 1
            for escritorio in punto.escritorios:
                if escritorio.activo and escritorio.cliente_actual:
                    escritorio.tiempo_restante -= 1
                    
                    if escritorio.tiempo_restante <= 0:
                        tiempo_atencion = self._calcular_tiempo_atencion(escritorio.cliente_actual, empresa)
                        escritorio.tiempos_atencion.append(tiempo_atencion)
                        escritorio.clientes_atendidos += 1
                        
                        mensaje.append(f"[{simulation_time} min] {escritorio.cliente_actual.nombre} atendido en {escritorio.identificacion}")
                        escritorio.cliente_actual = None
                        
                        if not punto.cola_clientes.is_empty():
                            nuevo_cliente = punto.cola_clientes.dequeue()
                            nuevo_cliente.tiempo_inicio_atencion = time.time()
                            tiempo_espera = (nuevo_cliente.tiempo_inicio_atencion - nuevo_cliente.tiempo_llegada) / 60
                            punto.tiempos_espera.append(tiempo_espera)
                            
                            escritorio.cliente_actual = nuevo_cliente
                            escritorio.tiempo_restante = self._calcular_tiempo_atencion(nuevo_cliente, empresa)
                            mensaje.append(f"[{simulation_time} min] {nuevo_cliente.nombre} asignado a {escritorio.identificacion}")
            
            time.sleep(0.1)
        
        return "\n".join(mensaje)

sistema = SistemaAtencion()