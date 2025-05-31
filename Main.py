import tkinter as tk
from tkinter import messagebox
import pyodbc
from datetime import date
import uuid

# Configuración de conexión
SERVER = 'DESKTOP-CTLT0M4\\SQLEXPRESS'
DATABASE = 'AlimentamosDB'
USERNAME = 'Sa'
PASSWORD = '123456'

def conectar_bd():
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
        )
        return conn
    except Exception as e:
        messagebox.showerror("Error de Conexión", str(e))
        return None

# Función para centrar ventanas
def centrar_ventana(ventana, ancho=300, alto=300):
    ventana.update_idletasks()
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# --- Funciones por opción ---

def crear_proveedor():
    def guardar():
        conn = conectar_bd()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Proveedor (nit_proveedor, nombre, persona_contacto, telefono, direccion)
                VALUES (?, ?, ?, ?, ?)
            """, (nit.get(), nombre.get(), contacto.get(), telefono.get(), direccion.get()))
            conn.commit()
            messagebox.showinfo("Éxito", "Proveedor creado correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    ventana = tk.Toplevel()
    ventana.title("Crear Proveedor")
    centrar_ventana(ventana, 300, 300)

    tk.Label(ventana, text="NIT:").pack()
    nit = tk.Entry(ventana)
    nit.pack()

    tk.Label(ventana, text="Nombre:").pack()
    nombre = tk.Entry(ventana)
    nombre.pack()

    tk.Label(ventana, text="Persona Contacto:").pack()
    contacto = tk.Entry(ventana)
    contacto.pack()

    tk.Label(ventana, text="Teléfono:").pack()
    telefono = tk.Entry(ventana)
    telefono.pack()

    tk.Label(ventana, text="Dirección:").pack()
    direccion = tk.Entry(ventana)
    direccion.pack()

    tk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)

def crear_producto():
    def guardar():
        conn = conectar_bd()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            proveedor_nit = proveedor_dict[proveedor_var.get()]
            cursor.execute("""
                INSERT INTO Producto (id_producto, nit_proveedor, nombre, descripcion, precio_unitario, fecha_vencimiento)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (str(uuid.uuid4()), proveedor_nit, nombre.get(), descripcion.get(), float(precio.get()), fecha.get()))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto creado correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def obtener_proveedores():
        conn = conectar_bd()
        if not conn:
            return {}
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT nit_proveedor, nombre FROM Proveedor")
            rows = cursor.fetchall()
            return {f"{nombre} ({nit})": nit for nit, nombre in rows}
        except Exception as e:
            messagebox.showerror("Error al cargar proveedores", str(e))
            return {}
        finally:
            conn.close()

    ventana = tk.Toplevel()
    ventana.title("Crear Producto")
    centrar_ventana(ventana, 300, 300)

    proveedor_dict = obtener_proveedores()
    proveedor_var = tk.StringVar(ventana)
    if proveedor_dict:
        proveedor_var.set(list(proveedor_dict.keys())[0])
    else:
        proveedor_var.set("")

    tk.Label(ventana, text="Proveedor:").pack()
    tk.OptionMenu(ventana, proveedor_var, *proveedor_dict.keys()).pack()

    tk.Label(ventana, text="Nombre:").pack()
    nombre = tk.Entry(ventana)
    nombre.pack()

    tk.Label(ventana, text="Descripción:").pack()
    descripcion = tk.Entry(ventana)
    descripcion.pack()

    tk.Label(ventana, text="Precio Unitario:").pack()
    precio = tk.Entry(ventana)
    precio.pack()

    tk.Label(ventana, text="Fecha Vencimiento (YYYY-MM-DD):").pack()
    fecha = tk.Entry(ventana)
    fecha.pack()

    tk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)

def crear_cliente():
    def guardar():
        conn = conectar_bd()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            ciudad_id = ciudad_dict[ciudad_var.get()]
            cursor.execute("""
                INSERT INTO Cliente (id_cliente, id_ciudad, nombre, telefono, direccion)
                VALUES (?, ?, ?, ?, ?)
            """, (str(uuid.uuid4()), ciudad_id, nombre.get(), telefono.get(), direccion.get()))
            conn.commit()
            messagebox.showinfo("Éxito", "Cliente creado correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def obtener_ciudades():
        conn = conectar_bd()
        if not conn:
            return {}
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id_ciudad, nombre FROM Ciudad")
            rows = cursor.fetchall()
            return {nombre: id_ciudad for id_ciudad, nombre in rows}
        except Exception as e:
            messagebox.showerror("Error al cargar ciudades", str(e))
            return {}
        finally:
            conn.close()

    ventana = tk.Toplevel()
    ventana.title("Crear Cliente")
    centrar_ventana(ventana, 300, 300)

    ciudad_dict = obtener_ciudades()
    ciudad_var = tk.StringVar(ventana)
    if ciudad_dict:
        ciudad_var.set(list(ciudad_dict.keys())[0])
    else:
        ciudad_var.set("")

    tk.Label(ventana, text="Ciudad:").pack()
    tk.OptionMenu(ventana, ciudad_var, *ciudad_dict.keys()).pack()

    tk.Label(ventana, text="Nombre:").pack()
    nombre = tk.Entry(ventana)
    nombre.pack()

    tk.Label(ventana, text="Teléfono:").pack()
    telefono = tk.Entry(ventana)
    telefono.pack()

    tk.Label(ventana, text="Dirección:").pack()
    direccion = tk.Entry(ventana)
    direccion.pack()

    tk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)

def crear_conductor():
    def obtener_rutas_y_ciudades():
        conn = conectar_bd()
        if not conn:
            return {}, {}
        cursor = conn.cursor()
        try:
            # Obtener rutas con información de ciudad
            cursor.execute("""
                SELECT r.id_ruta, r.nombre, c.id_ciudad, c.nombre 
                FROM Ruta r
                JOIN Ciudad c ON r.id_ciudad = c.id_ciudad
                ORDER BY r.nombre
            """)
            rows = cursor.fetchall()
            
            rutas_dict = {f"{nombre}": (id_ruta, id_ciudad) for id_ruta, nombre, id_ciudad, _ in rows}
            ciudades_dict = {id_ciudad: nombre for _, _, id_ciudad, nombre in rows}
            
            return rutas_dict, ciudades_dict
        except Exception as e:
            messagebox.showerror("Error al cargar rutas", str(e))
            return {}, {}
        finally:
            conn.close()

    def on_ruta_selected(event):
        # Cuando se selecciona una ruta, actualizar la ciudad automáticamente
        selected_ruta = ruta_var.get()
        if selected_ruta in rutas_dict:
            ruta_id, ciudad_id = rutas_dict[selected_ruta]
            ciudad_var.set(ciudades_dict.get(ciudad_id, ""))
            ciudad_entry.config(state='disabled')  # Deshabilitar edición
        else:
            ciudad_var.set("")
            ciudad_entry.config(state='normal')

    def guardar():
        conn = conectar_bd()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            selected_ruta = ruta_var.get()
            if selected_ruta not in rutas_dict:
                messagebox.showerror("Error", "Seleccione una ruta válida")
                return
                
            ruta_id, ciudad_id = rutas_dict[selected_ruta]
            
            # Validar fecha
            try:
                fecha_ingreso_val = fecha_ingreso.get()
                date.fromisoformat(fecha_ingreso_val)  # Validar formato
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
                return

            cursor.execute("""
                INSERT INTO Conductor (id_conductor, id_ciudad, id_ruta, nombres, apellidos, telefono, fecha_ingreso)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (str(uuid.uuid4()), ciudad_id, ruta_id, nombres.get(), apellidos.get(), telefono.get(), fecha_ingreso_val))
            
            conn.commit()
            messagebox.showinfo("Éxito", "Conductor creado correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    ventana = tk.Toplevel()
    ventana.title("Crear Conductor")
    centrar_ventana(ventana, 350, 400)

    # Obtener datos de rutas y ciudades
    rutas_dict, ciudades_dict = obtener_rutas_y_ciudades()

    # Variable para la selección de ruta
    ruta_var = tk.StringVar(ventana)
    if rutas_dict:
        ruta_var.set(list(rutas_dict.keys())[0])
    else:
        ruta_var.set("No hay rutas disponibles")

    # Variable para mostrar la ciudad
    ciudad_var = tk.StringVar(ventana)
    ciudad_var.set("")

    # Widgets
    tk.Label(ventana, text="Ruta:").pack()
    ruta_menu = tk.OptionMenu(ventana, ruta_var, *rutas_dict.keys())
    ruta_menu.pack()
    ruta_menu.bind("<Configure>", on_ruta_selected)  # Actualizar al seleccionar

    tk.Label(ventana, text="Ciudad:").pack()
    ciudad_entry = tk.Entry(ventana, textvariable=ciudad_var, state='disabled')
    ciudad_entry.pack()

    tk.Label(ventana, text="Nombres:").pack()
    nombres = tk.Entry(ventana)
    nombres.pack()

    tk.Label(ventana, text="Apellidos:").pack()
    apellidos = tk.Entry(ventana)
    apellidos.pack()

    tk.Label(ventana, text="Teléfono:").pack()
    telefono = tk.Entry(ventana)
    telefono.pack()

    tk.Label(ventana, text="Fecha Ingreso (YYYY-MM-DD):").pack()
    fecha_ingreso = tk.Entry(ventana)
    fecha_ingreso.insert(0, date.today().isoformat())
    fecha_ingreso.pack()

    tk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)

    # Actualizar ciudad inicial
    if rutas_dict:
        on_ruta_selected(None)

def crear_ruta():
    def guardar():
        conn = conectar_bd()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            # Validar y formatear fechas
            try:
                fecha_apertura_val = fecha_apertura.get()
                fecha_cambio_val = fecha_cambio.get()
                
                # Convertir a objetos date para validación
                fecha_apertura_date = date.fromisoformat(fecha_apertura_val)
                fecha_cambio_date = date.fromisoformat(fecha_cambio_val)
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
                return
            
            # Validar costo
            try:
                costo_val = float(costo.get())
            except ValueError:
                messagebox.showerror("Error", "El costo debe ser un número válido")
                return
            
            ciudad_destino_id = ciudad_dict[ciudad_destino_var.get()]
            ciudad_origen_id = ciudad_dict[ciudad_origen_var.get()]
            
            # Validar que origen y destino sean diferentes
            if ciudad_origen_id == ciudad_destino_id:
                messagebox.showerror("Error", "La ciudad origen y destino deben ser diferentes")
                return
            
            # Llamar al procedimiento almacenado
            params = (
                ciudad_destino_id, 
                ciudad_origen_id, 
                nombre.get(), 
                fecha_apertura_val,  # Enviar como string en formato YYYY-MM-DD
                costo_val, 
                fecha_cambio_val,    # Enviar como string en formato YYYY-MM-DD
                str(uuid.uuid4())
            )
            
            cursor.execute("{CALL sp_CrearRuta(?, ?, ?, ?, ?, ?, ?)}", params)
            conn.commit()
            messagebox.showinfo("Éxito", "Ruta creada correctamente.")
            ventana.destroy()
        except pyodbc.Error as e:
            messagebox.showerror("Error en la base de datos", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def obtener_ciudades():
        conn = conectar_bd()
        if not conn:
            return {}
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id_ciudad, nombre FROM Ciudad ORDER BY nombre")
            rows = cursor.fetchall()
            return {nombre: id_ciudad for id_ciudad, nombre in rows}
        except Exception as e:
            messagebox.showerror("Error al cargar ciudades", str(e))
            return {}
        finally:
            conn.close()

    ventana = tk.Toplevel()
    ventana.title("Crear Ruta")
    centrar_ventana(ventana, 350, 400)

    ciudad_dict = obtener_ciudades()
    
    # Ciudad destino
    tk.Label(ventana, text="Ciudad Destino:").pack()
    ciudad_destino_var = tk.StringVar(ventana)
    if ciudad_dict:
        ciudad_destino_var.set(list(ciudad_dict.keys())[0])
    else:
        ciudad_destino_var.set("")
    tk.OptionMenu(ventana, ciudad_destino_var, *ciudad_dict.keys()).pack()

    # Ciudad origen (con Bogotá por defecto si existe)
    tk.Label(ventana, text="Ciudad Origen:").pack()
    ciudad_origen_var = tk.StringVar(ventana)
    bogota_key = next((key for key in ciudad_dict.keys() if "Bogotá" in key or "Bogota" in key), None)
    if bogota_key:
        ciudad_origen_var.set(bogota_key)
    elif ciudad_dict:
        ciudad_origen_var.set(list(ciudad_dict.keys())[0])
    else:
        ciudad_origen_var.set("")
    tk.OptionMenu(ventana, ciudad_origen_var, *ciudad_dict.keys()).pack()

    tk.Label(ventana, text="Nombre Ruta:").pack()
    nombre = tk.Entry(ventana)
    nombre.pack()

    tk.Label(ventana, text="Fecha Apertura (YYYY-MM-DD):").pack()
    fecha_apertura = tk.Entry(ventana)
    fecha_apertura.insert(0, date.today().isoformat())
    fecha_apertura.pack()

    tk.Label(ventana, text="Costo:").pack()
    costo = tk.Entry(ventana)
    costo.pack()

    tk.Label(ventana, text="Fecha Cambio Costo (YYYY-MM-DD):").pack()
    fecha_cambio = tk.Entry(ventana)
    fecha_cambio.insert(0, date.today().isoformat())
    fecha_cambio.pack()

    tk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)

def crear_venta():
    # Variables globales para mantener el estado entre formularios
    global ventana_venta, ventana_detalle, id_venta_actual
    
    def guardar_venta_principal():
        global id_venta_actual
        conn = conectar_bd()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            # Generar ID de venta
            id_venta_actual = str(uuid.uuid4())
            
            # Obtener IDs de cliente y ruta
            cliente_info = cliente_dict[cliente_var.get()]
            id_cliente = cliente_info[0]
            id_ciudad = cliente_info[1]
            
            ruta_id = ruta_dict[ruta_var.get()][0]
            
            # Validar fecha
            try:
                fecha_venta_val = fecha_venta.get()
                date.fromisoformat(fecha_venta_val)  # Validar formato
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
                return

            # Insertar venta principal
            cursor.execute("""
                INSERT INTO Venta (id_venta, id_cliente, id_ciudad, id_ruta, fecha_venta, total_venta)
                VALUES (?, ?, ?, ?, ?, 0)  -- Inicializar total en 0
            """, (id_venta_actual, id_cliente, id_ciudad, ruta_id, fecha_venta_val))
            
            conn.commit()
            messagebox.showinfo("Éxito", "Venta creada. Ahora agregue productos.")
            ventana_venta.destroy()
            abrir_formulario_detalle()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def abrir_formulario_detalle():
        global ventana_detalle
        
        ventana_detalle = tk.Toplevel()
        ventana_detalle.title("Agregar Productos a Venta")
        centrar_ventana(ventana_detalle, 400, 350)
        
        # Obtener productos disponibles
        def obtener_productos():
            conn = conectar_bd()
            if not conn:
                return {}
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    SELECT id_producto, nombre, precio_unitario 
                    FROM Producto 
                    WHERE fecha_vencimiento > GETDATE()  -- Solo productos no vencidos
                    ORDER BY nombre
                """)
                rows = cursor.fetchall()
                return {f"{nombre} (${precio_unitario:.2f})": (id_producto, precio_unitario) 
                        for id_producto, nombre, precio_unitario in rows}
            except Exception as e:
                messagebox.showerror("Error al cargar productos", str(e))
                return {}
            finally:
                conn.close()
        
        productos_dict = obtener_productos()
        
        # Variables para el formulario
        producto_var = tk.StringVar(ventana_detalle)
        if productos_dict:
            producto_var.set(list(productos_dict.keys())[0])
        
        cantidad_var = tk.StringVar(ventana_detalle, value="1")
        subtotal_var = tk.StringVar(ventana_detalle, value="0.00")
        
        def calcular_subtotal(*args):
            try:
                producto_seleccionado = producto_var.get()
                cantidad = int(cantidad_var.get())
                if producto_seleccionado in productos_dict:
                    _, precio = productos_dict[producto_seleccionado]
                    subtotal = precio * cantidad
                    subtotal_var.set(f"{subtotal:.2f}")
            except:
                subtotal_var.set("0.00")
        
        # Configurar eventos para cálculo automático
        producto_var.trace_add("write", calcular_subtotal)
        cantidad_var.trace_add("write", calcular_subtotal)
        
        # Widgets del formulario de detalle
        tk.Label(ventana_detalle, text="Producto:").pack()
        tk.OptionMenu(ventana_detalle, producto_var, *productos_dict.keys()).pack()
        
        tk.Label(ventana_detalle, text="Cantidad:").pack()
        tk.Entry(ventana_detalle, textvariable=cantidad_var).pack()
        
        tk.Label(ventana_detalle, text="Subtotal:").pack()
        tk.Label(ventana_detalle, textvariable=subtotal_var).pack()
        
        def guardar_detalle(continuar=True):
            conn = conectar_bd()
            if not conn:
                return
            cursor = conn.cursor()
            try:
                # Validar datos
                producto_seleccionado = producto_var.get()
                if producto_seleccionado not in productos_dict:
                    messagebox.showerror("Error", "Seleccione un producto válido")
                    return
                
                try:
                    cantidad = int(cantidad_var.get())
                    if cantidad <= 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Error", "Cantidad debe ser un número entero positivo")
                    return
                
                id_producto, precio_unitario = productos_dict[producto_seleccionado]
                subtotal = precio_unitario * cantidad
                
                # Insertar detalle
                cursor.execute("""
                    INSERT INTO DetalleVenta (id_detalle, id_venta, id_producto, cantidad, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                """, (str(uuid.uuid4()), id_venta_actual, id_producto, cantidad, subtotal))
                
                # Actualizar total de la venta
                cursor.execute("""
                    UPDATE Venta 
                    SET total_venta = total_venta + ?
                    WHERE id_venta = ?
                """, (subtotal, id_venta_actual))
                
                conn.commit()
                
                if continuar:
                    # Limpiar campos para nuevo producto
                    cantidad_var.set("1")
                    producto_var.set(list(productos_dict.keys())[0])
                    messagebox.showinfo("Éxito", "Producto agregado. Agregue otro producto o finalice.")
                else:
                    # Finalizar venta
                    ventana_detalle.destroy()
                    messagebox.showinfo("Éxito", f"Venta finalizada. ID: {id_venta_actual}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()
        
        # Botones
        frame_botones = tk.Frame(ventana_detalle)
        frame_botones.pack(pady=10)
        
        tk.Button(frame_botones, text="Otro Producto", 
                 command=lambda: guardar_detalle(True)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Fin Venta", 
                 command=lambda: guardar_detalle(False)).pack(side=tk.LEFT, padx=5)
        
        # Calcular subtotal inicial
        calcular_subtotal()

    # --- Formulario principal de venta ---
    ventana_venta = tk.Toplevel()
    ventana_venta.title("Crear Venta - Datos Principales")
    centrar_ventana(ventana_venta, 350, 400)

    # Obtener clientes
    def obtener_clientes():
        conn = conectar_bd()
        if not conn:
            return {}
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT c.id_cliente, c.id_ciudad, c.nombre, ci.nombre 
                FROM Cliente c
                JOIN Ciudad ci ON c.id_ciudad = ci.id_ciudad
                ORDER BY c.nombre
            """)
            rows = cursor.fetchall()
            return {f"{nombre} ({ciudad})": (id_cliente, id_ciudad) 
                    for id_cliente, id_ciudad, nombre, ciudad in rows}
        except Exception as e:
            messagebox.showerror("Error al cargar clientes", str(e))
            return {}
        finally:
            conn.close()

    # Obtener rutas
    def obtener_rutas():
        conn = conectar_bd()
        if not conn:
            return {}
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT r.id_ruta, r.nombre, c.nombre 
                FROM Ruta r
                JOIN Ciudad c ON r.id_ciudad = c.id_ciudad
                ORDER BY r.nombre
            """)
            rows = cursor.fetchall()
            return {f"{ruta_nombre} ({ciudad})": (id_ruta, id_ruta) 
                    for id_ruta, ruta_nombre, ciudad in rows}
        except Exception as e:
            messagebox.showerror("Error al cargar rutas", str(e))
            return {}
        finally:
            conn.close()

    cliente_dict = obtener_clientes()
    ruta_dict = obtener_rutas()

    # Variables para el formulario
    cliente_var = tk.StringVar(ventana_venta)
    if cliente_dict:
        cliente_var.set(list(cliente_dict.keys())[0])
    
    ruta_var = tk.StringVar(ventana_venta)
    if ruta_dict:
        ruta_var.set(list(ruta_dict.keys())[0])
    
    fecha_venta = tk.StringVar(ventana_venta, value=date.today().isoformat())

    # Widgets del formulario principal
    tk.Label(ventana_venta, text="Cliente:").pack()
    tk.OptionMenu(ventana_venta, cliente_var, *cliente_dict.keys()).pack()
    
    tk.Label(ventana_venta, text="Ruta:").pack()
    tk.OptionMenu(ventana_venta, ruta_var, *ruta_dict.keys()).pack()
    
    tk.Label(ventana_venta, text="Fecha Venta (YYYY-MM-DD):").pack()
    tk.Entry(ventana_venta, textvariable=fecha_venta).pack()
    
    tk.Button(ventana_venta, text="Agregar Productos", 
             command=guardar_venta_principal).pack(pady=20)

def mostrar_vista_ventas():
    conn = conectar_bd()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Vista_VentasDetalle")
        rows = cursor.fetchall()
        ventana = tk.Toplevel()
        ventana.title("Vista Ventas Detalle")
        text_area = tk.Text(ventana, width=100, height=30)
        text_area.pack()
        for row in rows:
            text_area.insert(tk.END, str(row) + "\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

# --- Menú principal ---

def menu_principal():
    root = tk.Tk()
    root.title("Menú Principal - Alimentamos")
    centrar_ventana(root, 300, 300)

    opciones = [
        ("1) Crear Proveedor", crear_proveedor),
        ("2) Crear Producto", crear_producto),
        ("3) Crear Cliente", crear_cliente),
        ("4) Crear Ruta", crear_ruta),
        ("5) Crear Conductor", crear_conductor),
        ("6) Crear Venta", crear_venta),
        ("7) Mostrar Vista Ventas Detalle", mostrar_vista_ventas),
    ]

    for texto, comando in opciones:
        tk.Button(root, text=texto, command=comando, width=40).pack(pady=5)

    root.mainloop()

# Ejecutar menú
menu_principal()
