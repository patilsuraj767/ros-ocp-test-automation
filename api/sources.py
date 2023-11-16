import uuid
import requests
from lib import config
from requests.auth import HTTPBasicAuth


def get_cost_application_type_id():
    url = f"https://{config.DOMAIN}/api/sources/v3.1/application_types?filter[name][eq]=/insights/platform/cost-management"
    res = requests.get(url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD))
    data = res.json()['data']
    return data[0]['id']

def get_source_id_by_name(source_name):
    url = f"https://{config.DOMAIN}/api/sources/v3.1/sources?filter[name][eq]={source_name}"
    res = requests.get(url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD))
    data = res.json()['data']
    if data:
        return data[0]['id']
    else:
        return 0

def create_source(source_name, cluster_uuid):

    source_payload = {
        "sources":[
            {
                "name":source_name,
                "source_ref":cluster_uuid,
                "source_type_name":"openshift"
            }
        ],
        "endpoints":[],
        "authentications":[
            {
                "authtype":"token",
                "resource_type":"application",
                "resource_name":"/insights/platform/cost-management"
            }
        ],
        "applications":[
            {
                "application_type_id":get_cost_application_type_id(),
                "extra":{
                    "hcs":False
                },
                "source_name":source_name
            }
        ]
    }

    url_post = f"https://{config.DOMAIN}/api/sources/v3.1/bulk_create"
    post_response = requests.post(url_post, json=source_payload, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD))


    return post_response.json()


def delete_source(uuid):
    url = f"https://{config.DOMAIN}/api/sources/v3.1/sources/{uuid}"
    requests.delete(url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD))
