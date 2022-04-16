import urllib.request
from io import BytesIO
from json import loads, JSONDecodeError
from os.path import exists, getsize

import requests


class MCVersionV1:
    def __init__(self, assetIndex: dict, assets: str, complianceLevel: int, downloads: dict, id: str, javaVersion:
    dict, libraries: dict, logging: dict, mainClass: str, minecraftArguments: str, minimumLauncherVersion: int,
                 releaseTime: str, time: str, type: str):
        self.url = downloads['client']['url']
        self.size = downloads['client']['size']
        self.id = id


class MCVersionV2:
    def __init__(self, assetIndex: dict, assets: str, complianceLevel: int, downloads: dict, id: str, javaVersion:
    dict, libraries: dict, logging: dict, mainClass: str, arguments: str, minimumLauncherVersion: int,
                 releaseTime: str, time: str, type: str):
        self.url = downloads['client']['url']
        self.size = downloads['client']['size']
        self.id = id


class LauncherMeta:
    def __init__(self, latest: dict, versions: list):
        self.latest = latest
        self.version_urls = {}
        self.selected_versions = {}
        self.size = 0

        for v in versions:
            self.version_urls[v['id']] = v['url']
            # uncomment this to dump a list of all available jars to console
            # print(f'{v["id"]}')

    def download(self):
        for v in self.selected_versions:
            if not exists(f'./versions/{v}.jar') or getsize(f'./versions/{v}.jar') != self.selected_versions[v].size:
                print(f'downloading version {v} = {self.selected_versions[v].size} bytes from:'
                      f'\n{self.selected_versions[v].url}')
                request = requests.get(self.selected_versions[v].url, stream=True)

                if request.status_code == 200:
                    request.raw.decode_content = True
                    data = BytesIO(request.content)
                    with open(f'./versions/{v}.jar', 'wb') as file:
                        file.write(data.read())
                else:
                    print(f'could not download version {v}')
            else:
                print(f'Version {v} already exists in the versions directory')

    def get_selected_urls(self, version_list: list) -> None:
        for v in version_list:

            with urllib.request.urlopen(self.version_urls[v]) as url:
                try:
                    data = loads(url.read().decode())
                    try:
                        self.selected_versions[v] = MCVersionV1(**data)
                        self.size += self.selected_versions[v].size
                    except TypeError:  # minecraftArguments was changed to arguments at some point
                        self.selected_versions[v] = MCVersionV2(**data)
                        self.size += self.selected_versions[v].size

                except JSONDecodeError:
                    print(f'could not retrieve json file for version {v}')
