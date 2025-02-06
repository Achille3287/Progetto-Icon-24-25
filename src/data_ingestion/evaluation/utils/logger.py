import logging
import os

def setup_logger(log_file_path='system.log'):
    """
    Configura il logger per registrare i messaggi in un file di log.
    
    Args:
        log_file_path (str): Percorso del file di log.
    """
    log_dir = os.path.dirname(log_file_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger()

def log_message(logger, message, level='info'):
    """
    Registra un messaggio nel file di log.
    
    Args:
        logger (logging.Logger): L'istanza del logger.
        message (str): Messaggio da registrare.
        level (str): Livello del messaggio ('info', 'warning', 'error').
    """
    if level == 'info':
        logger.info(message)
    elif level == 'warning':
        logger.warning(message)
    elif level == 'error':
        logger.error(message)