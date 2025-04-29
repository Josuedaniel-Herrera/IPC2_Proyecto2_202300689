# xml_parser.py
import xml.etree.ElementTree as ET
from models import Empresa, PuntoAtencion, Escritorio, Transaccion, Cliente

def parse_configuracion_sistema(xml_file):
    """
    Parsea el archivo XML de configuración del sistema.
    Retorna una lista de objetos Empresa.
    """
    empresas = []
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for empresa_elem in root.findall('empresa'):
        id_empresa = empresa_elem.get('id')
        nombre = empresa_elem.find('nombre').text
        abreviatura = empresa_elem.find('abreviatura').text
        empresa = Empresa(id_empresa, nombre, abreviatura)

        # Parse puntos de atención
        puntos = empresa_elem.find('listaPuntosAtencion')
        if puntos is not None:
            for punto_elem in puntos.findall('puntoAtencion'):
                id_punto = punto_elem.get('id')
                nombre_punto = punto_elem.find('nombre').text
                direccion = punto_elem.find('direccion').text
                punto = PuntoAtencion(id_punto, nombre_punto, direccion)

                # Parse escritorios
                lista_escritorios = punto_elem.find('listaEscritorios')
                if lista_escritorios is not None:
                    for escritorio_elem in lista_escritorios.findall('escritorio'):
                        id_escritorio = escritorio_elem.get('id')
                        identificacion = escritorio_elem.find('identificacion').text
                        encargado = escritorio_elem.find('encargado').text
                        escritorio = Escritorio(id_escritorio, identificacion, encargado)
                        punto.agregar_escritorio(escritorio)
                empresa.agregar_punto_atencion(punto)

        # Parse transacciones
        lista_transacciones = empresa_elem.find('listaTransacciones')
        if lista_transacciones is not None:
            for transaccion_elem in lista_transacciones.findall('transaccion'):
                id_transaccion = transaccion_elem.get('id')
                nombre_trans = transaccion_elem.find('nombre').text
                tiempo_atencion = transaccion_elem.find('tiempoAtencion').text
                transaccion = Transaccion(id_transaccion, nombre_trans, tiempo_atencion)
                empresa.agregar_transaccion(transaccion)

        empresas.append(empresa)
    return empresas

def parse_configuracion_inicial(xml_file, empresas):
    """
    Parsea el archivo XML de configuración inicial de la prueba.
    Se asume que 'empresas' es la lista de empresas ya cargada.
    Se busca la empresa y punto de atención para asignar clientes y activar escritorios.
    Retorna la lista actualizada de empresas.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for config_elem in root.findall('configInicial'):
        id_empresa = config_elem.get('idEmpresa')
        id_punto = config_elem.get('idPunto')

        empresa_obj = next((e for e in empresas if e.id == id_empresa), None)
        if empresa_obj is None:
            continue
        punto_obj = next((p for p in empresa_obj.puntos_atencion if p.id == id_punto), None)
        if punto_obj is None:
            continue

        # Activar escritorios según el XML
        escritorios_activos = config_elem.find('escritoriosActivos')
        if escritorios_activos is not None:
            for esp in escritorios_activos.findall('escritorio'):
                id_escritorio = esp.get('idEscritorio')
                for escritorio in punto_obj.escritorios:
                    if escritorio.id == id_escritorio:
                        escritorio.activar()

        # Agregar clientes a la cola, detectando prioridad
        listado_clientes = config_elem.find('listadoClientes')
        if listado_clientes is not None:
            for cliente_elem in listado_clientes.findall('cliente'):
                dpi = cliente_elem.get('dpi')
                nombre_cliente = cliente_elem.find('nombre').text
                # << Detección de prioridad desde XML
                prioridad_elem = cliente_elem.find('prioridad')
                prioridad = prioridad_elem is not None and prioridad_elem.text.lower() == 'true'
                cliente = Cliente(dpi, nombre_cliente, prioridad)

                listado_trans = cliente_elem.find('listadoTransacciones')
                if listado_trans is not None:
                    for trans_elem in listado_trans.findall('transaccion'):
                        id_trans = trans_elem.get('idTransaccion')
                        cantidad = trans_elem.get('cantidad')
                        trans_obj = next((t for t in empresa_obj.transacciones if t.id == id_trans), None)
                        if trans_obj is not None:
                            cliente.agregar_transaccion(trans_obj, cantidad)

                punto_obj.encolar_cliente(cliente)

    return empresas
