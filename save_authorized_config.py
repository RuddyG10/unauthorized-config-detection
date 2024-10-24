from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
import logging

#Configuracion del log
logging.basicConfig(
    filename="./logs/error_log.log", #Errores,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s %(message)s"
)
# Inicializa Nornir usando los archivos de configuración
nr = InitNornir(config_file="config.yaml")
# Tarea para obtener el running-config
def saveAuthorizeConfig(task):
    try:
        # Usar NAPALM para obtener el running-config
        result = task.run(
            napalm_get,
            getters=["config"],  # Usar el getter "config" para obtener el running-config
        )

        running_config = result.result["config"]["running"]

        # Guardar en archivo
        filename = f"{task.host.name}_running_config_authorized.txt"
        with open("./authorize_config/"+filename, "w") as file:
            file.write(running_config)
        print(f"Running config guardado en {filename}")
    except Exception as ex:
        print(f"Ocurrio un error durante el guardado del dispositivo: {task.host.name}")
        logging.error(f"Error en el dispositivo {task.host.name}: {ex}",exc_info=True)

#result = nr.run(task=saveAuthorizeConfig)
#print_result(result)