import logging

# Crear un logger personalizado
logger = logging.getLogger('mi_logger')
logger.setLevel(logging.DEBUG)

# Crear un manejador de archivo (handler)
file_handler = logging.FileHandler('logs/mi_log.log')
file_handler.setLevel(logging.ERROR)

# Crear un manejador de consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
# Crear formato para los logs
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Asociar el formato a los manejadores
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
# Asociar los manejadores al logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)