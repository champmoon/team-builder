import shutil
from pathlib import Path
from typing import BinaryIO

from app.conf.settings import settings


class FileNotExist(Exception):
    def __init__(self, msg: str = "No arguments bytes_buffer or filename") -> None:
        super().__init__(msg)


class SystemFile:
    static_dir = settings.STATIC_FILES_DIR
    hostname = settings.SERVER_HOSTNAME

    def __init__(
        self,
        *,
        bytes_buffer: BinaryIO | None = None,
        dir_path: str,
        filename: str | None = None,
    ) -> None:
        self.bytes_buffer = bytes_buffer
        self.dir_path = dir_path
        self.filename = filename

        if self.dir_path[-1] != "/":
            self.dir_path += "/"

    def save(self) -> str:
        """
        save file in a `static directory`
        return `url` to access the file
        """
        if self.bytes_buffer is None or self.filename is None:
            raise FileNotExist

        file_path = f"{self.static_dir}/{self.dir_path}{self.filename}"

        file = Path(file_path)

        file.parent.mkdir(parents=True, exist_ok=True)

        with file.open("wb") as f:
            f.write(self.bytes_buffer.read())

        return self.hostname + file_path
        # return file_path

    def delete(self) -> None:
        """
        delete file in a `static directory`
        """
        try:
            shutil.rmtree(f"{self.static_dir}/{self.dir_path}")
        except Exception:
            pass
