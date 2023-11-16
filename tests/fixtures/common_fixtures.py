import pytest
from api import sources

@pytest.fixture()
def source_uuid(request):
    data = sources.create_source(request.param)
    yield data['sources'][0]['source_ref']
    sources.delete_source(data['sources'][0]['id'])