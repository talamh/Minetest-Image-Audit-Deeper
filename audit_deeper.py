import sys
import urllib.request
from json import loads, JSONDecodeError

from launchermeta import LauncherMeta


def main():
    # todo: we should check here to see if we have needed jars already
    # default_dir = '~./minecraft/versions'

    check_against = ['1.8.9']  # , '1.10.2', '1.12.2', '1.14.4', '1.16.1', '1.16.5', '1.17.1', '1.18.2']

    with urllib.request.urlopen(f'https://launchermeta.mojang.com/mc/game/version_manifest_v2.json') as url:
        try:
            data = loads(url.read().decode())
        except JSONDecodeError:
            print(f'could not retrieve launcher meta')
            sys.exit(1)

    meta = LauncherMeta(**data)
    meta.get_selected_urls(check_against)
    print(f'download size: {meta.size} bytes')

    meta.download()


if __name__ == "__main__":
    main()
