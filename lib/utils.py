import tarfile
import json
import requests
from requests.auth import HTTPBasicAuth
from lib import config

def change_cluster_uuid(data, uuid):
    data["cluster_id"] = uuid
    data["cr_status"]["clusterID"] = uuid
    return data


def create_archive_with_uuid(tar_file, uuid, tmp_dir):
    with tarfile.open(tar_file,'r:gz') as sample_tar:
        with tarfile.open(name=f"{tmp_dir}/tmp.tar.gz", mode='w:gz') as new_tar:
            for member in sample_tar.getmembers():
                if member.name == "manifest.json":
                    manifest = sample_tar.extractfile(member).read().decode('utf-8')
                    data = json.loads(manifest)
                    data = change_cluster_uuid(data, uuid)
                    with open(f"{tmp_dir}/manifest.json", "w") as manifest_file:
                        json.dump(data, manifest_file)
                    new_tar.add(manifest_file.name)

                new_tar.addfile(member, sample_tar.extractfile(member.name))
    return new_tar.name

def upload_to_ingress(tar_file):
    url = f'https://{config.DOMAIN}/api/ingress/v1/upload'
    files = {'file': ('cost-mgmt.tar.gz', open(tar_file, 'rb'), 'application/vnd.redhat.hccm.tar+tgz')}
    headers = {'Content-Transfer-Encoding': 'application/gzip'}
    r = requests.post(url, files=files, headers=headers, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD))
    print(r.text)
