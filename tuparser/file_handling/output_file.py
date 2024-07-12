from ..constants import LAUNCH_TIME
from ..utils import ConsoleColor, call_counter
from .file_manager import FileManager


class YAMLOutputFile:
    def __init__(
        self,
        data: dict[any, dict],
        *,
        folder_path: str = "output",
        complete_message: bool = True,
    ):
        self.data = data
        self.folder_path = folder_path
        self.complete_message = complete_message

        self.name = f"{LAUNCH_TIME.strftime('%d-%m-%Y-%H-%M-%S')}.yml"
        self.file_path = FileManager.join_paths(self.folder_path, self.name)

    @call_counter
    def write_data(self, *data: any) -> None:
        """Writes data to the dictionary 'data'

        Example:
            write_data('Alexey', 'Yaroslav', 'TUParser')

        NOTE: the dictionary should have at least as many keys as the values passed
        """
        for i, key in enumerate(self.data):
            self.data[key][self.write_data.calls] = data[i]

    def complete(self) -> None:
        FileManager.create_folder(self.folder_path)
        FileManager.dump_yaml(self.file_path, self.data)

        if self.complete_message:
            print(
                ConsoleColor.paint_info(
                    f"Output file path: {self.file_path}",
                )
            )
