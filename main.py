from pythonping import ping
from tkinter import messagebox
import win32console
import win32gui
import configparser
import os, time, pygame as pg

settings = configparser.ConfigParser()
pg.init()

def checkSettings():
    settings['Settings'] = {
        'ObjectiveIP': ''
    }
    settings.read('./utils/settings.ini')
    settings.sections()
    return input("""
                 Introduzca la IP o host del objetivo, esto solo debera hacerlo una vez.
                 En caso de querer cambiarlo, elimine el archivo settings.ini, 
                 y vuelva a inicar la aplicacion, o solamente cambielo en dicho archivo\n\n
                 Host/IP: """)

def saveSettings():

    ObjectiveIP = checkSettings()

    settings['Settings'] = {
        'ObjectiveIP': ObjectiveIP
    }

    with open('./utils/settings.ini', 'w') as settingsFile:
        settings.write(settingsFile)


def detect():

    print(f"""
        ¡Iniciando Rastreo! La app se cerrara dentro de 10 segundos, mientras se ejecutara 
        en 2ndo plano para no molestarle si desea cerrarla, puede hacerlo finalizando en el 
        administrador de tareas el proceso llamado Python.
        """, 
        end='', 
        flush=True)
    
    time.sleep(10)
    while True:
        
        ventana = win32console.GetConsoleWindow()
        win32gui.ShowWindow(ventana, 0)
        
        settings.read('./utils/settings.ini')
        settings.sections()
        ip = settings['Settings']['ObjectiveIP']


        signal = ping(ip, verbose=True)

        if not signal.success():
            continue
        sound = pg.mixer.Sound("./utils/success.mp3")
        pg.mixer.Sound.play(sound)
        messagebox.showinfo(title="¡Atencion!", message=f"El usuario: {ip} se ha conectado")
        break


if __name__ == "__main__":
    paths = os.listdir("./utils/")
    if 'settings.ini' not in paths:
        saveSettings()
        detect()
    else:
        detect()
