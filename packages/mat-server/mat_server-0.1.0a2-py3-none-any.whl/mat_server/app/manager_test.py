from unittest import mock

from mat_server.app.manager import Manager
from mat_server.app.mat_server import MatServer
from mat_server.domain import use_cases, entities


def test_create_config(capsys):
    generate_default_config_use_case = mock.MagicMock(spec=use_cases.GenerateDefaultConfigUseCase)
    check_config_use_case = mock.MagicMock(spec=use_cases.CheckConfigUseCase)
    mat_server = mock.MagicMock(spec=MatServer)

    manager = Manager(
        generate_default_config_use_case=generate_default_config_use_case,
        check_config_use_case=check_config_use_case,
        mat_server=mat_server,
    )

    manager.create_config()

    captured = capsys.readouterr()
    assert captured.out == '初始化 mat 設定 ...\nmat-data 資料夾建立完成\n'
    generate_default_config_use_case.execute.assert_called_once()


def test_check_failed(capsys):
    generate_default_config_use_case = mock.MagicMock(spec=use_cases.GenerateDefaultConfigUseCase)

    check_config_use_case = mock.MagicMock(spec=use_cases.CheckConfigUseCase)
    check_config_use_case.execute.return_value = entities.ValidationReport(
        failed_reasons=['必須要有 proxy host 設定']
    )

    mat_server = mock.MagicMock(spec=MatServer)

    manager = Manager(
        generate_default_config_use_case=generate_default_config_use_case,
        check_config_use_case=check_config_use_case,
        mat_server=mat_server,
    )

    assert manager.check_config() is False

    check_config_use_case.execute.assert_called_once()

    captured = capsys.readouterr()
    assert captured.out == '檢查設定檔 ...\n[x] 必須要有 proxy host 設定\n設定檔設定錯誤\n'


def test_check_success(capsys):
    generate_default_config_use_case = mock.MagicMock(spec=use_cases.GenerateDefaultConfigUseCase)

    check_config_use_case = mock.MagicMock(spec=use_cases.CheckConfigUseCase)
    check_config_use_case.execute.return_value = entities.ValidationReport()

    mat_server = mock.MagicMock(spec=MatServer)

    manager = Manager(
        generate_default_config_use_case=generate_default_config_use_case,
        check_config_use_case=check_config_use_case,
        mat_server=mat_server,
    )

    manager.check_config()

    check_config_use_case.execute.assert_called_once()

    captured = capsys.readouterr()
    assert captured.out == '檢查設定檔 ...\n設定檔檢查完成\n'


def test_serve_failed(capsys):
    generate_default_config_use_case = mock.MagicMock(spec=use_cases.GenerateDefaultConfigUseCase)

    check_config_use_case = mock.MagicMock(spec=use_cases.CheckConfigUseCase)
    check_config_use_case.execute.return_value = entities.ValidationReport(
        failed_reasons=['必須要有 proxy host 設定']
    )

    mat_server = mock.MagicMock(spec=MatServer)

    manager = Manager(
        generate_default_config_use_case=generate_default_config_use_case,
        check_config_use_case=check_config_use_case,
        mat_server=mat_server,
    )

    manager.serve('0.0.0.0', port=9527)

    check_config_use_case.execute.assert_called_once()

    captured = capsys.readouterr()
    assert captured.out == '檢查設定檔 ...\n[x] 必須要有 proxy host 設定\n設定檔設定錯誤\n'


def test_serve():
    generate_default_config_use_case = mock.MagicMock(spec=use_cases.GenerateDefaultConfigUseCase)

    check_config_use_case = mock.MagicMock(spec=use_cases.CheckConfigUseCase)
    check_config_use_case.execute.return_value = entities.ValidationReport()

    mat_server = mock.MagicMock(spec=MatServer)

    manager = Manager(
        generate_default_config_use_case=generate_default_config_use_case,
        check_config_use_case=check_config_use_case,
        mat_server=mat_server,
    )

    manager.serve('0.0.0.0', port=9527)

    check_config_use_case.execute.assert_called_once()

    mat_server.serve.assert_called_with(
        host='0.0.0.0',
        port=9527,
    )
