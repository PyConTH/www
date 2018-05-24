import json

talks = json.load(open('talks.json'))
accepted_talks = [talk for talk in talks if talk['state'] == 'accepted']

talk_page = """
.. class:: clearfix

{title_block}

Format: {talk_format}

Abstract
--------

{abstract}

Description
-----------

{description}

{name_block}

Bio
---

{bio}

-------
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

