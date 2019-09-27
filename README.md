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

`python scraper.py --search "SEARCH TERM" --bbox minimum_longitude,minimum_latitude,maximum_longitude,maximum_latitude`
