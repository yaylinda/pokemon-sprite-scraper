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
  return r.text


def parse_html(html):
    """ Parses the input HTML into an array of sprite urls"""

    lines = html.split(LINE_SPLITTER)

    print('[parse_html] parsing %d lines of HTML' % len(lines))

    data = []
    for line in lines:
        if LINE_START in line:
            sprite_url = line.split(LINE_END)[0]
            data.append(sprite_url)

    print('[parse_html] parsed %d pokemon sprite urls' % len(data))
    return data

def download_sprites(sprites):
    """ Downloads each sprite in the input array """

    if not os.path.exists(SPRITES_DIRECTORY):
        os.makedirs(SPRITES_DIRECTORY)

    print('[download_sprites] downloading %d sprite urls' % len(sprites))
    
    for sprite_url in sprites:
        name = sprite_url.split('/')[-1].split('.png')[0]
        save_path = '%s/%s.png' % (SPRITES_DIRECTORY, name)
        r = requests.get(sprite_url)
        with open(save_path, 'wb') as outfile:
            outfile.write(r.content)

    print('[download_sprites] downloaded %d sprite urls' % len(sprites))

def main():
    html = get_html(SOURCE_URL)
    sprites = parse_html(html)
    download_sprites(sprites)

    print('\nDone!')

if __name__ == '__main__':
    main()
