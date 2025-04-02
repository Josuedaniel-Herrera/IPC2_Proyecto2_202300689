# main.py
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import threading
from simulation import sistema
from models import Cliente
from graphviz_report import generar_reporte_cola, generar_reporte_escritorios

# Configuración de colores y estilos
BG_COLOR = "#f0f8ff"       # Azul muy claro
BTN_BG_COLOR = "#4682b4"   # Azul acero
BTN_FG_COLOR = "white"
FONT_NAME = "Helvetica"

def cargar_configuracion_sistema():
    xml_file = filedialog.askopenfilename(title="Seleccione archivo de configuración del sistema", filetypes=[("XML files", "*.xml")])
    if xml_file:
        try:
            sistema.cargar_configuracion_sistema(xml_file)
            messagebox.showinfo("Éxito", "Archivo de configuración cargado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar archivo: {e}")

def cargar_configuracion_inicial():
    xml_file = filedialog.askopenfilename(title="Seleccione archivo de configuración inicial", filetypes=[("XML files", "*.xml")])
    if xml_file:
        try:
            sistema.cargar_configuracion_inicial(xml_file)
            messagebox.showinfo("Éxito", "Archivo de configuración inicial cargado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar archivo: {e}")

def ver_estado_punto():
    id_empresa = simpledialog.askstring("Empresa", "Ingrese el ID de la empresa:")
    id_punto = simpledialog.askstring("Punto de atención", "Ingrese el ID del punto de atención:")
    estado = sistema.ver_estado_punto(id_empresa, id_punto)
    messagebox.showinfo("Estado del Punto", estado)

def activar_escritorio():
    id_empresa = simpledialog.askstring("Empresa", "Ingrese el ID de la empresa:")
    id_punto = simpledialog.askstring("Punto de atención", "Ingrese el ID del punto de atención:")
    id_escritorio = simpledialog.askstring("Escritorio", "Ingrese el ID del escritorio a activar:")
    resultado = sistema.activar_escritorio(id_empresa, id_punto, id_escritorio)
    messagebox.showinfo("Activar Escritorio", resultado)

def desactivar_escritorio():
    id_empresa = simpledialog.askstring("Empresa", "Ingrese el ID de la empresa:")
    id_punto = simpledialog.askstring("Punto de atención", "Ingrese el ID del punto de atención:")
    id_escritorio = simpledialog.askstring("Escritorio", "Ingrese el ID del escritorio a desactivar:")
    resultado = sistema.desactivar_escritorio(id_empresa, id_punto, id_escritorio)
    messagebox.showinfo("Desactivar Escritorio", resultado)

def atender_cliente():
    id_empresa = simpledialog.askstring("Empresa", "Ingrese el ID de la empresa:")
    id_punto = simpledialog.askstring("Punto de atención", "Ingrese el ID del punto de atención:")
    resultado = sistema.atender_cliente(id_empresa, id_punto)
    messagebox.showinfo("Atender Cliente", resultado)

def solicitud_atencion():
    id_empresa = simpledialog.askstring("Empresa", "Ingrese el ID de la empresa:")
    id_punto = simpledialog.askstring("Punto de atención", "Ingrese el ID del punto de atención:")
    dpi = simpledialog.askstring("Cliente", "Ingrese el DPI del cliente:")
    nombre = simpledialog.askstring("Cliente", "Ingrese el nombre del cliente:")

    # Solicitar las transacciones en el formato: "IDTransaccion:cantidad, IDTransaccion:cantidad"
    transacciones_input = simpledialog.askstring("Transacciones", 
        "Ingrese las transacciones a realizar (formato:\nIDTransaccion:cantidad, IDTransaccion:cantidad)\nEjemplo: T001:1, T002:2")
    cliente = Cliente(dpi, nombre)
    
    if transacciones_input:
        empresa_obj = sistema.buscar_empresa(id_empresa)
        if not empresa_obj:
            messagebox.showerror("Error", "Empresa no encontrada.")
            return
        transacciones_list = transacciones_input.split(',')
        for trans in transacciones_list:
            trans = trans.strip()
            if ':' in trans:
                tid, cantidad = trans.split(':')
                tid = tid.strip()
                cantidad = cantidad.strip()
                trans_obj = None
                for t in empresa_obj.transacciones:
                    if t.id == tid:
                        trans_obj = t
                        break
                if trans_obj is None:
                    messagebox.showerror("Error", f"Transacción {tid} no encontrada en la empresa.")
                    return
                cliente.agregar_transaccion(trans_obj, cantidad)
            else:
                messagebox.showerror("Error", "Formato de transacciones incorrecto. Use IDTransaccion:cantidad")
                return
    resultado = sistema.solicitud_atencion(id_empresa, id_punto, cliente)
    messagebox.showinfo("Solicitud de Atención", resultado)

def simular_actividad():
    id_empresa = simpledialog.askstring("Empresa", "Ingrese el ID de la empresa:")
    id_punto = simpledialog.askstring("Punto de atención", "Ingrese el ID del punto de atención:")
    def run_simulation():
        resultado = sistema.simular_actividad(id_empresa, id_punto)
        messagebox.showinfo("Simulación", resultado)
    threading.Thread(target=run_simulation).start()

def generar_reportes():
    id_empresa = simpledialog.askstring("Empresa", "Ingrese el ID de la empresa:")
    id_punto = simpledialog.askstring("Punto de atención", "Ingrese el ID del punto de atención:")
    empresa = sistema.buscar_empresa(id_empresa)
    if not empresa:
        messagebox.showerror("Error", "Empresa no encontrada.")
        return
    punto = None
    for p in empresa.puntos_atencion:
        if p.id == id_punto:
            punto = p
            break
    if not punto:
        messagebox.showerror("Error", "Punto de atención no encontrado.")
        return
    reporte1 = generar_reporte_cola(punto)
    reporte2 = generar_reporte_escritorios(punto)
    messagebox.showinfo("Reportes Generados", f"{reporte1}\n{reporte2}")

def limpiar_sistema():
    sistema.limpiar_sistema()
    messagebox.showinfo("Sistema", "El sistema se ha limpiado.")

# Configuración de la ventana principal con mejoras visuales
root = tk.Tk()
root.title("Sistema de Atención al Cliente - Soluciones Guatemaltecas S.A.")
root.geometry("700x500")
root.configure(bg=BG_COLOR)

# Etiqueta de bienvenida
lbl_welcome = tk.Label(root, text="Bienvenido al Sistema de Atención al Cliente", font=(FONT_NAME, 18, "bold"), bg=BG_COLOR, fg="#333333")
lbl_welcome.pack(pady=20)

# Menú principal con estilo
menu_bar = tk.Menu(root, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR)
root.config(menu=menu_bar)

# Menú de Configuración
config_menu = tk.Menu(menu_bar, tearoff=0, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR)
menu_bar.add_cascade(label="Configuración", menu=config_menu)
config_menu.add_command(label="Limpiar Sistema", command=limpiar_sistema)
config_menu.add_command(label="Cargar Archivo de Configuración", command=cargar_configuracion_sistema)
config_menu.add_command(label="Cargar Archivo de Configuración Inicial", command=cargar_configuracion_inicial)

# Menú de Puntos de Atención
punto_menu = tk.Menu(menu_bar, tearoff=0, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR)
menu_bar.add_cascade(label="Puntos de Atención", menu=punto_menu)
punto_menu.add_command(label="Ver Estado del Punto", command=ver_estado_punto)
punto_menu.add_command(label="Activar Escritorio", command=activar_escritorio)
punto_menu.add_command(label="Desactivar Escritorio", command=desactivar_escritorio)
punto_menu.add_command(label="Atender Cliente", command=atender_cliente)
punto_menu.add_command(label="Solicitud de Atención", command=solicitud_atencion)
punto_menu.add_command(label="Simular Actividad", command=simular_actividad)
punto_menu.add_command(label="Generar Reportes", command=generar_reportes)

root.mainloop()
