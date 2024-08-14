import logging
import os
from logging.handlers import RotatingFileHandler

# Definir o nível de log baseado na variável de ambiente
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()

# Formato personalizado para o log
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)

# Configurar o logger
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

# Configurar o handler de console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Configurar o handler de arquivo com rotação
file_handler = RotatingFileHandler('app.log', maxBytes=10**6, backupCount=5)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
