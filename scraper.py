import csv
import json
import os
import requests


SOURCE_URL = 'https://pokemondb.net/sprites'
SPRITES_DIRECTORY = 'sprites'
LINE_SPLITTER = '<span class="img-fixed icon-pkmn" data-src="'
LINE_START ='https://img.pokemondb.net/sprites/sword-shield/icon'
LINE_END = '" data-alt="'


def get_html(url):
  """ Returns the HTML of the url page """

  print('[get_html] fetching HTML from %s' % url)

  r = requests.get(url)
  html = r.text

  print('\tDone!\n')
  return html


def parse_html(html):
    """ Parses the input HTML into an array of sprite urls and pokemon ids"""

    lines = html.split(LINE_SPLITTER)

    print('[parse_html] parsing %d lines of HTML' % len(lines))

    data = []
    id = 1
    for line in lines:
        if LINE_START in line:
            sprite_url = line.split(LINE_END)[0]
            datum = {}
            datum['id'] = id
            datum['sprite_url'] = sprite_url
            datum['filename'] = sprite_url.split('/')[-1]
            data.append(datum)
            id += 1

    print('\tDone!\n')
    return data


def write_metadata(data):
    """ Writes json and csv files matching pokemon id to the sprite filename """

    print('[write_metadata] writing JSON and CSV metadata files')

    with open('metadata.json', 'w') as file:
        json.dump(data, file)

    with open('metadata.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=['id','sprite_url','filename'])                                               
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print('\tDone!\n')


def download_sprites(data):
    """ Downloads each sprite in the input array """

    if not os.path.exists(SPRITES_DIRECTORY):
        os.makedirs(SPRITES_DIRECTORY)

    print('[download_sprites] downloading %d sprite urls (please be patient...)' % len(data))
    
    for datum in data:
        save_path = '%s/%s' % (SPRITES_DIRECTORY, datum['filename'])
        r = requests.get(datum['sprite_url'])
        with open(save_path, 'wb') as outfile:
            outfile.write(r.content)

    print('\tDone!\n')


def main():
    html = get_html(SOURCE_URL)
    data = parse_html(html)
    write_metadata(data)
    download_sprites(data)


if __name__ == '__main__':
    main()
