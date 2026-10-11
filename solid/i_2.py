
from abc import ABC, abstractmethod


class Readable(ABC):
    @abstractmethod
    def read(self, path: str) -> str:
        pass


class Writable(ABC):
    @abstractmethod
    def write(self, path: str, content: str) -> None:
        pass


class Compressible(ABC):
    @abstractmethod
    def compress(self, path: str) -> None:
        pass


class ReadOnlyFileReader(Readable):
    def read(self, path: str) -> str:
        return f"Reading {path}"


class FileWriter(Writable):
    def write(self, path: str, content: str) -> None:
        print(f"Writing to {path}: {content}")


class ArchiveCompressor(Compressible):
    def compress(self, path: str) -> None:
        print(f"Compressing {path}")
