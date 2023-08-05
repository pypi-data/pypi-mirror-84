from typing import Dict

from mat_server.domain import base_types


class HTTPResponse(base_types.Entity):

    def __init__(self,
                 raw_data: bytes,
                 status_code: int,
                 headers: Dict[str, str]):
        self.raw_data = raw_data
        self.status_code = status_code
        self.headers = headers
