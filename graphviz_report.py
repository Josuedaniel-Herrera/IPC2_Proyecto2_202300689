from graphviz import Digraph

def generar_reporte_cola(punto):
    dot = Digraph(comment='Cola de Clientes', format='png')
    contador = 1
    
    for cliente in punto.cola_clientes:
        transacciones = "\\n".join([f"{t[0].id} x{t[1]}" for t in cliente.listado_transacciones])
        label = f"{cliente.nombre}\\nDPI: {cliente.dpi}\\n---\\n{transacciones}"
        dot.node(str(contador), label, shape='box')
        
        if contador > 1:
            dot.edge(str(contador-1), str(contador))
        contador += 1
    
    if contador == 1:
        dot.node('vacio', 'Cola Vacía', shape='box')
    
    dot.render('reporte_cola', view=False, cleanup=True)
    return "Reporte de cola generado: reporte_cola.png"

def generar_reporte_escritorios(punto):
    dot = Digraph(comment='Escritorios de Servicio', format='png')
    
    for escritorio in punto.escritorios:
        tiempos = [t for t in escritorio.tiempos_atencion]
        stats = (
            sum(tiempos)/len(tiempos) if tiempos else 0,
            max(tiempos) if tiempos else 0,
            min(tiempos) if tiempos else 0
        )
        
        label = (
            f"{escritorio.identificacion}\\n"
            f"Encargado: {escritorio.encargado}\\n"
            f"Estado: {'Activo' if escritorio.activo else 'Inactivo'}\\n"
            "---\\n"
            f"Atendidos: {escritorio.clientes_atendidos}\\n"
            f"T. Promedio: {stats[0]:.2f} min\\n"
            f"T. Máximo: {stats[1]:.2f} min\\n"
            f"T. Mínimo: {stats[2]:.2f} min"
        )
        
        dot.node(
            escritorio.id, 
            label, 
            shape='box', 
            color='green' if escritorio.activo else 'red'
        )
    
    dot.render('reporte_escritorios', view=False, cleanup=True)
    return "Reporte de escritorios generado: reporte_escritorios.png"