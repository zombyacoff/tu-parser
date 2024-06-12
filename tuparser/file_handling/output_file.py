from dataclasses import dataclass, field

from ..constants import LAUNCH_TIME
from .file_manager import FileManager


@dataclass
class YAMLOutputFile:
    data: dict[any, any]
    folder_path: str = field(default="output")
    name: str = f"{LAUNCH_TIME.strftime("%d-%m-%Y-%H-%M-%S")}.yml"
    index: int = 1

    def __post_init__(self) -> None:
        self.file_path = FileManager.join_paths(self.folder_path, self.name)

    def write_output(self, data: tuple[any]) -> None:
        for i, key in enumerate(self.data):
            self.data[key][self.index] = data[i]
        self.index += 1

    def complete_output(self) -> None:
        FileManager.create_folder(self.folder_path)
        FileManager.dump_yaml(self.file_path, self.data)
