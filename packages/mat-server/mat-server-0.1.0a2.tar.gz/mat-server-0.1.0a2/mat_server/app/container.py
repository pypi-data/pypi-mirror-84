import codecs
import os
import shutil

import flask
import waitress
import yaml
from dependency_injector import containers, providers
from dependency_injector.ext import flask as di_flask

from mat_server.app.cli import create_cli
from mat_server.app.manager import Manager
from mat_server.app.mat_server import MatServer, RoutesExt
from mat_server.app.mat_server.routes_ext import views
from mat_server.domain import use_cases
from mat_server.infrastructure import helpers, repositories


class DomainContainer(containers.DeclarativeContainer):
    ProjectDataHelper = providers.Singleton(
        helpers.ProjectDataHelper,
    )

    DataRetrieverHelper = providers.Singleton(
        helpers.DataRetrieverHelper,
    )

    FileHelper = providers.Singleton(
        helpers.FileHelper,
        os_module=providers.Object(os),
        codecs_module=providers.Object(codecs),
        shutil_module=providers.Object(shutil),
        yaml_module=providers.Object(yaml),
    )

    RequestHelper = providers.Singleton(
        helpers.HTTPRequestHelper,
    )

    MatConfigRepository = providers.Singleton(
        repositories.MatConfigRepository,
        file_helper=FileHelper,
        data_retriever_helper=DataRetrieverHelper,
    )

    CheckConfigUseCase = providers.Singleton(
        use_cases.CheckConfigUseCase,
        mat_config_repository=MatConfigRepository,
    )

    GenerateDefaultConfigUseCase = providers.Singleton(
        use_cases.GenerateDefaultConfigUseCase,
        project_data_helper=ProjectDataHelper,
        file_helper=FileHelper,
    )

    CheckIfMockResponseExistsUseCase = providers.Singleton(
        use_cases.CheckIfMockResponseExistsUseCase,
        mat_config_repository=MatConfigRepository,
    )

    GetMockResponseUseCase = providers.Singleton(
        use_cases.GetMockResponseUseCase,
        mat_config_repository=MatConfigRepository,
        file_helper=FileHelper,
    )

    GetProxyServerResponseUseCase = providers.Singleton(
        use_cases.GetProxyServerResponseUseCase,
        mat_config_repository=MatConfigRepository,
        request_helper=RequestHelper,
    )


class AppContainer(containers.DeclarativeContainer):
    DomainContainer = providers.Container(DomainContainer)

    FlaskApp = providers.Singleton(flask.Flask, __name__)

    ProxyView = di_flask.ClassBasedView(
        views.ProxyView,
        check_if_mock_response_exists_use_case=DomainContainer.CheckIfMockResponseExistsUseCase,
        get_mock_response_use_case=DomainContainer.GetMockResponseUseCase,
        get_proxy_server_response_use_case=DomainContainer.GetProxyServerResponseUseCase,
    )

    RoutesExt = providers.Singleton(
        RoutesExt,
        proxy_view_class=ProxyView.provider,
    )

    MatServer = providers.Singleton(
        MatServer,
        flask_app=FlaskApp,
        routes_ext=RoutesExt,
        wsgi_application_prod_serve_func=waitress.serve,
    )

    Manager = providers.Factory(
        Manager,
        generate_default_config_use_case=DomainContainer.GenerateDefaultConfigUseCase,
        check_config_use_case=DomainContainer.CheckConfigUseCase,
        mat_server=MatServer,
    )

    create_cli = providers.Callable(
        create_cli,
        Manager,
    )
