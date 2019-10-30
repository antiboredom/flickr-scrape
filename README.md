# Scrape flickr

## Installation

1. Clone the repo

2. Create a virtualenvironment

```
virtualenv env
source env/bin/activate
```

3. Install requirements

`pip install -r requirements.txt`

## Usage

[Get an API key from Flickr](https://www.flickr.com/services/api/misc.api_keys.html) and make a file called `credentials.json` which has the following text in it (replace the credentials with your own):

```
{"KEY":"YOUR_API_KEY", "SECRET":"YOUR_API_SECRET"}
```

To scrape for a particular search term:

`python scraper.py --search "SEARCH TERM" --bbox "minimum_longitude minimum_latitude maximum_longitude maximum_latitude"`


To scrape for a particular group:

`python scraper.py --group "GROUP URL"`

Where GROUP URL is something like https://www.flickr.com/groups/scenery/pool/

You can also add a lat/lng coordinates to specify a geographic bounding box:

`python scraper.py --search "SEARCH TERM" --bbox "minimum_longitude minimum_latitude maximum_longitude maximum_latitude"`

Large-sized (1024px width) will be downloaded by default. You can download the original images by passing the flag `--original`.

Limit the number of pages of results downloaded by passing `--max-pages N` where `N` is pages of 500 results each.
