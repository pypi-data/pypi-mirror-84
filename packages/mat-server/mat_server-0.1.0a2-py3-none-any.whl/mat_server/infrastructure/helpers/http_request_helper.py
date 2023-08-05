import requests

from mat_server.domain import helpers, entities


class HTTPRequestHelper(helpers.HTTPRequestHelperBase):  # pragma: no cover

    def __init__(self):
        self._session = requests.Session()

    def send(self, request: entities.HTTPRequest) -> entities.HTTPResponse:
        req = requests.Request(
            method=request.method,
            url=request.url,
            headers=request.headers,
            data=request.raw_body,
        )
        resp = self._session.send(req.prepare(), stream=True)

        return entities.HTTPResponse(
            raw_data=resp.raw.read(),
            status_code=resp.status_code,
            headers={
                name.lower(): value
                for name, value in resp.headers.items()
            },
        )
