from ..constants import LAUNCH_TIME
from .file_manager import FileManager


class YAMLOutputFile:
    def __init__(
        self, data: dict[str, dict], folder_path: str = "parser-output"
    ) -> None:
        self.output_data = data
        self.output_folder_path = folder_path

        self.launch_time_format = LAUNCH_TIME.strftime("%d-%m-%Y-%H-%M-%S")
        self.output_file_name = f"{self.launch_time_format}.yml"
        self.output_file_path = FileManager.join_paths(
            self.output_folder_path, self.output_file_name
        )

        self.output_file_index: int = 1

    def write_output(self, data: tuple[any]) -> None:
        for i, key in enumerate(self.output_data):
            self.output_data[key][self.output_file_index] = data[i]

        self.output_file_index += 1

    def complete_output(self) -> None:
        FileManager.create_folder(self.output_folder_path)
        FileManager.dump_yaml(self.output_file_path, self.output_data)
