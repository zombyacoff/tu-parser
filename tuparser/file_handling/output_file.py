from ..constants import LAUNCH_TIME
from .file_manager import FileManager


class YAMLOutputFile:
    def __init__(
        self,
        data: dict[str | int, dict],
        name: str = LAUNCH_TIME.strftime("%d-%m-%Y-%H-%M-%S"),
        folder_path: str = "output",
    ) -> None:
        self.main_data = data
        self.name = f"{name}.yml"
        self.folder_path = folder_path

        self.file_path = FileManager.join_paths(self.folder_path, self.name)

        self.index = 0

    def write_data(self, *data: any) -> None:
        """Writes data to the main dictionary,
        which will be stored in a YAML output file after parsing

        Example: write_data('Alexey', 'Yaroslav', 'TUParser')

        NOTE: the dictionary should have at least as many keys as the values passed
        """
        self.index += 1
        for i, key in enumerate(self.main_data):
            self.main_data[key][self.index] = data[i]

    def complete(self) -> None:
        FileManager.create_folder(self.folder_path)
        FileManager.dump_yaml(self.file_path, self.main_data)
