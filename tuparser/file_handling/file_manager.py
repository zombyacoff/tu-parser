import os

import yaml


class FileManager:
    @staticmethod
    def create_folder(folder_path: str) -> None:
        os.makedirs(folder_path, exist_ok=True)

    @staticmethod
    def join_paths(*paths: str) -> str:
        return os.path.join(*paths)

    @staticmethod
    def save_file(file_path: str, data: bytes) -> None:
        with open(file_path, "wb") as file:
            file.write(data)

    @staticmethod
    def load_yaml(file_path: str) -> dict[any, any]:
        with open(file_path, encoding="utf-8") as file:
            return yaml.safe_load(file)

    @staticmethod
    def dump_yaml(file_path: str, data: dict[any, any]) -> None:
        with open(file_path, "w", encoding="utf-8") as file:
            yaml.dump(data, file)
