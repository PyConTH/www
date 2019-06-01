import json
import datetime as dt
import html2text
import re
from copy import deepcopy

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
# Anything that isn't a square closing bracket
name_regex = "[^]]+"
# http:// or https:// followed by anything but a closing paren
url_regex = "http[s]?://[^)]+"

markup_regex = '\[({0})]\(\s*({1})\s*\)'.format(name_regex, url_regex)
markex = re.compile(markup_regex,re.IGNORECASE)

for x in accepted_talks:
    if x['title'] == "Deep Learning Introductory Workshop with TensorFlow 2.0":
        newtalk = deepcopy(x)
        x["name"] = "Sam Witteveen"
        newtalk['name'] = 'Martin Andrews'
        x['bio'] = """Sam is a Google Developer Expert for Machine Learning and is a co-founder of Red Dragon AI a deep tech company based in Singapore. He has extensive experience in startups and mobile applications and is helping developers and companies create smarter applications with machine learning. Sam is especially passionate about Deep Learning and AI in the fields of Natural Language and Conversational Agents and regularly shares his knowledge at events and trainings across Asia, as well as being the co-organiser of the Singapore TensorFlow and Deep Learning group. แซมพูดและอ่านภาษาไทยได้"""
        newtalk['bio'] = """Martin has over 20 years’ experience in Machine Learning and has used it to solve problems in financial modelling and has created AI automation for companies. His current area of focus and speciality is in natural language processing and understanding. In 2017, Google appointed Martin as one of the first 12 Google Developer Experts for Machine Learning. Martin is also one of the co-founders of Red Dragon AI."""
        newtalk['avatar'] = "https://th.pycon.org/martin-andrews.jpeg"
        newtalk['twitter'] = ''
        xtratalks.append(newtalk)
    else:
        x['bio'] = x['bio'].replace("<ul>","")
        x['bio'] = x['bio'].replace("</ul>","")
        x['bio'] = re.sub(r'<li>([^<]*)</li>', r'- \1',x['bio'])
        x['bio'] = x['bio'].replace("Link:","  Link:")
        x['bio'] = re.sub(markex,r'`\1 <\2>`_',x['bio'])


accepted_talks += xtratalks
accepted_talks.sort(key=lambda x: x["name"])
#for x in accepted_talks:
    #if x['name'].lower() == "Nithiroj Tripatarasit".lower():
        #x['bio'] = x['bio'].split("**Experiences:**")[0]
    #x['bio'] = html2text.html2text(x['bio'])

talk_page = """

.. class:: clearfix

{name_block}

Talk: {title}

Biography
---------

{bio}

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
.. title: Speakers
.. slug: speakers
.. date: {}
.. tags:
.. category:
.. link:
.. description: List of confirmed speakers.
.. type: text
"""
print(header.format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC+07:00")))

speakers = {}

for talk in accepted_talks:
    # title
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

