from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command, netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
import difflib

# Inicializa Nornir usando los archivos de configuración
nr = InitNornir(config_file="config.yaml")

"""Metodo para detectar y revertir configuraciones no autorizadas"""
def detectConfig(task):
    
    #Obtener Configuracion actual del dispositivo
    current_config_result = task.run(
        napalm_get,
        getters=["config"],  # Usar el getter "config" para obtener el running-config
    )
    
    #Guardar especificamente la configuracion en una variable
    current_running_config = current_config_result.result["config"]["running"]
    
    # Leer el archivo del running-config autorizado en la carpeta authorize_config
    authorized_config_file = f"./authorize_config/{task.host.name}_running_config_authorized.txt"
    with open(authorized_config_file, "r") as file:
        authorized_running_config = file.read()

    # Comparar el running-config actual con el autorizado
    if current_running_config != authorized_running_config:
        print(f"Cambio no autorizado detectado en {task.host.name}")
        
        # Mostrar las diferencias detectadas en ambos archivos usando la libreria difflib
        diff = difflib.unified_diff(
            authorized_running_config.splitlines(),
            current_running_config.splitlines(),
            lineterm='',
            fromfile='Configuracion Autorizada',
            tofile='Configuracion Actual'
        )

        #Imprimimos las lineas diferentes
        for line in diff:
            print(line)

        # Revertir a la configuración autorizada si se detecta un cambio no autorizado
        print(f"Revirtiendo configuración no autorizada en {task.host.name}")

        #Enviamos todas las lineas de la configuraciona autorizada del archivo al dispositivo
        task.run(
            netmiko_send_config,
            config_commands=authorized_running_config.splitlines()  # Aplicar configuración autorizada
        )

        #Enviamos el comando wr para guardar la configuracion
        task.run(
            netmiko_send_command,
            command_string="wr" # guardar
        )

        print(f"Se revirtieron las configuraciones del {task.host.name} exitosamente!")
        
    else:
        print(f"No se detectaron cambios no autorizados en {task.host.name}")


    
result = nr.run(task=detectConfig)
#print_result(result)

