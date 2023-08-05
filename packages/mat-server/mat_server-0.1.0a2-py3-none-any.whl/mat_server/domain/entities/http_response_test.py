from mat_server.domain.entities import HTTPResponse


def test_create_http_response():
    http_response = HTTPResponse(
        raw_data=b'raw_data',
        status_code=200,
        headers={
            'name': 'name',
        }
    )

    assert http_response.raw_data == b'raw_data'
    assert http_response.status_code == 200
    assert http_response.headers == {
        'name': 'name',
    }
