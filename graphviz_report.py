# graphviz_report.py
from graphviz import Digraph

def generar_reporte_cola(punto):
    """
    Genera un diagrama de la cola de clientes del punto de atención.
    Se muestran también las transacciones y cantidades que realizará cada cliente.
    Si la cola está vacía, se muestra un nodo indicando "Cola Vacía".
    """
    dot = Digraph(comment='Cola de Clientes')
    contador = 1
    tiene_clientes = False
    for cliente in punto.cola_clientes:
        tiene_clientes = True
        # Construir cadena con las transacciones y cantidades
        transacciones_str = ""
        for trans_tuple in cliente.listado_transacciones:
            transaccion, cantidad = trans_tuple
            transacciones_str += f"{transaccion.id}({cantidad}), "
        transacciones_str = transacciones_str.rstrip(", ")
        label = f"{cliente.nombre}\nDPI: {cliente.dpi}\nTransacciones: {transacciones_str}"
        dot.node(f'cliente{contador}', label)
        if contador > 1:
            dot.edge(f'cliente{contador-1}', f'cliente{contador}')
        contador += 1
    if not tiene_clientes:
        dot.node('vacio', 'Cola Vacía')
    dot.render('reporte_cola.gv', view=True)
    return "Reporte de cola generado (reporte_cola.gv.pdf)"

def generar_reporte_escritorios(punto):
    """
    Genera un diagrama de los escritorios de servicio en el punto de atención.
    """
    dot = Digraph(comment='Escritorios de Servicio')
    for escritorio in punto.escritorios:
        estado = "Activo" if escritorio.activo else "Inactivo"
        label = f"{escritorio.identificacion}\nEncargado: {escritorio.encargado}\nEstado: {estado}"
        dot.node(escritorio.id, label)
    dot.render('reporte_escritorios.gv', view=True)
    return "Reporte de escritorios generado (reporte_escritorios.gv.pdf)"
