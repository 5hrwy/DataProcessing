#!/usr/bin/env python
# Name: Sherwin Gomes
# Student number: 10004274
"""
This script scrapes IMDB and outputs a CSV file with highest rated tv series.
"""

import csv
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

TARGET_URL = "http://www.imdb.com/search/title?num_votes=5000,&sort=user_rating,desc&start=1&title_type=tv_series"
BACKUP_HTML = 'tvseries.html'
OUTPUT_CSV = 'tvseries.csv'


def extract_tvseries(dom):
    """
    Extract a list of highest rated TV series from DOM (of IMDB page).
    Each TV series entry should contain the following fields:
    - TV Title
    - Rating
    - Genres (comma separated if more than one)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    """

    # ADD YOUR CODE HERE TO EXTRACT THE ABOVE INFORMATION ABOUT THE
    # HIGHEST RATED TV-SERIES
    # NOTE: FOR THIS EXERCISE YOU ARE ALLOWED (BUT NOT REQUIRED) TO IGNORE
    # UNICODE CHARACTERS AND SIMPLY LEAVE THEM OUT OF THE OUTPUT.

    # get HTML content at target URL
    html = simple_get(TARGET_URL)

    # parse the HTML file into a DOM representation
    soup = BeautifulSoup(html, 'html.parser')

    # find all div's containing series details
    allseries = soup.find_all('div', class_='lister-item mode-advanced')

    # list to store series and details
    seriesout = []

    for series in allseries:

        # list to temporarily store details for each series
        seriesdetails = []

        # extract series title and append to list
        title = series.h3.a.get_text(strip=True)

        # check for missing data if so insert unknown
        if title == '':

            seriesdetails.append('unknown')

        else:
            seriesdetails.append(title)

        # extract series rating and append to list
        rating = float(series.strong.text)

        # check for missing data if so insert unknown
        if rating == '':

            seriesdetails.append('unknown')

        else:
            seriesdetails.append(rating)

        # extract series genre(s) and append to list
        genre = series.p.find('span', class_='genre').get_text(strip=True)

        # check for missing data if so insert unknown
        if genre == '':

            seriesdetails.append('unknown')

        else:
            seriesdetails.append(genre)

        # select series stars
        stars = series.select("p > a")

        # check for missing data if so insert unknown
        if stars == '':

            seriesdetails.append('unknown')

        else:
            # list to temporarily store star details for each series
            allstars = []

            # iterate over each star in cast of series and append to list
            for star in stars:
                cast = star.get_text(strip=True)
                allstars.append(cast)

            # convert list to string and append to list
            allstars = str(allstars)
            allstars = allstars.strip('[]')
            seriesdetails.append(allstars)

        # extract series runtime and append to list
        runtime = str(series.p.find('span', class_='runtime').get_text(strip=True))

        # check for missing data if so insert unknown
        if runtime == '':

            seriesdetails.append('unknown')

        else:
            runtime = runtime.strip('min ')
            seriesdetails.append(runtime)

        # store series details for each series in list
        seriesout.append(seriesdetails)

    # return list of all series and their details
    return [seriesout]


def save_csv(outfile, tvseries):
    """
    Output a CSV file containing highest rated TV-series.
    """
    writer = csv.writer(outfile)
    # ensure correct parsing in mac computers
    writer.writerow(['sep=,'])
    # insert header
    writer.writerow(['Title', 'Rating', 'Genre', 'Actors', 'Runtime'])

    # iterate over series and write row for each
    for series in tvseries:
        writer.writerows(series)


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('The following error occurred during HTTP GET request to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


if __name__ == "__main__":

    # get HTML content at target URL
    html = simple_get(TARGET_URL)

    # save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # parse the HTML file into a DOM representation
    dom = BeautifulSoup(html, 'html.parser')

    # extract the tv series (using the function you implemented)
    tvseries = extract_tvseries(dom)

    # write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file, tvseries)
