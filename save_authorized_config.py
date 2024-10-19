from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get

# Inicializa Nornir usando los archivos de configuración
nr = InitNornir(config_file="config.yaml")
# Tarea para obtener el running-config
def saveAuthorizeConfig(task):

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

result = nr.run(task=saveAuthorizeConfig)
#print_result(result)