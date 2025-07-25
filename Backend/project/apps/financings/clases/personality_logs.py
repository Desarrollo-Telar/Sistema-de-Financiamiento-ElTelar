import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Utiliza StreamHandler para enviar los logs a stdout
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
