# Government Data Scraper

## Description

This is a scraper which goes through 4 major government data providers and creates a text file with a short summary of their recent uploads. **Note** this has been scrappily made and only tested on macOS so may not work on your machine.

## How to use

Open a command window and run the shell script `run.sh`. When prompted, type either `d` or `l` to get either the last day's updates or all updates since you last called the script. The first time you run this you should only use `d`.

## Requirements

Python:
- `pandas`
- `xml.etree.ElementTree`

Command Line:
- `gdate`

## SOURCES:
- [ONS Releases](https://www.ons.gov.uk/releasecalendar)
- [Gov Research & Statistics](https://www.gov.uk/search/research-and-statistics?content_store_document_type=statistics_published&order=updated-newest)
- [Gov Data](https://data.gov.uk/)
- [London Data](https://data.london.gov.uk/)

