from os import makedirs, path

from yaml import dump as yaml_dump

from .constants import LAUNCH_TIME


class YamlOutputFile:
    __slots__ = ("file_path", "folder_path", "index", "main_data", "name")

    def __init__(
        self,
        *,
        pattern: dict[any, dict],
        name: str = LAUNCH_TIME.strftime("%d-%m-%Y-%H-%M-%S"),
        folder_path: str = "output",
    ) -> None:
        self.main_data = pattern
        self.name = f"{name}.yml"
        self.folder_path = folder_path

        self.file_path = path.join(self.folder_path, self.name)
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
        makedirs(self.folder_path, exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as file:
            yaml_dump(self.main_data, file)
