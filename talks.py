import json
import datetime as dt
import html2text

xtratalks = []
xtratalks.append({
    "name": "Mohamed Ali SOLA (Dali SOLA)",
    "email": "mohamed.ali.sola@gmail.com",
    "title": "Unlocking the power of natural language by machine translation: how python could serve my purpose?",
    "abstract": """With more than 7000 languages spoken across the world, it becomes more and more important to connect people and cultures together; Machine translation shows a real impact at this level.
This talk will go through:

- The translation problems, purposes of machine translation in industry, Entertainment Industry as an example (movies subtitles and TV contents)

- How to build a machine translation with a higher quality of translation output.

- NLP tools around machine translation and the advantages of python in the development process.""",
    "bio":"""Dali SOLA is a Data science enthusiast with experience in various aspects of NLP and machine translation.
        Dali had an engineer degree from at TEK-UP University in Tunisia and studied two Master degree in
        Business Intelligence and Innovation management. His core interest lies in “NLP”, ”Deep learning”,
        “Machine Learning”, ”Machine Translation” and "IA". In 2017 he get rewarded from ATB BANK  for  his solution "smart-HR",
        a human resource solution that deal with talents hiring issue, using NLP and IA .""",
    "twitter":"",
    "avatar":"",
    'talk_format': "Talk (~30-45 minutes)"
        })




talks = json.load(open('PyCon Thailand 2019 Submissions.json'))
accepted_talks = [talk for talk in talks if talk['state'] == 'accepted' and talk["confirmed"]]

accepted_talks += xtratalks


accepted_talks.sort(key=lambda x: x["name"])
for x in accepted_talks:
    x['bio'] = html2text.html2text(x['bio'])




talk_page = """

.. class:: clearfix

{title_block}
by {name}

Format: {talk_format}

Abstract
--------

{abstract}

"""

twitter_block = """

.. class:: fa fa-twitter fa-fw

    `{twitter} <https://twitter.com/{twitter}>`_

"""

link_block = """

.. class:: fa fa-link fa-fw

    {url}

"""

avatar_block = """

.. image:: {avatar}
    :alt: {name}
    :height: 200px
    :align: right
    :class: img-circle img-responsive

"""

title_block = """

{title}
{title_underline}

"""

name_block = """
{name}
{name_underline}

{avatar_block}

{twitter_block}
{link_block}
"""

header = """
.. title: Talks
.. slug: talks
.. date: {}
.. tags:
.. category:
.. link:
.. description: List of confirmed talks.
.. type: text
"""
print(header.format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC+07:00")))

speakers = {}

for talk in accepted_talks:
    # title
    talk["title"] = talk["title"].replace("\t"," ")
    talk['title_underline'] = '='*len(talk['title'])
    talk['title_block'] = title_block.format(**talk)
    # speaker
    talk['avatar_block'] = ""
    if talk.get('avatar'):
        talk['avatar_block'] = avatar_block.format(**talk)
    talk['twitter_block'] = ""
    if talk.get('twitter'):
        talk['twitter_block'] = twitter_block.format(**talk)
    talk['link_block'] = ""
    if talk.get('link'):
        talk['link_block'] = link_block.format(**talk)
    talk['name_underline'] = '='*len(talk['name'])
    talk['name_block'] = name_block.format(**talk)

    print(talk_page.format(**talk))

