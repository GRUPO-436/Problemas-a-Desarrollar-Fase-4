# DANIEL ALBERTO ROCHA MARTINEZ
# cc: 86088347
#
#
#
#
# Ejercicio 1: Sistema Integral de Gestión de Clientes, Servicios y Reservas
#PROGRAMACION

# Importa la librería Tkinter para crear interfaces gráficas
import tkinter as tk

# Importa componentes adicionales de Tkinter: tablas, listas desplegables y mensajes
from tkinter import ttk, messagebox

# Importa ABC y abstractmethod para crear clases abstractas
from abc import ABC, abstractmethod

# Importa datetime para registrar fecha y hora en el archivo de logs
from datetime import datetime

# Importa re para validar el formato del correo electrónico con expresiones regulares
import re


# =====================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================

# Clase base para todos los errores del sistema
class ErrorSistema(Exception):
    pass


# Error personalizado para fallos de inicio de sesión
class LoginError(ErrorSistema):
    pass


# Error personalizado para problemas con clientes
class ClienteError(ErrorSistema):
    pass


# Error personalizado para problemas con servicios
class ServicioError(ErrorSistema):
    pass


# Error personalizado para problemas con reservas
class ReservaError(ErrorSistema):
    pass


# =====================================================
# REGISTRO DE LOGS
# =====================================================

# Función para guardar eventos y errores en el archivo logs.txt
def registrar_log(mensaje):
    # Abre el archivo logs.txt en modo agregar, sin borrar lo anterior
    with open("logs.txt", "a", encoding="utf-8") as archivo:
        # Obtiene la fecha y hora actual
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Escribe el mensaje en el archivo con fecha y hora
        archivo.write(f"[{fecha}] {mensaje}\n")


# =====================================================
# FUNCIONES DE VALIDACIÓN
# =====================================================

# Valida que un texto no esté vacío y tenga mínimo 3 caracteres
def validar_texto(valor, campo):
    # Verifica si el campo está vacío
    if not valor.strip():
        raise ValueError(f"El campo {campo} no puede estar vacío.")

    # Verifica si el campo tiene menos de 3 caracteres
    if len(valor.strip()) < 3:
        raise ValueError(f"El campo {campo} debe tener mínimo 3 caracteres.")

    # Retorna el texto limpio sin espacios al inicio o final
    return valor.strip()


# Valida que el documento tenga solo números y mínimo 6 dígitos
def validar_documento(documento):
    # Verifica si el documento contiene solo números
    if not documento.isdigit():
        raise ValueError("El documento solo debe contener números.")

    # Verifica longitud mínima del documento
    if len(documento) < 6:
        raise ValueError("El documento debe tener mínimo 6 dígitos.")

    # Retorna el documento validado
    return documento


# Valida que el correo tenga formato correcto
def validar_correo(correo):
    # Patrón básico para validar correo electrónico
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    # Verifica si el correo coincide con el patrón
    if not re.match(patron, correo):
        raise ValueError("El correo electrónico no es válido.")

    # Retorna el correo validado
    return correo


# Valida que el precio sea numérico y mayor que cero
def validar_precio(precio):
    # Intenta convertir el precio a decimal
    try:
        precio = float(precio)

    # Si no se puede convertir, genera error
    except ValueError:
        raise ValueError("El precio debe ser numérico.")

    # Verifica que el precio sea positivo
    if precio <= 0:
        raise ValueError("El precio debe ser mayor que cero.")

    # Retorna el precio validado
    return precio


# Valida que la duración sea número entero y mayor que cero
def validar_duracion(duracion):
    # Intenta convertir la duración a entero
    try:
        duracion = int(duracion)

    # Si no se puede convertir, genera error
    except ValueError:
        raise ValueError("La duración debe ser un número entero.")

    # Verifica que la duración sea positiva
    if duracion <= 0:
        raise ValueError("La duración debe ser mayor que cero.")

    # Retorna la duración validada
    return duracion


# =====================================================
# CLASE ABSTRACTA GENERAL
# =====================================================

# Clase abstracta base para obligar a las clases hijas a implementar mostrar_info()
class EntidadSistema(ABC):

    # Método abstracto que debe ser implementado por las clases hijas
    @abstractmethod
    def mostrar_info(self):
        pass


# =====================================================
# CLASE USUARIO
# =====================================================

# Clase para manejar el usuario administrador del sistema
class Usuario:

    # Constructor de usuario
    def __init__(self, usuario, contrasena):
        # Atributo privado para guardar usuario
        self.__usuario = usuario

        # Atributo privado para guardar contraseña
        self.__contrasena = contrasena

    # Método para validar usuario y contraseña
    def autenticar(self, usuario, contrasena):
        # Retorna True si usuario y contraseña coinciden
        return self.__usuario == usuario and self.__contrasena == contrasena


# =====================================================
# CLASE CLIENTE
# =====================================================

# Cliente hereda de EntidadSistema
class Cliente(EntidadSistema):

    # Constructor de Cliente
    def __init__(self, nombre, documento, correo):
        try:
            # Valida y guarda el nombre como atributo privado
            self.__nombre = validar_texto(nombre, "nombre")

            # Valida y guarda el documento como atributo privado
            self.__documento = validar_documento(documento)

            # Valida y guarda el correo como atributo privado
            self.__correo = validar_correo(correo)

        # Captura errores de validación
        except ValueError as error:
            # Convierte el error general en error personalizado de cliente
            raise ClienteError(error)

    # Retorna el nombre del cliente
    def get_nombre(self):
        return self.__nombre

    # Retorna el documento del cliente
    def get_documento(self):
        return self.__documento

    # Retorna el correo del cliente
    def get_correo(self):
        return self.__correo

    # Devuelve la información del cliente en texto
    def mostrar_info(self):
        return f"{self.__nombre} | Doc: {self.__documento} | Correo: {self.__correo}"


# =====================================================
# CLASE ABSTRACTA SERVICIO
# =====================================================

# Clase abstracta Servicio
class Servicio(EntidadSistema):

    # Constructor de Servicio
    def __init__(self, nombre, precio_base, disponible=True):
        try:
            # Valida y guarda el nombre del servicio
            self.nombre = validar_texto(nombre, "nombre del servicio")

            # Valida y guarda el precio base
            self.precio_base = validar_precio(precio_base)

            # Guarda si el servicio está disponible
            self.disponible = disponible

        # Captura errores de validación
        except ValueError as error:
            # Lanza error personalizado de servicio
            raise ServicioError(error)

    # Método abstracto para calcular costo
    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        pass

    # Método abstracto para validar parámetros
    @abstractmethod
    def validar_parametros(self, duracion):
        pass


# Servicio especializado para reservar salas
class ReservaSala(Servicio):

    # Valida duración específica para salas
    def validar_parametros(self, duracion):
        # Valida duración como número entero positivo
        duracion = validar_duracion(duracion)

        # Limita la reserva de sala a máximo 8 horas
        if duracion > 8:
            raise ServicioError("La reserva de sala no puede superar 8 horas.")

        # Retorna duración válida
        return duracion

    # Calcula el costo del servicio
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        # Valida la duración
        duracion = self.validar_parametros(duracion)

        # Calcula subtotal
        subtotal = self.precio_base * duracion

        # Calcula total con impuesto y descuento
        return subtotal + (subtotal * impuesto) - descuento

    # Muestra información del servicio
    def mostrar_info(self):
        return f"Reserva de sala | {self.nombre} | ${self.precio_base:,.0f}/hora"


# Servicio especializado para alquiler de equipos
class AlquilerEquipo(Servicio):

    # Valida duración específica para alquiler de equipos
    def validar_parametros(self, duracion):
        # Valida duración
        duracion = validar_duracion(duracion)

        # Limita alquiler a máximo 15 horas
        if duracion > 15:
            raise ServicioError("El alquiler de equipo no puede superar 15 horas.")

        # Retorna duración válida
        return duracion

    # Calcula costo del alquiler
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        # Valida duración
        duracion = self.validar_parametros(duracion)

        # Calcula subtotal
        subtotal = self.precio_base * duracion

        # Aplica recargo del 10%
        recargo = subtotal * 0.10

        # Retorna total
        return subtotal + recargo + (subtotal * impuesto) - descuento

    # Muestra información del servicio
    def mostrar_info(self):
        return f"Alquiler de equipo | {self.nombre} | ${self.precio_base:,.0f}/hora"


# Servicio especializado para asesorías
class AsesoriaEspecializada(Servicio):

    # Valida duración específica para asesorías
    def validar_parametros(self, duracion):
        # Valida duración
        duracion = validar_duracion(duracion)

        # Limita asesoría a máximo 5 horas
        if duracion > 5:
            raise ServicioError("La asesoría especializada no puede superar 5 horas.")

        # Retorna duración válida
        return duracion

    # Calcula costo de asesoría
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        # Valida duración
        duracion = self.validar_parametros(duracion)

        # Calcula subtotal
        subtotal = self.precio_base * duracion

        # Valor adicional por experto
        valor_experto = 50000

        # Retorna total
        return subtotal + valor_experto + (subtotal * impuesto) - descuento

    # Muestra información del servicio
    def mostrar_info(self):
        return f"Asesoría especializada | {self.nombre} | ${self.precio_base:,.0f}/hora"


# =====================================================
# CLASE RESERVA
# =====================================================

# Clase Reserva
class Reserva(EntidadSistema):

    # Contador automático para códigos de reserva
    contador = 1

    # Constructor de reserva
    def __init__(self, cliente, servicio, duracion):
        # Valida que exista cliente
        if cliente is None:
            raise ReservaError("Debe seleccionar un cliente.")

        # Valida que exista servicio
        if servicio is None:
            raise ReservaError("Debe seleccionar un servicio.")

        # Valida disponibilidad del servicio
        if not servicio.disponible:
            raise ReservaError("El servicio no está disponible.")

        try:
            # Valida duración de la reserva
            self.duracion = validar_duracion(duracion)

        # Captura error de duración
        except ValueError as error:
            raise ReservaError(error)

        # Asigna código automático
        self.codigo = Reserva.contador

        # Incrementa contador
        Reserva.contador += 1

        # Guarda cliente
        self.cliente = cliente

        # Guarda servicio
        self.servicio = servicio

        # Estado inicial de la reserva
        self.estado = "Pendiente"

    # Confirma reserva
    def confirmar(self):
        # No permite confirmar una reserva cancelada
        if self.estado == "Cancelada":
            raise ReservaError("No se puede confirmar una reserva cancelada.")

        # Cambia estado
        self.estado = "Confirmada"

        # Registra evento en logs
        registrar_log(f"Reserva #{self.codigo} confirmada.")

    # Cancela reserva
    def cancelar(self):
        # No permite cancelar dos veces
        if self.estado == "Cancelada":
            raise ReservaError("La reserva ya estaba cancelada.")

        # Cambia estado
        self.estado = "Cancelada"

        # Registra evento
        registrar_log(f"Reserva #{self.codigo} cancelada.")

    # Procesa el pago de la reserva
    def procesar_pago(self):
        try:
            # Calcula costo usando polimorfismo según el tipo de servicio
            total = self.servicio.calcular_costo(
                self.duracion,
                impuesto=0.19,
                descuento=10000
            )

        # Captura errores del servicio
        except ServicioError as error:
            # Encadena excepción de servicio como error de reserva
            raise ReservaError("No fue posible procesar el pago.") from error

        # Si no hay error, registra pago
        else:
            registrar_log(f"Pago reserva #{self.codigo}. Total: ${total:,.0f}")
            return total

        # Siempre se ejecuta al finalizar
        finally:
            registrar_log(f"Proceso de pago finalizado para reserva #{self.codigo}.")

    # Muestra información de reserva
    def mostrar_info(self):
        return (
            f"#{self.codigo} | Cliente: {self.cliente.get_nombre()} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} horas | Estado: {self.estado}"
        )


# =====================================================
# SISTEMA PRINCIPAL
# =====================================================

# Clase que administra clientes, servicios y reservas
class SistemaSoftwareFJ:

    # Constructor del sistema
    def __init__(self):
        # Crea usuario administrador
        self.usuario_admin = Usuario("programacion", "programacion")

        # Lista interna de clientes
        self.clientes = []

        # Lista interna de servicios
        self.servicios = []

        # Lista interna de reservas
        self.reservas = []

    # Valida inicio de sesión
    def login(self, usuario, contrasena):
        # Si las credenciales no coinciden, lanza error
        if not self.usuario_admin.autenticar(usuario, contrasena):
            raise LoginError("Usuario o contraseña incorrectos.")

        # Registra inicio exitoso
        registrar_log("Inicio de sesión exitoso.")

    # Agrega cliente al sistema
    def agregar_cliente(self, nombre, documento, correo):
        # Crea objeto cliente
        cliente = Cliente(nombre, documento, correo)

        # Agrega cliente a la lista
        self.clientes.append(cliente)

        # Registra evento
        registrar_log(f"Cliente registrado: {cliente.get_nombre()}")

    # Agrega servicio al sistema
    def agregar_servicio(self, tipo, nombre, precio):
        # Crea servicio según el tipo seleccionado
        if tipo == "Reserva de sala":
            servicio = ReservaSala(nombre, precio)

        elif tipo == "Alquiler de equipo":
            servicio = AlquilerEquipo(nombre, precio)

        elif tipo == "Asesoría especializada":
            servicio = AsesoriaEspecializada(nombre, precio)

        else:
            raise ServicioError("Tipo de servicio no válido.")

        # Agrega servicio a la lista
        self.servicios.append(servicio)

        # Registra evento
        registrar_log(f"Servicio registrado: {servicio.nombre}")

    # Crea reserva usando índices seleccionados desde la interfaz
    def crear_reserva(self, indice_cliente, indice_servicio, duracion):
        # Obtiene cliente seleccionado
        cliente = self.clientes[indice_cliente]

        # Obtiene servicio seleccionado
        servicio = self.servicios[indice_servicio]

        # Crea reserva
        reserva = Reserva(cliente, servicio, duracion)

        # Agrega reserva a la lista
        self.reservas.append(reserva)

        # Registra evento
        registrar_log(f"Reserva creada #{reserva.codigo}")

    # Carga datos de prueba
    def cargar_datos_prueba(self):
        # Agrega clientes de prueba
        self.clientes.append(Cliente("Daniel Rocha", "123456789", "daniel@email.com"))
        self.clientes.append(Cliente("Laura Gómez", "987654321", "laura@email.com"))

        # Agrega servicios de prueba
        self.servicios.append(ReservaSala("Sala VIP", 80000))
        self.servicios.append(AlquilerEquipo("Computador portátil", 50000))
        self.servicios.append(AsesoriaEspecializada("Asesoría en software", 120000))

        # Registra evento
        registrar_log("Datos de prueba cargados.")


# =====================================================
# INTERFAZ GRÁFICA
# =====================================================

# Clase principal de la aplicación gráfica
class App:

    # Constructor de la interfaz
    def __init__(self, root):
        # Crea el sistema
        self.sistema = SistemaSoftwareFJ()

        # Guarda ventana principal
        self.root = root

        # Título de ventana
        self.root.title("Software FJ - Sistema de Gestión")

        # Tamaño de ventana
        self.root.geometry("900x600")

        # Evita cambiar tamaño
        self.root.resizable(False, False)

        # Muestra login
        self.mostrar_login()

    # Limpia todos los elementos de la ventana
    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Muestra pantalla de login
    def mostrar_login(self):
        # Limpia ventana
        self.limpiar_ventana()

        # Crea marco principal
        frame = tk.Frame(self.root, padx=30, pady=30)
        frame.pack(expand=True)

        # Título
        tk.Label(frame, text="SOFTWARE FJ", font=("Arial", 24, "bold")).pack(pady=10)

        # Subtítulo
        tk.Label(frame, text="Inicio de sesión", font=("Arial", 14)).pack(pady=10)

        # Etiqueta usuario
        tk.Label(frame, text="Usuario:").pack()

        # Caja de texto para usuario
        self.usuario_entry = tk.Entry(frame, width=30)
        self.usuario_entry.pack(pady=5)

        # Etiqueta contraseña
        tk.Label(frame, text="Contraseña:").pack()

        # Caja de texto para contraseña
        self.contrasena_entry = tk.Entry(frame, width=30, show="*")
        self.contrasena_entry.pack(pady=5)

        # Botón para ingresar
        tk.Button(frame, text="Ingresar", width=20, command=self.validar_login).pack(pady=15)

        # Texto de ayuda
        tk.Label(frame, text="Usuario: programacion | Contraseña: programacion", fg="gray").pack()

    # Valida login
    def validar_login(self):
        try:
            # Obtiene usuario escrito
            usuario = self.usuario_entry.get()

            # Obtiene contraseña escrita
            contrasena = self.contrasena_entry.get()

            # Valida credenciales
            self.sistema.login(usuario, contrasena)

        except LoginError as error:
            # Registra error
            registrar_log(f"ERROR LOGIN: {error}")

            # Muestra mensaje de error
            messagebox.showerror("Error de acceso", str(error))

        else:
            # Si el login es correcto, muestra menú
            self.mostrar_menu()

    # Muestra menú principal
    def mostrar_menu(self):
        # Limpia ventana
        self.limpiar_ventana()

        # Título del sistema
        titulo = tk.Label(self.root, text="Sistema Integral Software FJ", font=("Arial", 20, "bold"))
        titulo.pack(pady=15)

        # Frame para botones
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Lista de botones con texto y función
        botones = [
            ("Registrar cliente", self.ventana_cliente),
            ("Registrar servicio", self.ventana_servicio),
            ("Crear reserva", self.ventana_reserva),
            ("Listar clientes", self.listar_clientes),
            ("Listar servicios", self.listar_servicios),
            ("Listar reservas", self.listar_reservas),
            ("Confirmar reserva", self.confirmar_reserva),
            ("Cancelar reserva", self.cancelar_reserva),
            ("Procesar pago", self.procesar_pago),
            ("Cargar datos de prueba", self.cargar_prueba),
            ("Salir", self.root.quit),
        ]

        # Crea botones en dos columnas
        for i, (texto, comando) in enumerate(botones):
            tk.Button(frame, text=texto, width=25, height=2, command=comando).grid(
                row=i // 2,
                column=i % 2,
                padx=10,
                pady=8
            )

        # Área de texto para mostrar resultados
        self.salida = tk.Text(self.root, width=100, height=12)
        self.salida.pack(pady=10)

    # Escribe texto en el área de salida
    def escribir_salida(self, texto):
        self.salida.delete("1.0", tk.END)
        self.salida.insert(tk.END, texto)

    # Ventana para registrar cliente
    def ventana_cliente(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar cliente")
        ventana.geometry("400x300")

        tk.Label(ventana, text="Nombre:").pack()
        nombre = tk.Entry(ventana, width=40)
        nombre.pack()

        tk.Label(ventana, text="Documento:").pack()
        documento = tk.Entry(ventana, width=40)
        documento.pack()

        tk.Label(ventana, text="Correo:").pack()
        correo = tk.Entry(ventana, width=40)
        correo.pack()

        # Función interna para guardar cliente
        def guardar():
            try:
                self.sistema.agregar_cliente(nombre.get(), documento.get(), correo.get())
            except ClienteError as error:
                registrar_log(f"ERROR CLIENTE: {error}")
                messagebox.showerror("Error", str(error))
            else:
                messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
                ventana.destroy()

        tk.Button(ventana, text="Guardar", command=guardar).pack(pady=20)

    # Ventana para registrar servicio
    def ventana_servicio(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar servicio")
        ventana.geometry("400x300")

        tk.Label(ventana, text="Tipo de servicio:").pack()

        tipo = ttk.Combobox(
            ventana,
            values=["Reserva de sala", "Alquiler de equipo", "Asesoría especializada"],
            state="readonly",
            width=35
        )
        tipo.pack()
        tipo.current(0)

        tk.Label(ventana, text="Nombre del servicio:").pack()
        nombre = tk.Entry(ventana, width=40)
        nombre.pack()

        tk.Label(ventana, text="Precio base por hora:").pack()
        precio = tk.Entry(ventana, width=40)
        precio.pack()

        # Guarda servicio
        def guardar():
            try:
                self.sistema.agregar_servicio(tipo.get(), nombre.get(), precio.get())
            except ServicioError as error:
                registrar_log(f"ERROR SERVICIO: {error}")
                messagebox.showerror("Error", str(error))
            else:
                messagebox.showinfo("Éxito", "Servicio registrado correctamente.")
                ventana.destroy()

        tk.Button(ventana, text="Guardar", command=guardar).pack(pady=20)

    # Ventana para crear reserva
    def ventana_reserva(self):
        if not self.sistema.clientes or not self.sistema.servicios:
            messagebox.showwarning("Advertencia", "Debe registrar clientes y servicios primero.")
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Crear reserva")
        ventana.geometry("500x350")

        tk.Label(ventana, text="Cliente:").pack()

        clientes_combo = ttk.Combobox(
            ventana,
            values=[c.mostrar_info() for c in self.sistema.clientes],
            state="readonly",
            width=60
        )
        clientes_combo.pack()
        clientes_combo.current(0)

        tk.Label(ventana, text="Servicio:").pack()

        servicios_combo = ttk.Combobox(
            ventana,
            values=[s.mostrar_info() for s in self.sistema.servicios],
            state="readonly",
            width=60
        )
        servicios_combo.pack()
        servicios_combo.current(0)

        tk.Label(ventana, text="Duración en horas:").pack()
        duracion = tk.Entry(ventana, width=30)
        duracion.pack()

        # Guarda reserva
        def guardar():
            try:
                self.sistema.crear_reserva(
                    clientes_combo.current(),
                    servicios_combo.current(),
                    duracion.get()
                )
            except (ReservaError, IndexError) as error:
                registrar_log(f"ERROR RESERVA: {error}")
                messagebox.showerror("Error", str(error))
            else:
                messagebox.showinfo("Éxito", "Reserva creada correctamente.")
                ventana.destroy()

        tk.Button(ventana, text="Crear reserva", command=guardar).pack(pady=20)

    # Lista clientes
    def listar_clientes(self):
        if not self.sistema.clientes:
            self.escribir_salida("No hay clientes registrados.")
            return

        texto = "--- CLIENTES ---\n\n"

        for cliente in self.sistema.clientes:
            texto += cliente.mostrar_info() + "\n"

        self.escribir_salida(texto)

    # Lista servicios
    def listar_servicios(self):
        if not self.sistema.servicios:
            self.escribir_salida("No hay servicios registrados.")
            return

        texto = "--- SERVICIOS ---\n\n"

        for servicio in self.sistema.servicios:
            texto += servicio.mostrar_info() + "\n"

        self.escribir_salida(texto)

    # Lista reservas
    def listar_reservas(self):
        if not self.sistema.reservas:
            self.escribir_salida("No hay reservas registradas.")
            return

        texto = "--- RESERVAS ---\n\n"

        for reserva in self.sistema.reservas:
            texto += reserva.mostrar_info() + "\n"

        self.escribir_salida(texto)

    # Ventana genérica para seleccionar reserva
    def seleccionar_reserva(self, accion):
        if not self.sistema.reservas:
            messagebox.showwarning("Advertencia", "No hay reservas registradas.")
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Seleccionar reserva")
        ventana.geometry("550x250")

        tk.Label(ventana, text="Seleccione una reserva:").pack()

        combo = ttk.Combobox(
            ventana,
            values=[r.mostrar_info() for r in self.sistema.reservas],
            state="readonly",
            width=80
        )
        combo.pack(pady=10)
        combo.current(0)

        # Aplica acción seleccionada
        def aplicar():
            reserva = self.sistema.reservas[combo.current()]

            try:
                if accion == "confirmar":
                    reserva.confirmar()
                    mensaje = "Reserva confirmada correctamente."

                elif accion == "cancelar":
                    reserva.cancelar()
                    mensaje = "Reserva cancelada correctamente."

                else:
                    total = reserva.procesar_pago()
                    mensaje = f"Pago procesado correctamente. Total: ${total:,.0f}"

            except ReservaError as error:
                registrar_log(f"ERROR EN RESERVA: {error}")
                messagebox.showerror("Error", str(error))

            else:
                messagebox.showinfo("Éxito", mensaje)
                ventana.destroy()

        tk.Button(ventana, text="Aceptar", command=aplicar).pack(pady=20)

    # Confirmar reserva
    def confirmar_reserva(self):
        self.seleccionar_reserva("confirmar")

    # Cancelar reserva
    def cancelar_reserva(self):
        self.seleccionar_reserva("cancelar")

    # Procesar pago
    def procesar_pago(self):
        self.seleccionar_reserva("pagar")

    # Cargar datos de prueba
    def cargar_prueba(self):
        try:
            self.sistema.cargar_datos_prueba()
        except ErrorSistema as error:
            registrar_log(f"ERROR DATOS PRUEBA: {error}")
            messagebox.showerror("Error", str(error))
        else:
            messagebox.showinfo("Éxito", "Datos de prueba cargados correctamente.")


# =====================================================
# EJECUCIÓN DEL PROGRAMA
# =====================================================

# Verifica que este archivo se esté ejecutando directamente
if __name__ == "__main__":
    # Crea ventana principal
    ventana_principal = tk.Tk()

    # Crea la aplicación
    app = App(ventana_principal)

    # Mantiene abierta la ventana
    ventana_principal.mainloop()