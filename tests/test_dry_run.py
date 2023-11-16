from dotenv import load_dotenv
load_dotenv()
import pytest
import requests
import tempfile
import uuid
from lib import utils, config
from tests.fixtures.common_fixtures import source_uuid
from requests.auth import HTTPBasicAuth
import json
import time


@pytest.mark.parametrize('source_uuid', [str(uuid.uuid4())], indirect=True)
def test_dry_run(source_uuid):
    with tempfile.TemporaryDirectory() as tmp_dir:
        data = utils.create_archive_with_uuid("samples/test.tar.gz" , source_uuid, tmp_dir)
        time.sleep(10)
        utils.upload_to_ingress(data)
        time.sleep(10)
        # get recommendation
        url = f"https://{config.DOMAIN}/api/cost-management/v1/recommendations/openshift?start_date=2023-04-01&cluster={config.DEFAULT_SOURCE_NAME}"
        res = requests.get(url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD))
        assert res.status_code == 200
        
        res = res.json()
        if res["data"]:
            with open('tests/dry_run_expected_res.json') as file:
                file_contents = file.read()
                expected_res = json.loads(file_contents)
                expected_res, res = json.dumps(expected_res['data'][0]['recommendations'], sort_keys=True), json.dumps(res['data'][0]['recommendations'], sort_keys=True)
                assert expected_res == res
        else:
            pytest.fail(f"Empty response from /api/cost-management/v1/recommendations/openshift: {res})")
