from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command, netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
import difflib
from save_authorized_config import saveAuthorizeConfig
import logging

# Configuración del log
logging.basicConfig(
    filename="./logs/error_log.log",  # Errores
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s %(message)s"
)

# Inicializa Nornir usando los archivos de configuración
nr = InitNornir(config_file="config.yaml")


"""Método para detectar y revertir configuraciones no autorizadas"""
def detectConfig(task):
    try:
        print(f"Iniciando auditoría en {task.host.name}...")
        
        # Obtener configuración actual del dispositivo
        current_config_result = task.run(
            napalm_get,
            getters=["config"]
        )
        
        # Guardar específicamente la configuración en una variable
        current_running_config = current_config_result.result["config"]["running"]
        
        # Leer el archivo del running-config autorizado
        authorized_config_file = f"./authorize_config/{task.host.name}_running_config_authorized.txt"
        with open(authorized_config_file, "r") as file:
            authorized_running_config = file.read()
        
        # Comparar la configuración actual con la autorizada
        if current_running_config != authorized_running_config:
            print(f"Cambio no autorizado detectado en {task.host.name}")
            
            # Mostrar las diferencias usando la librería difflib
            diff = difflib.unified_diff(
                authorized_running_config.splitlines(),
                current_running_config.splitlines(),
                lineterm='',
                fromfile='Configuración Autorizada',
                tofile='Configuración Actual'
            )

            for line in diff:
                print(line)
            print("\n")
            print("1. Revertir configuración")
            print("0. Cancelar")
            validate = input("Elija una opcion (0-1): ")
            if validate == '1':

                # Revertir la configuracion no autorizada
                print(f"Revirtiendo configuración no autorizada en {task.host.name}")
                
                task.run(
                    netmiko_send_config,
                    config_commands=authorized_running_config.splitlines()
                )
                
                task.run(
                    netmiko_send_command,
                    command_string="wr"
                )

                print(f"Se revirtieron las configuraciones del {task.host.name} exitosamente!")
                saveAuthorizeConfig(task)
            else:
                return
        else:
            print(f"No se detectaron cambios no autorizados en {task.host.name}")
    except Exception as ex:
        print(f"Ocurrió un error durante el procesamiento en el dispositivo {task.host.name}")
        logging.error(f"Error en el dispositivo {task.host.name}: {ex}", exc_info=True)


def showDevices():
    devices = list(nr.inventory.hosts.keys())
    print("\n--- Seleccione un dispositivo ---")
    for idx, device in enumerate(devices, 0):
        print(f"{idx}. {device}")
    choice = input("Seleccione el numero del dispositivo: ")

    try:
        device_indx = int(choice)
        if 0 <= device_indx < len(devices):
            return devices[device_indx]
        else:
            return None
    except ValueError:
        print("Entrada invalida. Por favor, ingrese un numero.")
        return None


# Función para mostrar el menú y ejecutar las opciones
def show_menu():
    while True:
        print("\n--- Menú de Opciones ---")
        print("1. Guardar configuración de los dispositivos")
        print("2. Realizar auditoría de configuración")
        print("3. Salir")
        
        choice = input("Seleccione una opción (1-3): ")

        if choice == '1':
            device = showDevices()
            if device:
                print(f"Guardando configuración del dispositivo {device}...\n")
                result = nr.filter(name=device).run(task=saveAuthorizeConfig)
                #print_result(result)
                
        elif choice == '2':
            device = showDevices()
            if device:
                print(f"Realizando auditoría de configuración en {device}...\n")
                result = nr.filter(name=device).run(task=detectConfig)
                #print_result(result)
                
        elif choice == '3':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Ejecutar el menú interactivo
if __name__ == "__main__":
    show_menu()
