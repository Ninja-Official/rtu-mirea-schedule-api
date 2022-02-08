import logging
import sys
import os.path


def setup_logger(path_to_error_log, logger_name):
    """Инициализация объекта для логирования информации

    Parameters
    ----------
    path_to_error_log: str, обязательный
        Путь и название файла, куда будут сохраняться логи. Пример: errors.log
    logger_name: str или None, обязательный
        Название логгера

    Вернёт logger с указанным именем (logger_name), если имя указано как None, то вернёт корневой логгер
    """
    logging_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] - %(message)s')
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(path_to_error_log)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging_formatter)

    # логирование в консоль
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging_formatter)
    logger.addHandler(handler)
    logger.addHandler(file_handler)
    return logger


async def start_parsing():
    """Главная функция, реализующая выполнение парсинга данных с помощью
    интерфейса класса Parse
    """
    # во избежание рекурсивного включения
    # from .parser import ExcelParser, PDFParse
    from .excel_parser import ExcelParser
    from .college_parser import CollegeParser
    from .downloader import Downloader
    from .excel_formatter import ExcelFormatter
    from .college_formatter import CollegeFormatter
    from ..database.database import get_database

    downloader = Downloader(
        path_to_error_log='downloader.log', base_file_dir='documents/')
    downloader.run()

    # директория, в которой хранятся excel документы
    xlsx_dir = 'documents/semester'
    college_dir = 'documents/college'
    for path, _, files in os.walk(xlsx_dir):
        for file_name in files:
            path_to_file = os.path.join(path, file_name)
            file_extension = os.path.splitext(path_to_file)[1]
            if file_extension == '.pdf':
                pass
                # pdf_parser = PDFParser(path_to_file,
                #                        path_to_error_log='pdf_parser.log')
                # pdf_parser.parse()
            else:
                excel_parser = ExcelParser(await get_database(), path_to_file, 'semester', ExcelFormatter(),
                                           path_to_error_log='excel_parser.log')
                excel_parser.parse()
    for path, _, files in os.walk(college_dir):
        for file_name in files:
            path_to_file = os.path.join(path, file_name)
            college_parser = CollegeParser(await get_database(),
                                           path_to_file, CollegeFormatter(), path_to_error_log='excel_parser.log')
            college_parser.parse()