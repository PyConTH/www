#!/usr/bin/python3
""" Upload talks
"""
import json
import yaml

TALKS = yaml.load(open('talks-retry.yaml'))

desc = """
PyCon Thailand: https://2018.th.pycon.org/

{title}

Speaker: {speaker}

------------

Description:
{description}

------------

Bio:
{bio}
"""

META_TMPL = {
    "title": "my test title",
    "description": "my test description",
    "tags": ["python", ],
    "privacyStatus": "public",
    "embeddable": True,
    "license": "creativeCommon",
    "publicStatsViewable": True,
    # "publishAt": "2017-06-01T12:05:00+02:00",
    "categoryId": "22", # People & Blogs (like PyCon US)
    "recordingdate": "2018-06-16",
    "location": {
        "latitude": 13.7205,
        "longitude": 100.498368
    },
    "locationDescription": "Knowledge Exchange Center – KX",
    "playlistTitles":  ["PyCon Thailand 2018"],
    "language":  "en"
}

with open('commands.sh', 'w') as commands:
    for talk in TALKS:
        if 'file' not in talk:
            commands.write('# "{}" missing\n'.format(talk['title']))
            continue
        talk['description'] = desc.format(**talk)
        meta = {}
        meta.update(META_TMPL)
        meta.update(talk)
        fn = talk['file']
        if "/17/" in fn:
            meta['recordingdate'] = "2018-06-17"
        jsonfn = '{}.json'.format(fn)
        with open(jsonfn, 'w') as meta_json:
            json.dump(meta, meta_json)
        command = './youtubeuploader_linux_amd64 -metaJSON "{}" -filename "{}"\n'.format(jsonfn, fn)
        commands.write(command)
