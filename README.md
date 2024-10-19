# Proyecto de Detección y Reversión de Configuraciones No Autorizadas

## Descripción

Este proyecto utiliza Nornir, una biblioteca de automatización de redes en Python, para detectar y revertir configuraciones no autorizadas en dispositivos de red. El objetivo es garantizar que los dispositivos mantengan una configuración autorizada, protegiendo así la integridad de la red.

## Requisitos

Para ejecutar este proyecto, asegúrate de tener instalado Python y las siguientes bibliotecas:

- [Nornir](https://nornir.readthedocs.io/en/latest/)
- [Nornir-Netmiko](https://nornir-netmiko.readthedocs.io/en/latest/)
- [Nornir-NAPALM](https://nornir-napalm.readthedocs.io/en/latest/)
- [Difflib](https://docs.python.org/3/library/difflib.html)

Puedes instalar las bibliotecas necesarias utilizando `pip`:

```bash
pip install nornir nornir-netmiko nornir-napalm
