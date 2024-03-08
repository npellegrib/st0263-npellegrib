# st0263-2024-1 Tópicos especiales en telemática 
#
# Estudiante(s): Neller Pellegrino, npellegrib@eafit.edu.co
#
# Profesor: Juan Carlos Montoya, jcmontoy@eafit.edu.co
#
# Nombre del proyecto: Desarrollo de un Sistema P2P para Compartición de Archivos
#
# 1. Breve descripción de la actividad
#
Este proyecto implementa un sistema P2P (Peer-to-Peer) para la compartición de archivos, permitiendo la transferencia y descubrimiento de archivos entre nodos de manera distribuida y descentralizada.
## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
- Comunicación entre peers mediante gRPC.
- Transferencia de archivos en modo ECO/DUMMY.
- Descubrimiento dinámico de nuevos peers.
- Concurrencia en el servidor para manejar múltiples solicitudes.

## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
- flooding

# 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
Se utilizó una arquitectura basada en microservicios, comunicación gRPC para la interacción entre peers, y RabbitMQ para la actualización de archivos entre peers.

# 3. Descripción del ambiente de desarrollo y técnico
- Lenguaje de programación: Python
- Librerías principales: gRPC, Flask, aiofiles, pika (RabbitMQ)
- Versiones: Python 3.8, gRPC 1.38, Flask 2.0, aiofiles 0.7, pika 1.2

## Como se compila y ejecuta
Ejecutar `python server.py` para iniciar el servidor y `python client.py` para el cliente. Usar `python client.py discover [peer_address]` para descubrimiento de peers.

## Descripción y como se configuran los parámetros del proyecto
El archivo `config/config.json` contiene parámetros configurables como IP del servidor, puerto, y directorio de archivos.

# 4. Descripción del ambiente de EJECUCIÓN
Similar al ambiente de desarrollo, desplegado en AWS EC2 para pruebas en un entorno distribuido.

# IP o nombres de dominio en nube o en la máquina servidor
Ejemplo: https://us-east-1.console.aws.amazon.com/ec2-instance-connect/ssh?connType=standard&instanceId=i-072b0788c8d41a15a&osUser=ubuntu&region=us-east-1&sshPort=22#/

# 5. Otra información relevante para esta actividad
El sistema permite la expansión y adaptabilidad a nuevos requerimientos, con la posibilidad de integrar funcionalidades de sincronización real de archivos en futuras versiones.

# Referencias:
- Documentación oficial de gRPC
- Tutoriales de Flask y RabbitMQ
## [URL de gRPC](https://grpc.io/docs/)
## [URL de Flask](https://flask.palletsprojects.com/en/2.0.x/)
## [URL de RabbitMQ](https://www.rabbitmq.com/documentation.html)
