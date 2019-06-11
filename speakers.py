import json
import datetime as dt
import html2text
import re
from copy import deepcopy

FILELOC="/home/fw/Downloads/"

seenemail=[]
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

xtratalks.append({
    "name": "Mishari Muqbil",
    "email": "mishari@mishari.net",
    "title": "Teaching Coding To Kids",
"abstract": """This is a workshop for adults such as parents, teachers, community organizers and others interested in organizing classes where kids learn how to program Python in a peer to peer, collaborative learning environment.

We will take a time machine back to the time when we were just starting off with coding and explore what that “aha” moments were for each of us. Based on that we will split into groups along common themes and design learning paths and a curriculum outline for kids to explore the joys of programming.

Collaborative learning environments put less emphasis on instructors and more on children’s natural tendency to be curious and to share. As part of this workshop you will learn how to facilitate such an environment.

Kids are welcome to join too as subject matter experts and participants in the process.

Requirement:
 - Humans aged 7+
 - Computer, Tablet or anything that runs Python
""",
    "twitter":"",
    "bio": "CEO of Zymple",
    "avatar":"",
    'talk_format': "Workshop (> 60 minutes)"
        })

xtratalks.append({
    "name": "Chanapai Chuadchum",
    "email": "teslacoil358@gmail.com",
    "title": "How to build an open source catbot with Python, a 3D printer and a microcontroller",
    "abstract": """This talk is about a project that was designed to test the ML A.I research and robotics opensource. The aim is to improve the robot's ability at human interaction and develop various applications for the robot. Right now this robot is an early protype with limited applications. This project aims to improve the robot's abilities in the near future.""",
    "twitter":"",
    "avatar":"",
    "bio": """My real name is Chanapai Chuadchum my nick name is Korn i was started my work on roobtics since i was 10 on the and i got the thrid place on the competition in Solar innovative contest when i was 11 years old since then i'm dedicated to working on robotics to develop the useful and sophisticated robots to make them life like as most as i can currently i'm studying robotics engineer at the pensylavania university online in Robotics Engineer Master degree
Currently i'm trying to make my own company in robotics field to serve humanity as much as possible to eleminate the time that we need to spend on unneccessary thing.""",
    'talk_format': "Talk (~30-45 minutes)"
        })

xtratalks.append({
    "name": "Shane Torr",
    "email": "shanetorr@gummybear.asia",
    "title": "Tech Skills: What's Hot And What's Not.",
    "abstract": """Wonder if your skills are in demand or if you need to change direction? This session will give context to the current tech skills market in Thailand, and which web development skills are most in demand now.  We’ll see how Python compares to other languages, and what future prospects might be for Python Developers.""",
    "twitter":"",
    "avatar":"",
    "bio": """Shane is CEO at Gummy Bear Tech Recruitment. He has over 30 years international experience in IT, and has been based in Thailand for the last 17 years where he’s been focusing on technical recruitment.  Strong interest in SaaS applications, cloud technologies, and Linux desktops""",
    'talk_format': "Talk (~30-45 minutes)"
        })


talks = json.load(open(FILELOC + 'PyCon Thailand 2019 Submissions.json'))
#accepted_talks = [talk for talk in talks if talk['state'] == 'accepted' and talk["confirmed"]]
accepted_talks = [talk for talk in talks if talk['state'] == 'accepted']
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
        newtalk['email'] = 'GitHub@mdda.net'.lower()
        xtratalks.append(newtalk)
    elif x['title'].lower() == "code like a girl":
        x['title'] = "Python for beginners"
    elif x["title"].startswith("AIoT"):
        x["bio"] = "CEO of DycodeX - the AIoT enabler in Indonesia. Microsoft Most Valuable Professional (MVP) of Microsoft Azure. 15 years as entrepreneur. A developer, hardware maker, and public speaker. "
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
    if talk['email'].strip().lower() not in seenemail:
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
        seenemail.append(talk['email'].strip().lower())

