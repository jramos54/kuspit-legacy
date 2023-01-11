# import logging
# from colorama import Fore, Style

# class Logger:
#     def __init__(self, name=__name__, level=logging.INFO):
#         self.logger = logging.getLogger(name)
#         self.logger.setLevel(level)
        
#         formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
#         console_handler = logging.StreamHandler()
#         console_handler.setFormatter(formatter)
#         self.logger.addHandler(console_handler)
        
#     def _colorize(self, message, color):
#         return f"{color}{message}{Style.RESET_ALL}"
        
#     def info(self, message):
#         self.logger.info(self._colorize(message, Fore.GREEN))
        
#     def warning(self, message):
#         self.logger.warning(self._colorize(message, Fore.YELLOW))
        
#     def error(self, message):
#         self.logger.error(self._colorize(message, Fore.RED))
        
#     def critical(self, message):
#         self.logger.critical(self._colorize(message, Fore.RED + Style.BRIGHT))
        
#     def assert_pass(self, message):
#         self.logger.info(self._colorize(f"ASSERT PASS: {message}", Fore.GREEN))
        
#     def assert_fail(self, message):
#         self.logger.error(self._colorize(f"ASSERT FAIL: {message}", Fore.RED))

import logging
from colorama import Fore, Style, init

init(autoreset=True)  # Asegura que los efectos de colorama se resetean automáticamente

class Logger:
    def __init__(self, name=__name__, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Usa un handler personalizado para aplicar el color
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.CustomFormatter())
        self.logger.addHandler(console_handler)

    class CustomFormatter(logging.Formatter):
        # Define un formato base para el log
        base_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

        # Diccionario de colores por nivel de log
        level_colors = {
            logging.DEBUG: Fore.BLUE,
            logging.INFO: Fore.GREEN,
            logging.WARNING: Fore.YELLOW,
            logging.ERROR: Fore.RED,
            logging.CRITICAL: Fore.RED + Style.BRIGHT
        }

        def format(self, record):
            # Selecciona el color basado en el nivel del log
            color = self.level_colors.get(record.levelno, Fore.WHITE)
            message = logging.Formatter(self.base_format).format(record)
            return color + message + Style.RESET_ALL

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
    
    def assert_pass(self, message):
        self.logger.info(f"ASSERT PASS: {message}")

    def assert_fail(self, message):
        self.logger.error(f"ASSERT FAIL: {message}")
