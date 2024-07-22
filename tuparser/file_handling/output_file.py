from ..constants import LAUNCH_TIME
from .file_manager import FileManager


class YAMLOutputFile:
    __slots__ = ("file_path", "folder_path", "index", "main_data", "name")
    FORMATTED_LAUNCH_TIME = LAUNCH_TIME.strftime("%d-%m-%Y-%H-%M-%S")

    def __init__(self, config: dict) -> None:
        self.main_data = config.get("pattern")
        self.name = config.get("name", f"{self.FORMATTED_LAUNCH_TIME}.yml")
        self.folder_path = config.get("folder_path", "output")

        self.file_path = FileManager.join_paths(self.folder_path, self.name)
        self.index = 1

    def write_data(self, *data: any) -> None:
        """Writes data to the main dictionary,
        which will be stored in a YAML output file after parsing

        Example: write_data('Alexey', 'Yaroslav', 'TUParser')

        NOTE: the dictionary should have at least as many keys as the values passed
        """
        for i, key in enumerate(self.main_data):
            self.main_data[key][self.index] = data[i]
        self.index += 1

    def complete(self) -> None:
        FileManager.create_folder(self.folder_path)
        FileManager.dump_yaml(self.file_path, self.main_data)
