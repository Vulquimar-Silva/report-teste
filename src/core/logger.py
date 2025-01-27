import logging
import os
from logging.handlers import RotatingFileHandler

# Diretório para armazenar logs
LOG_DIR = "logs"
try:
    os.makedirs(LOG_DIR, exist_ok=True)
except Exception as e:
    print(f"[ERROR] Falha ao criar diretório de logs: {e}")

# Definir níveis de log válidos
VALID_LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()

# Validar nível de log
if log_level not in VALID_LOG_LEVELS:
    logging.warning(f"Nível de log inválido '{log_level}'. Usando 'INFO' como padrão.")
    log_level = 'INFO'

# Configuração do logger principal
logger = logging.getLogger('report-algar')

# Evitar reconfigurações se o logger já estiver configurado
if not logger.hasHandlers():
    # Formato personalizado para o log
    log_format = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    formatter = logging.Formatter(log_format)

    # Configurar handler de console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Configurar handler de arquivo com rotação
    log_file_path = os.path.join(LOG_DIR, 'app.log')
    file_handler = RotatingFileHandler(
        log_file_path, maxBytes=5 * 10**6, backupCount=5, encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Configurar nível de log
    logger.setLevel(log_level)

    # Mensagem de inicialização
    env = os.getenv('ENV', 'development')
    if env == 'production':
        logger.info(f"Logger iniciado em modo produção com nível '{log_level}'.")
    else:
        logger.debug(f"Logger configurado com nível '{log_level}', armazenando em '{log_file_path}'.")

# Função auxiliar para alterar o nível de log em runtime
def set_log_level(level):
    """
    Altera dinamicamente o nível de log.
    
    Args:
        level (str): Novo nível de log. Valores válidos: DEBUG, INFO, WARNING, ERROR, CRITICAL.
    """
    if level.upper() in VALID_LOG_LEVELS:
        current_level = logging.getLevelName(logger.level)
        if current_level != level.upper():
            logger.setLevel(level.upper())
            logger.info(f"Nível de log alterado para {level.upper()}.")
    else:
        logger.warning(f"Tentativa de alterar para um nível de log inválido: {level}.")
