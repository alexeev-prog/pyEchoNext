from pyechonext.response import Response


def test_response():
	response = Response(body='{"test": true, "testlib": "pytest"}', content_type='application/json')

	assert response.status_code == '200 OK'
	assert response.content_type == "application/json"
	assert response.charset == "UTF-8"

	response_json = response.json

	assert response_json == {"test": True, "testlib": "pytest"}
