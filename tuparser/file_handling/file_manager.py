import os

import yaml

YAML_EXTENSIONS = (".yml", ".yaml")


class FileManager:
    @staticmethod
    def create_folder(folder_path: str) -> None:
        os.makedirs(folder_path, exist_ok=True)

    @staticmethod
    def join_paths(*paths: str) -> str:
        return os.path.join(*paths)

    @staticmethod
    def dump_binary_data(file_path: str, data: bytes) -> None:
        with open(file_path, "wb") as file:
            file.write(data)

    @staticmethod
    def load_yaml(file_path: str) -> dict[any, any] | None:
        """Loads a YAML file and returns a dictionary

        :param file_path: (String) YAML file path without file extension

        :return: dictionary if successful, None otherwise
        """
        for extension in YAML_EXTENSIONS:
            try:
                with open(file_path + extension, encoding="utf-8") as file:
                    return yaml.safe_load(file)
            except FileNotFoundError:
                ...

    @staticmethod
    def dump_yaml(file_path: str, data: dict[any, any]) -> None:
        """Dump a dictionary into a YAML file

        :param file_path: (String) YAML file path
        :param data: dictionary to dump
        """
        with open(file_path, "w", encoding="utf-8") as file:
            yaml.dump(data, file)
