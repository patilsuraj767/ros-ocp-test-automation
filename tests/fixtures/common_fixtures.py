import pytest
from api import sources
from lib import config

@pytest.fixture()
def source_uuid(request):
    source_name = config.DEFAULT_SOURCE_NAME

    # Delete source if already exist
    source_id = sources.get_source_id_by_name(source_name)
    if source_id:
        sources.delete_source(source_id)

    data = sources.create_source(source_name, request.param)
    yield data['sources'][0]['source_ref']
    sources.delete_source(data['sources'][0]['id'])