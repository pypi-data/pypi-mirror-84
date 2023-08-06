import abc
from typing import Any, List

from mat_server.domain import base_types


class FileHelperBase(base_types.Helper):

    @abc.abstractmethod
    def join_file_paths(self, *paths: str) -> str:
        """連結檔名"""

    @abc.abstractmethod
    def read_bytes(self, target_path: str) -> bytes:
        """讀取檔案資料"""
        pass

    @abc.abstractmethod
    def read_yaml(self, target_path: str) -> Any:
        """讀取 yaml 檔案"""
        pass

    @abc.abstractmethod
    def copy_folder(self, src_path: str, dest_path: str):
        """複製資料夾 (支援遞迴複製)"""
        pass
