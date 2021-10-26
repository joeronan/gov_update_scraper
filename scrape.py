import requests
from datetime import datetime
import sys
import pytz
import pandas as pd
from xml.etree import ElementTree


# Government Data

def gov_data():
    return _gov_data(page_num=0, data_list=[])


def _gov_data(page_num: int, data_list: list):

    if page_num > 10:
        print('TOO MANY CALLS TO GOV DATA')
        return data_list

    r = requests.get(
        f'https://data.gov.uk/api/action/package_search?rows=100&start={(page_num*100) + 1}')
    r.json()

    terminate = False

    for entry in r.json()['result']['results']:

        entry_date = datetime.fromisoformat(
            entry['metadata_modified']).replace(microsecond=0)
        date_check = (entry_date >= start_date) and (entry_date <= end_date)

        if date_check:
            data_list.append({
                'source': 'Government Data',
                'url': f'https://data.gov.uk/dataset/{entry["id"]}/',
                'title': entry['title'],
                'description': entry['notes'],
                'datetime': entry_date.isoformat(),
            })
        else:
            terminate = True

    if terminate:
        return data_list
    else:
        return _gov_data(page_num=page_num+1, data_list=data_list)


# Government Statistical Research

def gov_stat_res():
    return _gov_stat_res(page_num=1, data_list=[])


def _gov_stat_res(page_num: int, data_list: list):

    if page_num > 10:
        print('TOO MANY CALLS TO GOV STATISTICAL RESEARCH')
        return data_list

    r = requests.get(
        f'https://www.gov.uk/search/research-and-statistics.atom?content_store_document_type=statistics_published&page={page_num}')
    root = ElementTree.fromstring(r.text)

    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):

        entry_date = datetime.fromisoformat(entry.find(
            '{http://www.w3.org/2005/Atom}updated').text[:-1])
        date_check = (entry_date >= start_date) and (entry_date <= end_date)

        if date_check:
            data_list.append({
                'source': 'Government Statistical Research',
                'url': entry.find('{http://www.w3.org/2005/Atom}link').attrib['href'],
                'title': entry.find('{http://www.w3.org/2005/Atom}title').text,
                'description': entry.find('{http://www.w3.org/2005/Atom}summary').text,
                'datetime': entry_date.isoformat(),
            })
        else:
            terminate = True

    if terminate:
        return data_list
    else:
        return _gov_stat_res(page_num=page_num+1, data_list=data_list)


# ONS

def ons():
    return _ons(page_num=1, data_list=[])


def _ons(page_num: int, data_list: list):

    if page_num > 10:
        print('TOO MANY CALLS TO ONS')
        return data_list

    r = requests.get(
        f'https://www.ons.gov.uk/releasecalendar?rss&page={page_num}')
    root = ElementTree.fromstring(r.text)
    for entry in root[0].findall('item'):

        entry_date = datetime.fromisoformat(
            entry.find('{http://purl.org/dc/elements/1.1/}date').text[:-1])
        date_check = (entry_date >= start_date) and (entry_date <= end_date)

        if date_check:
            data_list.append({
                'source': 'ONS',
                'url': entry.find('link').text,
                'title': entry.find('title').text,
                'description': '',
                'datetime': entry_date.isoformat(),
            })
        else:
            terminate = True

    if terminate:
        return data_list
    else:
        return _ons(page_num=page_num+1, data_list=data_list)


# London Data

def london_data():
    data_list = []
    r = requests.get(f'https://data.london.gov.uk/api/datasets/')
    for entry in r.json()['datasets']:
        entry_date = datetime.fromisoformat(
            entry['updatedAt'][:-1]).replace(microsecond=0)
        date_check = (entry_date >= start_date) and (entry_date <= end_date)

        if date_check:
            data_list.append({
                'source': 'London Data',
                'url': f'https://data.london.gov.uk/dataset/{entry["slug"]}',
                'title': entry['title'],
                'description': entry['description'],
                'datetime': entry_date.isoformat(),
            })
        else:
            break

    return data_list


start_date = datetime.fromisoformat(
    sys.argv[1]).astimezone(pytz.utc).replace(tzinfo=None)
end_date = datetime.fromisoformat(
    sys.argv[2]).astimezone(pytz.utc).replace(tzinfo=None)

output = []
output += gov_data()
output += gov_stat_res()
output += ons()
output += london_data()

df = pd.DataFrame(output)
df.to_csv(sys.argv[3])
df.to_csv('./output/most_recent.csv')
