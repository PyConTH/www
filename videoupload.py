#!/usr/bin/python
import html
import io

import http.client as httplib
import urllib
from collections import OrderedDict
from datetime import datetime, tzinfo, timezone, timedelta

import httplib2
import os
import random
import sys
import time

import pytz
import requests

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from docutils import core
from docutils.writers._html_base import HTMLTranslator
from docutils.writers.html5_polyglot import Writer
from fuzzywuzzy import fuzz
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import yaml
import ruamel.yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Talk data indexed by (day,time,track)
talks = {}

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
                        httplib.IncompleteRead, httplib.ImproperConnectionState,
                        httplib.CannotSendRequest, httplib.CannotSendHeader,
                        httplib.ResponseNotReady, httplib.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google Developers Console at
# https://console.developers.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = ["https://www.googleapis.com/auth/youtube.upload",
                        "https://www.googleapis.com/auth/youtube.force-ssl"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the Developers Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


# If modifying these scopes, delete the file token.pickle.
DRIVE_SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
                'https://www.googleapis.com/auth/drive.readonly']


def get_authenticated_service(args):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   scope=YOUTUBE_UPLOAD_SCOPE+DRIVE_SCOPES,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    youtube= build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                 http=credentials.authorize(httplib2.Http()))
    drive =  build('drive', 'v3', http=credentials.authorize(httplib2.Http()))
    return drive,youtube


#
# def get_drive_service():
#     """Shows basic usage of the Drive v3 API.
#     Prints the names and ids of the first 10 files the user has access to.
#     """
#     creds = None
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'client_secrets.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)
#
#     service = build('drive', 'v3', credentials=creds)
#     return service

class HTMLFragmentTranslator( HTMLTranslator ):
    def __init__( self, document ):
        HTMLTranslator.__init__( self, document )
        self.head_prefix = ['','','','','']
        self.body_prefix = []
        self.body_suffix = []
        self.stylesheet = []
    def astext(self):
        return ''.join(self.body)

html_fragment_writer = Writer()
html_fragment_writer.translator_class = HTMLFragmentTranslator

def reST_to_html( s ):
    return core.publish_string( s, writer = html_fragment_writer )

import sys
import textwrap
import types

import docutils.nodes
import docutils.parsers.rst
import docutils.utils
import sphinx.writers.text
import sphinx.builders.text
import sphinx.util.osutil


def parse_rst(text: str) -> docutils.nodes.document:
    parser = docutils.parsers.rst.Parser()
    components = (docutils.parsers.rst.Parser,)
    settings = docutils.frontend.OptionParser(
        components=components
    ).get_default_values()
    document = docutils.utils.new_document("<rst-doc>", settings=settings)
    parser.parse(text, document)
    return document


def reST_to_text( source ):
    # TODO: Doesnt turn links into text with the url shown

    document = parse_rst(source)

    app = types.SimpleNamespace(
        srcdir=None,
        confdir=None,
        outdir=None,
        events=None,
        doctreedir="/",
        config=types.SimpleNamespace(
            text_newlines="native",
            text_sectionchars="=",
            text_add_secnumbers=False,
            text_secnumber_suffix=".",
        ),
        tags=set(),
        registry=types.SimpleNamespace(
            create_translator=lambda self, something, new_builder: sphinx.writers.text.TextTranslator(
                document, new_builder
            )
        ),
    )

    builder = sphinx.builders.text.TextBuilder(app)

    translator = sphinx.writers.text.TextTranslator(document, builder)

    document.walkabout(translator)

    return translator.body


def update_youtube(youtube, videos):
    for video in videos:
        name, *_ = video['speaker'].split(',')
        name = ' '.join([p.capitalize() for p in name.split()])
        title = "{} - {}".format(video['title'], name)
        if len(title) > 100:
            title = "{}... - {}".format(video['title'][:100-(len(name)+3+3)], name)

        hour,min = video['time'].split(':')
        date=datetime(2019,6, 15 if video['day'] == 'sat' else 16, int(hour), int(min),
                      tzinfo=timezone(timedelta(hours=7)))
        url =  "https://th.pycon.org/talks/#{day}_{track}_{time}".format(**video)
        description = """Talk by {} - {} @ PyCon Thailand 2019 ({})

{}


Speaker Bio - {}:

{}""".format(video['speaker'],
           date.strftime("%a %d %b"),
           url,
           reST_to_text(video['description'] or '').strip('\n'),
           video['speaker'],
           reST_to_text(video['bio'] or '').strip('\n'))
        description = description
        tags = list(set(video['snippet']['tags'] + [name,  'pyconth2019', 'python language', 'pycon thailand']))

        body = dict(
            id=video['youtubeid'],
            snippet=dict(
                title=title,
                description=description,
                tags=tags,
                categoryId='28'
            ),
            recordingDetails= {
                "location": {
                    "latitude": "13.6851249",
                    "longitude": "100.6088319"
                },
                "recordingDate": date.astimezone(pytz.utc).isoformat().replace('+00:00','.000Z')
            }
        )

        def same(x,y):
            # Stupid tags come back in random order
            if type(x) == list:
                return set(x) == set(y)
            else:
                return x == y

        if all([same(body['snippet'][key],video['snippet'][key]) for key in body['snippet']]):
            # nothing needs updating
            continue

        print(video['snippet'])
        print(body)

        request = youtube.videos().update(
            part=",".join(body.keys()),
            body=body)
        response = request.execute()
        if video['youtubeid'] != response.get('id', None):
           raise Exception(response)



def initialize_upload(youtube, file, mimetype, title, description, keywords=None, category=22, privacyStatus='private'):
    tags = None
    if keywords:
        tags = keywords.split(",")

    body = dict(
        snippet=dict(
            title=title,
            description=description,
            tags=tags,
            categoryId=category
        ),
        status=dict(
            privacyStatus=privacyStatus
        )
    )

    fh = io.BytesIO()
    writer = io.BufferedWriter(fh)

    # try:
    #     os.mkfifo('my_fifo')
    # except FileExistsError:
    #     pass
    # fh = open('my_fifo', 'w', os.O_WRONLY|os.O_NONBLOCK)
    downloader = MediaIoBaseDownload(writer, file, chunksize=1024 * 1024)
    #o = os.open('my_fifo', os.O_RDONLY | os.O_NONBLOCK)
    reader = io.BufferedReader(fh)

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        # The chunksize parameter specifies the size of each chunk of data, in
        # bytes, that will be uploaded at a time. Set a higher value for
        # reliable connections as fewer chunks lead to faster uploads. Set a lower
        # value for better recovery on less reliable connections.
        #
        # Setting "chunksize" equal to -1 in the code below means that the entire
        # file will be uploaded in a single HTTP request. (If the upload fails,
        # it will still be retried where it left off.) This is usually a best
        # practice, but if you're using Python older than 2.6 or if you're
        # running on App Engine, you should set the chunksize to something like
        # 1024 * 1024 (1 megabyte).

        media_body=MediaIoBaseUpload(reader, chunksize=1024 * 1024 , resumable=True, mimetype=mimetype)
    )
	
    if "id" in insert_request:
        print("Video id", insert_request["id"])
    else:
        print("id not in insert_request")

    resumable_upload(insert_request, downloader, writer)


# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(insert_request, downloader, buffer):
    dl_done=False
    while not dl_done:
        # Get rid of extra data we already uploader

        print("downloading chunk...")
        dl_status, dl_done = downloader.next_chunk()
        buffer.flush()

        response = None
        error = None
        retry = 0
        while response is None:

            try:

                print("Uploading chunk...")
                status, response = insert_request.next_chunk()
                if response is False:
                    break
                if 'id' in response:
                    print("Video id '%s' was successfully uploaded." % response['id'])
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
            except HttpError as e:
                raise
                if e.resp.status in RETRIABLE_STATUS_CODES:
                    error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                         e.content)
                else:
                    raise
            except RETRIABLE_EXCEPTIONS as e:
                error = "A retriable error occurred: %s" % e
                raise

            if error is not None:
                print(error)
                retry += 1
                if retry > MAX_RETRIES:
                    exit("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print("Sleeping %f seconds and then retrying..." % sleep_seconds)
                time.sleep(sleep_seconds)




def get_videos(service, drive_url):
    folder_id = drive_url.split('/')[-1] # TODO: fix
    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)",
        q="'{}' in parents".format(folder_id)).execute()
    for day in results.get('files', []):
        videos = service.files().list(
            fields="nextPageToken, files(id, name, exportLinks, mimeType)",
            q="'{}' in parents".format(day['id'])).execute()
        for video in videos.get('files',[]):
            request = service.files().get_media(fileId=video['id'])
            video['download'] = request
            yield video


def get_talks(file):
    talks = {}
    with open(file, encoding="utf8") as f:
        data = ruamel.yaml.load(f, ruamel.yaml.RoundTripLoader)
        for t in data['talks']:
            if t.get('speaker') and t.get('track'):
                yield t

def update_talks(file, videos):
    conf = open(file, encoding="utf8")
    data = ruamel.yaml.load(conf, ruamel.yaml.RoundTripLoader)
    conf.close()
    def merge(l,r):
        r['youtube_url'] = "https://www.youtube.com/watch?v=" + l['youtubeid']
        return r

    join(videos, data['talks'], key_yaml, key_yaml, merge)
    with open(file, 'w') as conf:
        ruamel.yaml.dump(data, conf, ruamel.yaml.RoundTripDumper)


def key_drive(video):
    name = video['name']
    if "." in name:
        name, ext = name.split('.')
    day, track, *speaker = name.split('_')
    day = dict(Day1="sat", Day2="sun").get(day)
    if track == 'Track':
        track = speaker.pop(0)
    else:
        track = track[-1]
    try:
        track = int(track[-1])
    except ValueError:
        track = 0
    speaker = ' '.join([speaker[0]]+ [s[0] for s in speaker[1:]]).lower()
    return (day, track, speaker)

def key_yaml(t):
    if t.get('speaker',''):
        speaker = t.get('speaker','').replace('-', ' ')
        speaker, *_ = speaker.split('(')
        speaker = speaker.split()
        speaker = ' '.join([speaker[0]]+[s[0] for s in speaker[1:]]).lower()
    else:
        speaker = ''
    return (t.get('day'), t.get('track'), speaker)




def get_channel(youtube, channelid):
    channel = []

    list_request = youtube.search().list(channelId=channelid,
                                         part='snippet',
                                         maxResults=50,
                                         order="date",
                                         type="youtube#video",
                                         publishedAfter="2019-01-01T00:00:00.000Z",
                                         )

    while list_request:
        list_response = list_request.execute()

        # Print information about each video.
        for item in list_response['items']:
            title = item['snippet']['title']
            video_id = item['id'].get('videoId')
            if not video_id:
                continue
            #print('%s (%s)' % (title, video_id))
            video = dict(id=video_id,
                                  #filename=get_filename(youtube, video_id),
                                 **item['snippet'])
            video['title'] = html.unescape(video['title'])
            #video['description'] = html.unescape(video['description'])
            #video['snippet'] = item['snippet']
            channel.append(video)
            #channel.append((item['snippet']))

        list_request = youtube.channels().list_next(list_request, list_response)


    # get more details
    details = youtube.videos().list(id=','.join([v['id'] for v in channel]),
                                    part="fileDetails,snippet",

                                    # onBehalfOfContentOwner="pycon-thailand-0631@pages.plusgoogle.com"
                                    ).execute()
    for detail, video in zip(details['items'], channel):
        assert video['id']==detail['id']
        video['filename'] = detail['fileDetails']['fileName']
        video['snippet'] = detail['snippet']
        video['title'] = detail['snippet']['title']

    return channel


def join(left, right, key_left, key_right, merge):
    " return merged, unmatched_left and unmatched_right"
    merged = []
    unmerged_right = []
    map = OrderedDict()
    for item in left:
        key = key_left(item)
        map[key] = item
    for item in right:
        if not map:
            break
        key = key_right(item)
        if key in map:
            merged.append(merge(map[key], item))
            del map[key]
        else:
            ratios = [(fuzz.token_set_ratio(key, lkey),v, lkey) for lkey,v in map.items()]
            ratio, best, lkey = sorted(ratios, key=lambda i:i[0])[-1]
            if ratio>90:
                merged.append(merge(best, item))
                del map[lkey]
            else:
                unmerged_right.append(item)

    return merged, list(map.values()), unmerged_right

def do_upload(youtube, videos):
    for video in videos:
        request = video['download']

        # TODO: find youtube video and see if it was uploaded after its last modified date and reupload if so
        # TODO: get title and keywords right. link back to main site. need permaurl for site.
        title = video['title']
        description = video['description']
        keywords = "pyconth,python"

        try:
            initialize_upload(youtube, file=request, mimetype=video['mimeType'],
                              title=title, description=description, category="22",
                              keywords=keywords)
        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
            break


if __name__ == '__main__':
    argparser.add_argument("--driveurl", required=False, help="share url for the videos")
    argparser.add_argument("--talks", required=True, help="Talks.yaml file")
    argparser.add_argument("--channelid", default="UCtHekbmBXtp5AYSVARFQQiw")
    argparser.add_argument("--no_upload", default=False, action='store_true')
    # argparser.add_argument("--category", default="22",
    #                        help="Numeric video category. " +
    #                             "See https://developers.google.com/youtube/v3/docs/videoCategories/list")
    # argparser.add_argument("--keywords", help="Video keywords, comma separated",
    #                        default="")
    args = argparser.parse_args()
    #
    # if not os.path.exists(args.file):
    #     exit("Please specify a valid file using the --file= parameter.")


    # Find talk videos
    #drive = get_drive_service()
    drive,youtube = get_authenticated_service(args)

    # Match to schedule data
    talks = list(get_talks(args.talks))

    channel = get_channel(youtube, args.channelid)
    #channel = dict([('Do you know what Pycon Thailand is all about?', {'id': 'UExY3mb-CkA', 'filename': 'pycon2018.mp4', 'title': 'Do you know what Pycon Thailand is all about?', 'publishedAt': '2019-05-15T07:46:52.000Z', 'channelId': 'UCtHekbmBXtp5AYSVARFQQiw', 'description': "Wonder what Pycon is all about? Here's a video on what happened last year. With more attendees, more booths, and more keynote speakers this year, we're ...", 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/UExY3mb-CkA/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/UExY3mb-CkA/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/UExY3mb-CkA/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'PyCon Thailand', 'liveBroadcastContent': 'none'}), ('Introduction to serverless Python with AWS Lambda', {'id': 'NPsp_MwhUiI', 'filename': 'unknown', 'title': 'Introduction to serverless Python with AWS Lambda', 'publishedAt': '2018-08-09T04:08:48.000Z', 'channelId': 'UCtHekbmBXtp5AYSVARFQQiw', 'description': 'PyCon Thailand: https://2018.th.pycon.org/ Introduction to serverless Python with AWS Lambda Speaker: Murat Knecht https://twitter.com/muratknecht ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/NPsp_MwhUiI/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/NPsp_MwhUiI/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/NPsp_MwhUiI/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'PyCon Thailand', 'liveBroadcastContent': 'none'}), ('Graph-Theoretic Computation in Python', {'id': '1-aSxYDiyZM', 'filename': 'unknown', 'title': 'Graph-Theoretic Computation in Python', 'publishedAt': '2018-08-08T12:54:45.000Z', 'channelId': 'UCtHekbmBXtp5AYSVARFQQiw', 'description': 'PyCon Thailand: https://2018.th.pycon.org/ Graph-Theoretic Computation in Python Speaker: Poomjai Nacaskul, PhD, DIC, CFA ------------ Description: Playing ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/1-aSxYDiyZM/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/1-aSxYDiyZM/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/1-aSxYDiyZM/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'PyCon Thailand', 'liveBroadcastContent': 'none'}), ('Python for Self-Trackers: How to Visualize and Better Understand Your Life in Data', {'id': 'wHuHC1VflZ8', 'filename': 'unknown', 'title': 'Python for Self-Trackers: How to Visualize and Better Understand Your Life in Data', 'publishedAt': '2018-08-08T12:02:27.000Z', 'channelId': 'UCtHekbmBXtp5AYSVARFQQiw', 'description': 'PyCon Thailand: https://2018.th.pycon.org/ Python for Self-Trackers: How to Visualize and Better Understand Your Life in Data Speaker: Mark Koester ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/wHuHC1VflZ8/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/wHuHC1VflZ8/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/wHuHC1VflZ8/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'PyCon Thailand', 'liveBroadcastContent': 'none'})])

    merged, no_matched, no_video = join(channel, talks,
                                         lambda i: i['title'].lower().replace('_',' '),
                                         lambda i: ' - '.join([i['title'],i['speaker']]).lower(),
                                         lambda l,r: dict(youtubeid=l['id'], snippet=l['snippet'], youtubetitle=l['title'], **r))
    print("Youtube videos - unmatched")
    for item in no_matched:
        print(" - ", item['title'])
    print("Talks with no video")
    for item in no_video:
        print(" - ", item['title'], " - ", item['speaker'])

    # print("matched")
    # for item in merged:
    #     print(item['youtubetitle'])
    #     print(item['title'])

    update_talks(args.talks, merged)
    # TODO: Update title and description on youtube if different
    update_youtube(youtube, merged)

    if not args.no_upload and args.driveurl:
        to_upload, no_drive, no_talks = join(get_videos(drive, args.driveurl),
                                          no_video,
                                          key_drive,
                                          key_yaml,
                                          lambda l, r: dict([('drive_id', l['id'])] + list(r.items())))
        print("Can't match from drive", no_drive)
        do_upload(youtube, to_upload)



