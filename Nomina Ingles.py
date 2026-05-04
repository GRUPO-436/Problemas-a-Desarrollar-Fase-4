# DANIEL ALBERTO ROCHA MARTINEZ
# cc: 86088347
#PROGRAMACION


# Import GUI libraries Importa la libreria principal para crear interfaces gráficas
import tkinter as tk
from tkinter import ttk, messagebox #importa componenetes adicionales de tkinter (tabla y mensajes emergentes)

# ==========================================
# BASE CLASS
# ==========================================
class Empleado:

    def __init__(self, nombre, cedula, salario_base): # Contructor de la clase
        self.nombre = nombre              # Employee name   "Guarda el nombre del empleado"
        self.cedula = cedula              # Employee ID     "Guarda la Cedula"
        self.salario_base = salario_base  # Base salary     "Guarda el Salario Base"  

    def calcular_salario(self):           # Es el Metodo Virtual (es obligatorio en clases hijas) 
        raise NotImplementedError()       # Virtual method  Obliga a implementar en sub clases

    def mostrar_informacion(self, detalle=False, incluir_bonos=False, extra=False):  # Metodo para Mostrar Informacion Con diferentes Niveles

        info = f"Name: {self.nombre}\nID: {self.cedula}" # Informacion Basica

        if detalle: # si se pide detalle muestra el salario total
            info += f"\nTotal Salary: {self.calcular_salario()}"

        if incluir_bonos and hasattr(self, "obtener_bonificaciones"): # Si se piden la informacion de bonos y el objeto tiene ese metodo
            info += f"\nBonuses: {self.obtener_bonificaciones()}"

        if extra:  # Informacion adicinal del salario base
            info += f"\nBase Salary: {self.salario_base}"

        return info # Retorna el texto Final


# ==========================================
# MIXIN
# ==========================================
class Bonificable:

    def __init__(self): # Constructor de Bonificacion
        self.bonificaciones = [] # Lista vacia para Guardar Bonos

    def agregar_bonificacion(self, monto):  # Metodo para agregar bonificaciones
        self.bonificaciones.append(monto)

    def obtener_bonificaciones(self):  # Metodo para obtener total de bonificaciones
        return sum(self.bonificaciones)


# ==========================================
# FULL-TIME EMPLOYEES
# ==========================================
class EmpleadoTiempoCompleto(Empleado, Bonificable):

    def __init__(self, nombre, cedula, salario_base, bonificacion):
        Empleado.__init__(self, nombre, cedula, salario_base) # Inicializa clase base
        Bonificable.__init__(self)                            # Inicializa bonificaciones 
        self.bonificacion = bonificacion                      # Bonificacion fija

    def calcular_salario(self): # Calcula salario Total
        return self.salario_base + self.bonificacion + self.obtener_bonificaciones()

    def mostrar_informacion(self, detalle=False, incluir_bonos=False, extra=False):  # Sobrescribe mostrar informacion 
        info = super().mostrar_informacion(detalle, incluir_bonos, extra)

        if extra:
            info += f"\nFixed Bonus: {self.bonificacion}"  # Agrega bonificacion fija si se puede pide detalle completo

        return info
    
# ==========================================
#  HOURLY EMPLOYEES
# ==========================================


class EmpleadoPorHoras(Empleado, Bonificable):

    def __init__(self, nombre, cedula, costo_hora, horas):
        Empleado.__init__(self, nombre, cedula, costo_hora)
        Bonificable.__init__(self)
        self.horas = horas  # Numero de Horas trabajadas

    def calcular_salario(self): # Calcula el salario
        return (self.salario_base * self.horas) + self.obtener_bonificaciones()

    def mostrar_informacion(self, detalle=False, incluir_bonos=False, extra=False):
        info = super().mostrar_informacion(detalle, incluir_bonos, extra)

        if extra:  # Muestra detalles especificos
            info += f"\nHours Worked: {self.horas}"
            info += f"\nHourly Rate: {self.salario_base}"

        return info

# ==========================================
# COMMISSION-BASED EMPLOYEES
# ==========================================

class EmpleadoComision(Empleado, Bonificable):

    def __init__(self, nombre, cedula, salario_base, porcentaje):
        Empleado.__init__(self, nombre, cedula, salario_base)
        Bonificable.__init__(self)
        self.porcentaje = porcentaje
        self.ventas = 1000  # valor base de ventas

    def calcular_salario(self):  # Calcula salario
        return self.salario_base + (self.ventas * self.porcentaje) + self.obtener_bonificaciones()

    def mostrar_informacion(self, detalle=False, incluir_bonos=False, extra=False):
        info = super().mostrar_informacion(detalle, incluir_bonos, extra)

        if extra:  # Detalles adicionales
            info += f"\nCommission Rate: {self.porcentaje}"
            info += f"\nSales Base: {self.ventas}"

        return info


# ==========================================
# SYSTEM
# ==========================================
class SistemaNomina:

    def __init__(self):
        self.empleados = []   # Lista de empleados

    def agregar(self, emp):  # Agrega empleado
        self.empleados.append(emp)

    def eliminar(self, index): # Elimina el ampleado que selecione
        if index >= 0:
            self.empleados.pop(index)

    def total(self): # Calcula total usando polimorfismo
        total = 0
        lista = []

        for e in self.empleados:  # Recorre todos los empleados
            salario = e.calcular_salario()   # Polymorphism cada objeto responde distinto
            lista.append((e.nombre, salario))
            total += salario

        return total, lista


# ==========================================
# LOGIN
# ==========================================
def login():
    if user_entry.get() == "programacion" and pass_entry.get() == "programacion": # verifica usuario y contraseña
        login_window.destroy() # Cierra Login
        iniciar_app()          # Abre app principal
    else:
        messagebox.showerror("Error", "Invalid credentials")

#Ventana de login
login_window = tk.Tk()
login_window.title("Login")

tk.Label(login_window, text="User").pack()
user_entry = tk.Entry(login_window)
user_entry.pack()

tk.Label(login_window, text="Password").pack()
pass_entry = tk.Entry(login_window, show="*")
pass_entry.pack()

tk.Button(login_window, text="Login", command=login).pack()


# ==========================================
# MAIN INTERFACE
# ==========================================
def iniciar_app():

    sistema = SistemaNomina()   # Crea el Sistema

    root = tk.Tk()
    root.title("Payroll System")
    root.geometry("900x600")

    # Tabla
    tree = ttk.Treeview(root, columns=("Name", "ID", "Salary"), show="headings") # Crea una tabla, define tres columnas y hace que solo se vean los encabezados
    tree.heading("Name", text="Name") # Define el titulo visible de la primera columna
    tree.heading("ID", text="ID") # Define el encabezado de la segunda columna con el texto ID
    tree.heading("Salary", text="Salary") # Define el encabezado de la tercera columna son el texto salary
    tree.pack(fill="both", expand=True) # Hace que se expanda horizontal y vertical y que se aproveche el espacio disponible

    def actualizar():  # Actualiza la Tabla
        tree.delete(*tree.get_children()) #  Borra todas las filas actuales de la tabla, obtiene todos los elementos insertados
        for i, e in enumerate(sistema.empleados): # Recorre la lista de empleados almacenada
            tree.insert("", "end", iid=i, # inserta una nueva fila en la tabla
                        values=(e.nombre, e.cedula, e.calcular_salario())) # Define los valores que se mostraran en la fila

    # FORM
    frame = tk.Frame(root) # Crea un contenedor dentro de la ventana root para organizar los campos del formulario
    frame.pack() # coloca el frame en la ventana

    tk.Label(frame, text="Name").grid(row=0, column=0) # Crea una etiqueta con el texto name dentro de frame
    entry_nombre = tk.Entry(frame) # Crea una ventana de texto para que el usuario escriba el nombre
    entry_nombre.grid(row=0, column=1) # Ubica esa ventana de texto en la fila 0, columna 1

    tk.Label(frame, text="ID").grid(row=1, column=0) # Crea una etiqueta con el texto ID en la fila 1 columna 0
    entry_cedula = tk.Entry(frame) # Crea una ventana de texto para ingresar la cedula 
    entry_cedula.grid(row=1, column=1) # ubica la ventana en la fila 1, columna 1

    tk.Label(frame, text="Base Salary").grid(row=2, column=0)# Crea una etiqueta con el texto Base Salary
    entry_salario = tk.Entry(frame) # Crea una ventana de texto para ingresar el salario base
    entry_salario.grid(row=2, column=1) # Ubica la ventana de texto en la fila 2, columna 1

    tk.Label(frame, text="Employee Type").grid(row=3, column=0)# Crea una etiqueta que indica el tipo de empleado
    combo = ttk.Combobox(frame, values=["Full Time", "Hourly", "Commission"]) # Crea una lista desplegable con tre opsiones: Tiempo completo, por horas y comision
    combo.grid(row=3, column=1) # Ubica el Combobox en la fila 3, columna 1
    combo.current(0) # Hace que la primera opción aparezca seleccionada por defecto

    label1 = tk.Label(frame) #Crea una etiqueta vacia, se usara despues para mostrar un campo dinamico segun el tipo de empleado
    entry1 = tk.Entry(frame) # Crea una ventana de texto asociada a label1

    label2 = tk.Label(frame) # Crea una segunda etiqueta vacia para otro posible campo dinamico
    entry2 = tk.Entry(frame) # Crea una segunda ventana de texto asociada a label2

    def actualizar_form(): # Define una funcion que cambia los campos visibles del formulario segun el tipo de empleado
        # Oculta los campos dinamicos
        label1.grid_forget() 
        entry1.grid_forget()
        label2.grid_forget()
        entry2.grid_forget()

        if combo.get() == "Full Time": # Verifica si se selecciona tiempo completo
            label1.config(text="Bonus") # Cambia el texto del campo "Bonus"
            label1.grid(row=4, column=0) # Muestra el campo en pantalla
            entry1.grid(row=4, column=1) # Muestra el campo en pantalla

        elif combo.get() == "Hourly": # Si es por horas
            label1.config(text="Hours") # Campo para escribir las horas trabajadas
            label1.grid(row=4, column=0) # Muestra ambos campos
            entry1.grid(row=4, column=1) # Muestra ambos campos
            label2.config(text="Hourly Rate") # Campo para costo por hora
            label2.grid(row=5, column=0) # Muestra ambos campos
            entry2.grid(row=5, column=1) # Muestra ambos campos

        elif combo.get() == "Commission": # Si es por comision
            label1.config(text="Percentage") # Campo para el porcentaje de la comision
            label1.grid(row=4, column=0) # Muestra el campo
            entry1.grid(row=4, column=1) # Muestra el campo

    combo.bind("<<ComboboxSelected>>", lambda e: actualizar_form()) # Vincula un evento al combobox, cada vez que el usuario cambia el tipo de empleado, se ejecuta actualizar para cambiar los campos del formulario
    actualizar_form() # ejecuta la funsion inmediatmente al iniciar, para que el formulario se configure correctamente desde el inicio

    # ADD EMPLOYEE (NO AUTO INFO)
    def agregar(): # Define la funsion que se ejecuta cuando se presiona el boton Add
        try: # Inicia un bloque de control de errores
            nombre = entry_nombre.get() # Obtiene el texto ingresado en el campo del nombre
            cedula = entry_cedula.get() # Obtiene el texto ingresado en el campo ID

            if combo.get() == "Full Time": # Verifica si el usuario selecciono Full Time en el menu desplegable
                # Crea un objeto de tipo Empleado Tiempo Completo
                emp = EmpleadoTiempoCompleto(nombre, cedula,
                                              float(entry_salario.get()), # Salario base
                                              float(entry1.get())) # Bonificacion

            elif combo.get() == "Hourly": # Verifica si seleccionó Hourly
                # Crea un empleado por horas
                emp = EmpleadoPorHoras(nombre, cedula,
                                        float(entry2.get()), # Costo por hora
                                        float(entry1.get())) # Horas trabajadas

            else: # Si no es ninguno de los anteriores es comision
                # Crea un empleado por comision
                emp = EmpleadoComision(nombre, cedula,
                                        float(entry_salario.get()), # Salario base
                                        float(entry1.get())) # Porcentaje de comision

            sistema.agregar(emp) # Agrega el empleado creado a la lista del sistema
            actualizar() # Actualiza la tabla para mostrar el nuevo empleado

        except:  # Captura cualquier error ocurrido en el bloque try
            messagebox.showerror("Error", "Invalid data") # Muestra un mensaje si hubo datos mal ingresados

    def eliminar(): # Funcion para eliminar a un empleado
        if tree.selection(): # Verifica si hay un empleado seleccionado en la tabla
            sistema.eliminar(int(tree.selection()[0])) # Obtiene el indice del elemento seleccionado y lo elimina de la lista
            actualizar() # Actualiza la tabla despues de eliminar a un empleado

    def agregar_bono(): # Funsion para agregar bonificaciones a un empleado
        if tree.selection(): # Verifica que haya un empleado seleccionado
            emp = sistema.empleados[int(tree.selection()[0])] # Obtiene el objeto empleado seleccionado en la tabla
            emp.agregar_bonificacion(float(entry_bono.get())) # Agrega una bonificación al empleado, toma el valor del campo, lo convierte a numero y lo guarda en la lista de bonificaciones

    def mostrar_basico(): # Funsion para mostrar informacion basica
        if tree.selection(): # Verifica que haya un empleado seleccionado
            emp = sistema.empleados[int(tree.selection()[0])] # Obtiene el empleado seleccionado
            messagebox.showinfo("Info", emp.mostrar_informacion()) # Muestra una ventana con el nombre y cedula

    def mostrar_salario(): # Define una función para mostrar la informacion del empleado con salario total
        if tree.selection(): # Verifica si hay un empleado seleccionado en la tabla
            emp = sistema.empleados[int(tree.selection()[0])] # Obtiene el empleado seleccionado
            messagebox.showinfo("Info", emp.mostrar_informacion(True)) # Muestra una ventana con el nombre, cedula y salario total

    def mostrar_completo(): # Funsion para mostrar la informacion completa del empleado
        if tree.selection(): # Verifica que haya un empleado seleccionado
            emp = sistema.empleados[int(tree.selection()[0])] # Obtiene el empleado seleccionado
            messagebox.showinfo("Info", emp.mostrar_informacion(True, True, True)) # Muestra la informacion completa: Nombre, cedula, salario total, bonificaciones, salario base y datos especificos como horas, comisiones

    def mostrar_total(): # Funsion para calcula y mostrar toda la nomina
        total, lista = sistema.total() # Llama al metodo total del sistema, suma el total de salarios y da una lista de los empleados

        text = "PAYROLL:\n\n" # Crea el texto inicial del mensaje
        for nombre, salario in lista: # Recorre la lista de los empleados
            text += f"{nombre}: {salario}\n" # Agrega cada empleado al texto con el nombre y salario

        text += f"\nTOTAL: {total}" # Agrega el total final de la nomina

        messagebox.showinfo("Payroll", text) # Muestra todo en una ventana emergente

    tk.Button(frame, text="Add", command=agregar).grid(row=6, column=0) # Boton para agregar empleados
    tk.Button(frame, text="Delete", command=eliminar).grid(row=6, column=1) # Boton para eliminar el empleado seleccionado

    tk.Label(frame, text="Bonus").grid(row=7, column=0) # Etiqueta que indica el campo de bonificacion
    entry_bono = tk.Entry(frame) # Ventana de texto para ingresar el valor del bono
    entry_bono.grid(row=7, column=1) # Ubica el campo en la interaz

    tk.Button(frame, text="Add Bonus", command=agregar_bono).grid(row=8, column=0) # Boton para agregar una bonificacion al empleado seleccionado

    tk.Button(root, text="Show Basic", command=mostrar_basico).pack() # Boton que muestra la informacion basica del empleado
    tk.Button(root, text="Show Salary", command=mostrar_salario).pack() # Boton que muestra informacion con salario total
    tk.Button(root, text="Show Complete", command=mostrar_completo).pack() # Boton que muestra toda la informacion detallada
    tk.Button(root, text="Total Payroll", command=mostrar_total).pack() # Boton que calcula y muestra la nomina completa

    root.mainloop() # Mantiene la ventana abierta esperando interaccion


login_window.mainloop() # Es la primera ventana que aparece