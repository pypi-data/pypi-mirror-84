import urllib.parse
from typing import Dict, Optional, List

from mat_server.domain import base_types


class RouteResponseConfig(base_types.Entity):
    def __init__(self,
                 file_path: Optional[str] = None,
                 data: Optional[str] = None):
        self.file_path = file_path
        self.data = data

    def __hash__(self):
        return hash((
            self.file_path,
            self.data,
        ))

    def __eq__(self, other):
        if not isinstance(other, RouteResponseConfig):
            return False
        return hash(self) == hash(other)


class RouteConfig(base_types.Entity):
    def __init__(self,
                 listen_path: str,
                 method: str,
                 status_code: int,
                 query: Optional[Dict[str, List[str]]],
                 response: RouteResponseConfig):
        self.listen_path = listen_path
        self.method = method
        self.status_code = status_code
        self.query = query
        self.response = response

    def check_if_query_string_matches_config(self, query_string: str) -> bool:
        if self.query:
            query_params = urllib.parse.parse_qs(query_string)
            for key, values in self.query.items():
                if set(values) != set(query_params.get(key, [])):
                    return False
        return True

    def __hash__(self):
        return hash((
            self.listen_path,
            self.method,
            self.status_code,
            frozenset((key, frozenset(value)) for key, value in self.query.items()),
            self.response,
        ))

    def __eq__(self, other):
        if not isinstance(other, RouteConfig):
            return False
        return hash(self) == hash(other)
