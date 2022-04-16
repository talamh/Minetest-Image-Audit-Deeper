import io
import json
import urllib.request
from json import loads, JSONDecodeError
from os.path import exists
from pathlib import Path
from zipfile import ZipFile

from PIL import Image

from launchermeta import LauncherMeta


def pre_process_jars():
    ver_dir = './versions'
    for path in Path(ver_dir).iterdir():
        if path.is_file():
            f = f'{ver_dir}/{path.name}'
            if f.endswith('.jar'):
                json_file = f'{f.removesuffix(".jar")}.json'
                if not exists(json_file):  # no associated json file so we preprocess the jar
                    print(f'preprocessing {f}')
                    size_group_names = []
                    size_group_images = []

                    with ZipFile(f'{f}') as jar_file:
                        filelist = jar_file.filelist

                        for img in filelist:
                            if len(img.filename.split('.')) == 3:  # mcmeta file
                                continue
                            ext = img.filename.split('.')[1]

                            if ext == 'tga' or ext == 'png' or ext == 'jpg':
                                texture = Image.open(io.BytesIO(jar_file.read(img.filename)))

                                image_dims = f'{texture.width}x{texture.height}'

                                if image_dims not in size_group_names:
                                    size_group_names.append(image_dims)
                                    size_group_images.append([])

                                size_group_images[size_group_names.index(image_dims)].append(img.filename)

                        img_dict = {}
                        for g in size_group_names:
                            img_dict[g] = size_group_images[size_group_names.index(g)]

                        json_object = json.dumps(img_dict, indent=4)
                        with open(json_file, "w") as outfile:
                            outfile.write(json_object)


def main():
    # todo: we should check here to see if we have needed jars already
    # default_dir = '~./minecraft/versions'

    check_against = ['1.8.9']  # , '1.10.2', '1.12.2', '1.14.4', '1.16.1']  # , '1.16.5', '1.17.1', '1.18.2']

    meta = None

    with urllib.request.urlopen('https://launchermeta.mojang.com/mc/game/version_manifest_v2.json') as url:
        try:
            data = loads(url.read().decode())
            meta = LauncherMeta(**data)
            meta.get_selected_urls(check_against)
            print(f'total download size: {meta.size} bytes')
            meta.download()
        except JSONDecodeError:
            print('could not retrieve launcher meta')

    # check what jars we have and do some indexing if needed
    pre_process_jars()


if __name__ == "__main__":
    main()
