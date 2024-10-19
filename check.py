from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from napalm import get_network_driver

"""Script para revisar si el dispositivo admite edicion de archivos.
    Esto es importante para ejecutar el script main, ya que este necesita
    editar archivos."""
# Inicializa Nornir usando los archivos de configuración
nr = InitNornir(config_file="config.yaml")

def check_file_system_access(task):
    # Usar NAPALM para obtener el driver del dispositivo
    driver = get_network_driver(task.host.platform)

    # Establecer conexión con el dispositivo usando NAPALM
    optional_args = {"port": task.host.port}  # Si es necesario incluir argumentos opcionales como el puerto
    device = driver(
        hostname=task.host.hostname,
        username=task.host.username,
        password=task.host.password,
        optional_args=optional_args
    )

    device.open()

    # Listar el sistema de archivos
    try:
        file_system_output = device.cli(["dir"])
        print(f"Contenido del sistema de archivos en {task.host.name}:")
        print(file_system_output)
    except Exception as e:
        print(f"No se pudo acceder al sistema de archivos en {task.host.name}: {e}")

    # Cerrar la conexión al dispositivo
    device.close()

# Ejecutar la tarea para verificar el acceso al sistema de archivos
result = nr.run(task=check_file_system_access)
print_result(result)
