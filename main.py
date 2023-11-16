from dotenv import load_dotenv
load_dotenv()
import uuid
from lib import utils, config
from api import sources
from requests.auth import HTTPBasicAuth
import requests
import json

url = f"https://{config.DOMAIN}/api/cost-management/v1/recommendations/openshift?start_date=2023-04-01&cluster=my-test-source"
res = requests.get(url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD))
data = res.json()
with open('tests/dry_run_expected_res.json') as file:
    file_contents = file.read()
    expected_res = json.loads(file_contents)
    expected_res, res = json.dumps(expected_res), json.dumps(data, sort_keys=True)
    print(expected_res == res)
