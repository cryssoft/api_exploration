#!/usr/bin/python3


from dotenv import load_dotenv 
from googleapiclient.discovery import build
from os     import getenv
from re     import match 
from sys    import argv as g_argv
from time   import sleep


def get_youtube_video_channel(p_videoId: str, p_apiKey: str) -> str:
    """
    Use Google's documented API to get video metadata for each video we've
    watched on youtube (with various incoming URL formats) and return the
    channel ID so we can track unique channels we've watched.

    0.0.1 - cribbed from a YouTube video (fitting!)
    0.0.2 - reduced to just what we need from the API and for the return
    """
    l_returns: str = ''

    try:
        l_api = build('youtube', 'v3', developerKey=p_apiKey)
        l_request = l_api.videos().list(part='snippet', id=p_videoId)
        l_response = l_request.execute()
        l_videoData = l_response['items'][0]
        l_returns = l_videoData['snippet']['channelTitle']

    #  Very bad form, but exploring the relevant exceptions can wait
    except Exception as l_exception:
        pass

    sleep(1)    #  Put in some sleep here since we don't want to anger the API gods

    return(l_returns)


def main(p_argv: list[str]) -> None:
    """
    Simple, double loop.  Loop 1 reads the CSV-ish file from our "comments" column
    in the to-do list spreadsheet.  Loop 2 writes out just the host names (for non-
    youtube content) or host names and youtube channel names.  We can always de-
    duplicate the list once it's back in Excel.

    0.0.1 - based on regex matching, had a lot of issues
    0.0.2 - based on split()s, much more reliable
    0.0.3 - worked around the UTF-8 problem in the data (darn Excel!)
    0.0.4 - found data quality issues with trailing whitespace (darn Excel!)
    0.0.5 - moved the Google API key into a .env file so this code is safe to up-load
    """
    l_dictUrl: dict[str,dict] = {}

    load_dotenv()
    l_apiKey = getenv('GOOGLE_API_KEY')

    #  No idea how a non-Unicode character got into this column, but it is what it is
    with open(p_argv[1], 'r', encoding='utf-8', errors='ignore') as l_file:
        try:
            for l_data in l_file:
                #  Some oddities with this dataset - lots of trailing whitespace
                l_data = l_data.strip()

                if (match(r'^https:\/\/.+', l_data) is not None):
                    l_split: list[str] = l_data.split('/')
                    l_dictUrl[l_data] = {}
                    l_dictUrl[l_data]['host'] = l_split[2]

                    #  Capture the video ID from several different URL formats (yuck!)
                    if (match(r'.*youtu.+', l_split[2])):
                        if (l_split[3] in ['live', 'shorts']):
                            l_dictUrl[l_data]['video_id'] = l_split[4].split('?')[0]
                        elif (match(r'^watch\?.+', l_split[3])):
                            l_dictUrl[l_data]['video_id'] = l_split[3].split('?')[1].split('=')[1].split('&')[0]
                        else:
                            l_dictUrl[l_data]['video_id'] = l_split[3].split('?')[0]

        #  Redundantly ignore things that don't decode properly into Unicode  :-(
        except UnicodeDecodeError as l_ude:
            pass

    for l_url in l_dictUrl:
        if ((match(r'.*youtu.+', l_url)) and ('video_id' in l_dictUrl[l_url])):
            l_channel = get_youtube_video_channel(l_dictUrl[l_url]['video_id'], l_apiKey)
            print(f'"www.youtube.com","{l_channel}"')
        else:
            print(f'"{l_dictUrl[l_url]['host']}",""')

    return


#  Keep ourselves out of trouble if someone tries to import this module/file.
if (__name__ == '__main__'):
    main(g_argv)