import os
from time import strftime, localtime
import urllib
import json
# import omdb
from arm.config.config import cfg


def get_info(directory):
    file_list = []
    for i in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, i)):
            a = os.stat(os.path.join(directory, i))
            fsize = os.path.getsize(os.path.join(directory, i))
            fsize = round((fsize / 1024), 1)
            fsize = "{0:,.1f}".format(fsize)
            create_time = strftime('%Y-%m-%d %H:%M:%S', localtime(a.st_ctime))
            access_time = strftime('%Y-%m-%d %H:%M:%S', localtime(a.st_atime))
            file_list.append([i, access_time, create_time, fsize])  # [file,most_recent_access,created]
    return file_list


def getsize(path):
    st = os.statvfs(path)
    free = (st.f_bavail * st.f_frsize)
    freegb = free/1073741824
    return freegb


def convert_log(logfile):
    logpath = cfg['LOGPATH']
    fullpath = os.path.join(logpath, logfile)

    output_log = os.path.join('static/tmp/', logfile)

    with open(fullpath) as infile, open(output_log, 'w') as outfile:
        txt = infile.read()
        txt = txt.replace('\n', '\r\n')
        outfile.write(txt)
    return(output_log)


def call_omdb_api(title=None, year=None, imdbID=None, plot="short"):
    """ Queries OMDbapi.org for title information and parses if it's a movie
        or a tv series """
    omdb_api_key = cfg['OMDB_API_KEY']

    if imdbID:
        strurl = "http://www.omdbapi.com/?i={1}&plot={2}&r=json&apikey={0}".format(omdb_api_key, imdbID, plot)
    elif title:
        # try:
        title = urllib.parse.quote(title)
        strurl = "http://www.omdbapi.com/?s={1}&plot={2}&r=json&apikey={0}".format(omdb_api_key, title, plot)
    else:
        print("no params")
        return(None)

    # strurl = urllib.parse.quote(strurl)
    print(strurl)
    title_info_json = urllib.request.urlopen(strurl).read()
    title_info = json.loads(title_info_json.decode())
    # d = {'year': '1977'}
    # dvd_info = omdb.get(title=title, year=year)
    print("call was successful")
    return(title_info)
    # except Exception:
    #     print("call failed")
    #     return(None)
