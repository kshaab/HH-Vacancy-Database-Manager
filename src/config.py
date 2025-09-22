from configparser import ConfigParser
import os
def config(filename="database.ini", section="postgresql"):
    """Чтение параметров для подключения"""
    parser = ConfigParser()
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
    parser.read(file_path)

    if parser.has_section(section):
        return {param[0]: param[1] for param in parser.items(section)}

    raise Exception(f"Section {section} not found in {filename}")



