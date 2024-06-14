from dataclasses import dataclass, field

from ..constants import LAUNCH_TIME
from ..utils import call_counter
from .file_manager import FileManager


@dataclass
class YAMLOutputFile:
    data: dict[any, any]
    folder_path: str = field(default="output")

    name: str = f"{LAUNCH_TIME.strftime("%d-%m-%Y-%H-%M-%S")}.yml"

    def __post_init__(self) -> None:
        self.file_path = FileManager.join_paths(self.folder_path, self.name)

    @call_counter
    def write_data(self, *data: any) -> None:
        """Writes data to the dictionary 'data'
        
        :param data: data to write. If multiple values need to be written,
        they should be passed as a tuple.
        
        Example:
            write_data('Alexey', 'Yaroslav', 'TUParser')
        
        NOTE: the dictionary should have at least as many keys as the values passed.
        """
        for i, key in enumerate(self.data):
            self.data[key][self.write_data.calls] = data[i]

    def complete(self) -> None:
        FileManager.create_folder(self.folder_path)
        FileManager.dump_yaml(self.file_path, self.data)
