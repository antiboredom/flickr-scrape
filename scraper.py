from __future__ import print_function
import time
import sys
import json
import re
import os
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

with open('credentials.json') as infile:
    creds = json.load(infile)

KEY = creds['KEY']
SECRET = creds['SECRET']

def download_file(url, local_filename):
    if local_filename is None:
        local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename


def get_photos(q, page=1, bbox=None):
    params = {
        'content_type': '7',
        'per_page': '500',
        'media': 'photos',
        'method': 'flickr.photos.search',
        'format': 'json',
        'advanced': 1,
        'nojsoncallback': 1,
        'extras': 'media,realname,url_l,o_dims,geo,tags,machine_tags,date_taken',#url_c,url_l,url_m,url_n,url_q,url_s,url_sq,url_t,url_z',
        'page': page,
        'text': q,
        'api_key': KEY,
    }

    # bbox should be: minimum_longitude, minimum_latitude, maximum_longitude, maximum_latitude
    if bbox is not None and len(bbox) == 4:
        params['bbox'] = ','.join(bbox)

    results = requests.get('https://api.flickr.com/services/rest', params=params).json()['photos']
    return results


def search(q, bbox=None):
    # create a folder for the query if it does not exist
    foldername = os.path.join('images', re.sub(r'[\W]', '_', q))
    if bbox is not None:
        foldername += '_'.join(bbox)

    if not os.path.exists(foldername):
        os.makedirs(foldername)

    jsonfilename = os.path.join(foldername, 'results.json')

    if not os.path.exists(jsonfilename):

        # save results as a json file
        photos = []
        current_page = 1

        results = get_photos(q, page=current_page, bbox=bbox)

        total_pages = results['pages']
        photos += results['photo']

        while current_page < total_pages:
            print('downloading metadata, page {} of {}'.format(current_page, total_pages))
            current_page += 1
            photos += get_photos(q, page=current_page, bbox=bbox)['photo']
            time.sleep(0.5)

        with open(jsonfilename, 'w') as outfile:
            json.dump(photos, outfile)

    else:
        with open(jsonfilename, 'r') as infile:
            photos = json.load(infile)

    # download images
    print('Downloading images')
    for photo in tqdm(photos):
        try:
            url = photo.get('url_l')
            extension = url.split('.')[-1]
            localname = os.path.join(foldername, '{}.{}'.format(photo['id'], extension))
            if not os.path.exists(localname):
                download_file(url, localname)
        except:
            continue


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Download images from flickr')
    parser.add_argument('--search', '-s', dest='q', required=True, help='Search term')
    parser.add_argument('--bbox', '-b', dest='bbox', required=False, help='Bounding box to search in, separated by commas like so: minimum_longitude,minimum_latitude,maximum_longitude,maximum_latitude')
    args = parser.parse_args()

    q = args.q

    try:
        bbox = args.bbox.split(',')
    except:
        bbox = None

    if bbox and len(bbox) != 4:
        bbox = None

    print('Searching for {}'.format(q))
    if bbox:
        print('Within', bbox)

    search(q, bbox)
