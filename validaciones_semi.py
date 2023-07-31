import pymysql
from Encrypt_Decrypt import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import threading
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import subprocess
import os
import sys
import shutil
from webdriver_manager.chrome import ChromeDriverManager


#Variables Globales
#-------------------------------------------------------------------------------------------
global HoraInicio
global HoraFin
global EstadoBot
global Url
global PalabraBuscar
global driver 

# Path Default
#Variables de arranque
#-------------------------------------------------------------------------------------------
comprobarRuta = str(os.path.dirname(sys.argv[0]))
if comprobarRuta.strip() == None:
    EjecutablePrograma = str(os.path.basename(sys.executable))
    RutaEjecutablePrograma = str(os.path.dirname(sys.executable))
elif comprobarRuta.strip() == '':
    EjecutablePrograma = str(os.path.basename(sys.executable))
    RutaEjecutablePrograma = str(os.path.dirname(sys.executable))
else:
    EjecutablePrograma = str(os.path.basename(sys.argv[0]))
    RutaEjecutablePrograma = str(os.path.dirname(sys.argv[0]))

# Path Software
#-------------------------------------------------------------------------------------------
def obtenerRutas():
    #ruta de este archivo .py, incluyendo el nombre de este archivo
    ejecutablePrograma = str(os.path.realpath(sys.argv[0]))
    #ruta contenedora de este archivo .py
    rutaEjecutablePrograma = str(os.path.dirname(os.path.realpath(sys.argv[0])))
    return {"ejecutablePrograma": ejecutablePrograma, "rutaEjecutablePrograma": rutaEjecutablePrograma}

#Encriptaciones de Datos sencibles
#-------------------------------------------------------------------------------------------
password = "413052325A474C6D417752335A774C35417752335A6D5A305A6D4C3D"
user = "416D563245774D54416D443D"
database = "417744325A77706A41484C325A477031416D443245774D524177523341514C35413052325A474C6D4177783245774D5341484C325A774D54416D443D"
host = "5A6D526D5A775A335A78486D5A5157535A6D4E6C45475A6B"

# Conexión a base de datos
#-------------------------------------------------------------------------------------------
def conntDB():
    try:    
        connectionMySQL = pymysql.connect(host=DeCrypt(host), 
            user=DeCrypt(user), password=DeCrypt(password), 
            database=DeCrypt(database), charset='utf8', cursorclass = pymysql.cursors.DictCursor)
        connectionMySQL.autocommit(True)  
        print('conectado a la base de datos')  
        return connectionMySQL
    except Exception as e:
        print('Sin conexión a la base de datos', e)

#Versión de chrome Windows
#-------------------------------------------------------------------------------------------
def obtenerVersionChromeWindows():
    try:
        resultado = subprocess.check_output(
            r'wmic datafile where name="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" get Version /value',
        shell = True
        )
        resultado = resultado.decode('utf-8').strip()
        resultado = resultado.split('=')
        resultado = str(resultado[1])
        resultado = resultado.split('.')
        versionChrome = str(resultado[0])
        print('Version google:', versionChrome)
        return versionChrome
    except Exception as e:
        nombreFuncion = "obtenerVersionChromeWindows"
        ControlERROR(e, nombreFuncion)
        print('Error en obtener version de chrome: ' + str(e))
        return False
    
# Versión de chrome linux
#-------------------------------------------------------------------------------------------
def obtenerVersionChrome(nombrePrograma):
    try:
        comando = subprocess.run([nombrePrograma, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        resultado = str(comando.stdout)  # r: Google Chrome 91.0.4472.114
        resultado = resultado.split(' ')
        resultado = str(resultado[2])  # r: 91.0.4472.114
        resultado = resultado.split('.')
        versionChrome = str(resultado[0])  # r: 91
        print('Version google:', versionChrome)
        return versionChrome
    except Exception as e:
        nombreFuncion = "obtenerVersionChrome"
        print("Error al obtener version de chromer" + str(e))
        ControlERROR(e, nombreFuncion)
        return False
#Descarga chrome driver
#-------------------------------------------------------------------------------------------
def rutaChromeDriver():
    my_os = sys.platform
    if my_os == "linux" or my_os == "linux2":
        print('Sistema operativo: ' + my_os)
        versionarchivo = str(obtenerVersionChrome('google-chrome'))
    elif my_os == "win32":
        print('Sistema operativo: ' + my_os)       
        versionarchivo = False   
    nombreCarpeta = f"chromedriver_{versionarchivo}"
    rutaEjecutablePrograma = obtenerRutas()['rutaEjecutablePrograma']
    rutachromedriver = os.path.join(rutaEjecutablePrograma, nombreCarpeta)
    print(rutachromedriver)
    rutadriversJSON = os.path.join(rutaEjecutablePrograma, "drivers.json")
    print(rutadriversJSON)
    if not os.path.exists(rutachromedriver):
        try:
            if not os.path.exists(rutadriversJSON):
                pass
            else:
                os.remove(rutadriversJSON)
            rutaDescarga = ChromeDriverManager(path=rutachromedriver).install()
            shutil.move(rutaDescarga, rutachromedriver)
            return rutachromedriver
        except Exception as e:
            nombreFuncion = "consultas"
            print("Error al obtener datos binarios chromedriver: " + str(e))
            ControlERROR(e, nombreFuncion)            
            False
    else:
        return rutachromedriver

# Parametros chrome driver - selenium
#-------------------------------------------------------------------------------------------
def ejecutarChromeDriver():
    global driver
    try:
        rutaEjecutablePrograma = obtenerRutas()['rutaEjecutablePrograma']
        print("Estoy aqui")          
        rutachromedriver = rutaChromeDriver()
        ejecutable = os.path.join(rutachromedriver, 'chromedriver')    
        rutaUserChrome = str(os.path.join(
        rutaEjecutablePrograma, 'DefaultChrome'))
        perfilChrome = f"user-data-dir={rutaUserChrome}"
        chrome_option = webdriver.ChromeOptions()        
        chrome_option.add_argument(perfilChrome)
        chrome_option.add_argument("--start-maximized")#Open Browser in maximized mode
        chrome_option.add_argument("--no-sandbox")#Bypass OS security model
        # chrome_option.add_argument("--headless=new")#Chrome en segundo plano
        chrome_option.add_argument("--disable-dev-shm-usage")#overcome limited resource problems       
        chrome_option.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Chrome(service=Service(ejecutable), options=chrome_option)
        ContinuarEjecucion = True        
    except Exception as e:
        nombreFuncion = "ejecutarChromeDriver"
        print(f"Error en el driver: {e}")
        ControlERROR(e, nombreFuncion)
        ContinuarEjecucion = False
    return ContinuarEjecucion

#Traer datos de la BD
#-------------------------------------------------------------------------------------------
def consultas():
    global HoraInicio 
    global HoraFin
    global EstadoBot
    global Url
    global PalabraBuscar
    connectionMySQL = conntDB()
    try:
        with connectionMySQL.cursor() as cursor:
            consulta = 'SELECT * FROM tbl_principal;'
            cursor.execute(consulta)
            rows = cursor.fetchall()
            #print(rows)
            if len(rows) > 0:
            # Crear listas vacías para almacenar los valores de la tercera columna
                detalle_valores = []
                for row in rows:
                    detalle = row['PRI_DETALLE']
                    detalle_valores.append(detalle)
                HoraInicio = int(detalle_valores[0])
                HoraFin = int(detalle_valores[1])
                EstadoBot = detalle_valores[2]
                Url = detalle_valores[3]
                PalabraBuscar = detalle_valores[4]
                print('trayendo data de la base de datos') 
    except Exception as e:
        nombreFuncion = "consultas"
        print(f"No fue posible conectarse a la base de datos, tipo de error: {e}")
        ControlERROR(e, nombreFuncion)


    
#Validar hora
#-------------------------------------------------------------------------------------------

def validarHora(HoraInicio, HoraFin):
    try: 
        horaActual = int(datetime.now().strftime("%H"))
        if horaActual >= HoraInicio and horaActual < HoraFin:
            print("Bot dentro del horario de funcionamiento", str(horaActual))
            return True
        else:
            print("Bot fuera del horario de funcionamiento ",str(horaActual))
            return False
    except Exception as e:
        nombreFuncion = "validarHora"
        print("Error en validarHora")
        ControlERROR(e, nombreFuncion)

#Validar Eatado
#-------------------------------------------------------------------------------------------
def validarEstado(EstadoBot):
    try:
        if EstadoBot == "Activo":
            return True
        else:
            print("Bot Inactivo")
            return False
    except Exception as e:
        nombreFuncion = "validarEstado"
        print("Error en validarEstado")
        ControlERROR(e, nombreFuncion)

# Función para realizar la busqueda y obtener el contenido
#-------------------------------------------------------------------------------------------
def buscar_obtener_contenido(Url, PalabraBuscar):
    try:
        driver.get(Url)
        busqueda = driver.find_element(By.NAME, "q")
        busqueda.send_keys(PalabraBuscar)
        busqueda.send_keys(Keys.ENTER)
        driver.implicitly_wait(5)

        resultado = driver.find_element(By.XPATH, '//a[contains(@href, "wikipedia")]')
        resultado.click()
        driver.implicitly_wait(5)
        if resultado:
            raspar_contenido()
        else:
            print("No se encontró el resultado")
            ejecutarBot()
    except Exception as e:
        nombreFuncion = "buscar_obtener_contenido"
        print("Ocurrió un error durante la ejecución de buscar_obtener_contenido:", e)
        ControlERROR(e, nombreFuncion)
        driver.close()

#Scraping Bot
#-------------------------------------------------------------------------------------------
def raspar_contenido():
    try:
        titulo = driver.find_element(By.CLASS_NAME, 'mw-page-title-main')
        introduccion = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[1]')
        historia = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[2]')
        componentes = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[5]')
        time.sleep(3)
        contenido = {
            "titulo": titulo.text,
            "introduccion": introduccion.text,
            "historia": historia.text,
            "componentes": componentes.text
        }
        
        insertar_contenido(contenido)
            
    except Exception as e:
        nombreFuncion = "raspar_contenido"
        print("nombreFuncion")
        ControlERROR(e, nombreFuncion)
        driver.close()

    
# Función para insertar datos
#-------------------------------------------------------------------------------------------
def insertar_contenido(contenido):
    connectionMySQL = conntDB()
    try:
        with connectionMySQL.cursor() as cursor:
            consulta = "INSERT INTO tbl_prueba (PRU_TITULO, PRU_INTRODUCCION, PRU_HISTORIA, PRU_COMPONENTES) VALUES (%s, %s, %s, %s)"
            valores = (contenido["titulo"], contenido["introduccion"], contenido["historia"], contenido["componentes"])
            print("Aqui estoy")
            cursor.execute(consulta, valores)
            connectionMySQL.commit()
            print("Contenido insertado correctamente")
            driver.close()
    except Exception as e:
        nombreFuncion = "insertar_contenido"
        print("Error en insertar_contenido", str(e))
        ControlERROR(e, nombreFuncion)
        driver.close()

#Ejecutar Bot
#-------------------------------------------------------------------------------------------
def ejecutarBot():
    try:
        detener_bot = True
        while detener_bot:
            consultas()
            if validarHora(HoraInicio, HoraFin):
                if validarEstado(EstadoBot):
                    print("El estado del bot es Activo")
                    driver = ejecutarChromeDriver()
                    if driver == True:
                        buscar_obtener_contenido(Url, PalabraBuscar)
                    else:
                        print("No se pudo ejecutar el driver")
                else:
                    print("El estado del bot es Inactivo")              
            time.sleep(20)        
    except Exception as e:
        nombreFuncion = "ejecutarBot"
        print("Error en ejecutarBot")
        ControlERROR(e, nombreFuncion)
        
        
 
    
# Control de errores
#-------------------------------------------------------------------------------------------

def ControlERROR(e, nombreFuncion):
    connectionMySQL = conntDB()
    try:
        with connectionMySQL.cursor() as cursor:
            # Limpiamos la cadena
            cadena1 = str(e).replace('"','*')
            cadena2 = cadena1.replace("'","*")
            sql2 = "INSERT INTO " + str(DeCrypt(database)) + \
                ".tbl_logs (LOG_TIPO_ERROR, LOG_ESTADO ) VALUES ('" + str(nombreFuncion) + "', '" + str(cadena2) + "');"
            cursor.execute(sql2)
            connectionMySQL.close()
    except:
        print('Error ControlERROR')
        connectionMySQL.close()

ejecutarBot()
