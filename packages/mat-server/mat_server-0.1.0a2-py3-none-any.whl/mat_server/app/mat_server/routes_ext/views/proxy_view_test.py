from unittest import mock

import flask.views
import pytest

from mat_server import AppContainer
from mat_server.domain import use_cases, entities


@pytest.fixture
def container():
    container = AppContainer()
    return container


@pytest.fixture
def app(container):
    mat_server = container.MatServer()
    return mat_server.get_app()


def test_return_mock_response(client, container):
    check_if_mock_response_exists_use_case = mock.MagicMock(spec=use_cases.CheckIfMockResponseExistsUseCase)
    check_if_mock_response_exists_use_case.execute.return_value = True

    get_mock_response_use_case = mock.MagicMock(spec=use_cases.GetMockResponseUseCase)
    get_mock_response_use_case.execute.return_value = entities.ServerResponse(
        raw_body=b'raw_data',
        headers={'name': 'value'},
        status_code=200,
    )
    get_proxy_server_response_use_case = mock.MagicMock(spec=use_cases.GetProxyServerResponseUseCase)

    with container.DomainContainer.CheckIfMockResponseExistsUseCase.override(check_if_mock_response_exists_use_case):
        with container.DomainContainer.GetMockResponseUseCase.override(get_mock_response_use_case):
            with container.DomainContainer.GetProxyServerResponseUseCase.override(get_proxy_server_response_use_case):
                resp = client.get(flask.url_for('proxy', path='path', name='name'), headers={'name': 'name'})
                assert resp.status_code == 200
                assert resp.headers['name'] == 'value'
                assert resp.data == b'raw_data'


def test_return_proxy_server_response(client, container):
    check_if_mock_response_exists_use_case = mock.MagicMock(spec=use_cases.CheckIfMockResponseExistsUseCase)
    check_if_mock_response_exists_use_case.execute.return_value = False

    get_mock_response_use_case = mock.MagicMock(spec=use_cases.GetMockResponseUseCase)

    get_proxy_server_response_use_case = mock.MagicMock(spec=use_cases.GetProxyServerResponseUseCase)
    get_proxy_server_response_use_case.execute.return_value = entities.ServerResponse(
        raw_body=b'raw_data',
        headers={'name': 'value'},
        status_code=200,
    )

    with container.DomainContainer.CheckIfMockResponseExistsUseCase.override(check_if_mock_response_exists_use_case):
        with container.DomainContainer.GetMockResponseUseCase.override(get_mock_response_use_case):
            with container.DomainContainer.GetProxyServerResponseUseCase.override(get_proxy_server_response_use_case):
                resp = client.get(flask.url_for('proxy', path='path', name='name'), headers={'name': 'name'})
                assert resp.status_code == 200
                assert resp.headers['name'] == 'value'
                assert resp.data == b'raw_data'
