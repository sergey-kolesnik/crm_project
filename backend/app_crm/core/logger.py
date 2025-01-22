import logging
from pathlib import Path
import sys

LOG_FILE_PATH = Path("logs/crm_app.log")
LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)


class CrmLogger:
    """
    Класс для настройки и управления логированием приложения.
    """

    def __init__(self, logger_name: str, log_file_path: str = "logs/crm_app.log"):
        """
        Инициализирует логгер
        """

        self.log_file_path = Path(log_file_path)
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s")

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        self.logger.addHandler(stdout_handler)

        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log(self, level: int, message: str):
        """
        Логирует сообщение с указанным уровнем.

        Args:
            level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            message: Сообщение для логирования.
        """
        self.logger.log(level, message)

    def debug(self, message: str):
       self.log(logging.DEBUG, message)

    def info(self, message: str):
        self.log(logging.INFO, message)


    def warning(self, message: str):
        self.log(logging.WARNING, message)


    def error(self, message: str):
        self.log(logging.ERROR, message)


    def critical(self, message: str):
      self.log(logging.CRITICAL, message)
    


crm_logger = CrmLogger("crm_logger_app")