# Repositorio de Inventario de Configuraciones

Aqui se guardan todos los archivos necesarios para el funcionamiento del programa y configuracion de la libreria Nornir.

## Archivos

### `hosts.yaml`

Este archivo define los dispositivos individuales que Nornir gestionará. Cada dispositivo se representa como una entrada con un nombre único, y se puede incluir información como la dirección IP, el nombre de usuario, la contraseña y otros parámetros específicos del dispositivo.

## Archivos

### `groups.yaml`

Este archivo permite agrupar dispositivos por características comunes. Los grupos pueden incluir uno o más dispositivos definidos en el archivo hosts.yaml, lo que facilita la gestión de múltiples dispositivos a la vez. Solo se agrego de ejemplo, no tiene configuracion crucial de los equipos.

## Archivos

### `default.yaml`

Este archivo define valores predeterminados que se aplican a todos los dispositivos. Puedes establecer configuraciones generales que se aplicarán automáticamente a todos los dispositivos en el inventario, a menos que se sobrescriban en los archivos hosts.yaml o groups.yaml.