import flask.views

from mat_server.domain import use_cases, entities


class ProxyView(flask.views.View):

    def __init__(self,
                 check_if_mock_response_exists_use_case: use_cases.CheckIfMockResponseExistsUseCase,
                 get_mock_response_use_case: use_cases.GetMockResponseUseCase,
                 get_proxy_server_response_use_case: use_cases.GetProxyServerResponseUseCase,
                 ):
        self._check_if_mock_response_exists_use_case = check_if_mock_response_exists_use_case
        self._get_mock_response_use_case = get_mock_response_use_case
        self._get_proxy_server_response_use_case = get_proxy_server_response_use_case

    def dispatch_request(self, path: str):  # type: ignore
        request = entities.ClientRequest(
            method=flask.request.method,
            path=path,
            query_string=flask.request.query_string.decode(),
            headers={name: value for name, value in flask.request.headers.items()},
            raw_body=flask.request.stream.read()
        )

        # 檢查是否需要 mock response
        existed = self._check_if_mock_response_exists_use_case.execute(request)

        # 如果需要 mock
        if existed:
            mock_response = self._get_mock_response_use_case.execute(request)
            return self._transform_response_to_flask_response(mock_response)

        # 如果不需要 mock，直接轉給 proxy server
        else:
            proxy_server_response = self._get_proxy_server_response_use_case.execute(request)
            return self._transform_response_to_flask_response(proxy_server_response)

    @staticmethod
    def _transform_response_to_flask_response(response: entities.ServerResponse):
        return flask.Response(
            response=response.raw_body,
            headers=response.headers,
            status=response.status_code,
        )
