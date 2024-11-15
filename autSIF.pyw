import time, requests, mysql.connector, threading

import os, shutil, subprocess

user = os.getlogin()
ruta = f'C:\\Users\\{user}\\AppData\\autSIF.pyw'
if not os.path.exists(ruta):
 shutil.copy("autSIF.pyw", ruta)
reg=f'reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v autSIF /t REG_SZ /d {ruta} /f'
subprocess.run(reg, shell=True)


autenticacion = mysql.connector.connect(
user='root',
password='',
host='localhost',
database='DATABASEX'
)


print_lock = threading.Lock()
def enviar_peticion(url, tiempo):
 global n
 while True:
  with print_lock:
   print(f"ESPERANDO {tiempo} SEG PARA ENVIAR PETICION...")
  time.sleep(tiempo)
  try:
   response = requests.get(url)
   with print_lock:
    print(f"Petición enviada a: {url} -> Respuesta: {response.status_code}\n")
  except requests.exceptions.RequestException as e:
   with print_lock:
    print(f"Error al enviar a {url}: {e}\n")

def ver_base_de_datos():
 cursor = autenticacion.cursor()
 query = "SELECT url, minutos FROM control"
 cursor.execute(query)
 resultados = cursor.fetchall()
 threads = []
 for fila in resultados:
  tseg = int(fila[1]) * 60
  url = fila[0]
  hilo = threading.Thread(target=enviar_peticion, args=(url, tseg))
  threads.append(hilo)
  hilo.start()
 cursor.close()

ver_base_de_datos()

