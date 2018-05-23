import json

talks = json.load(open('talks.json'))
accepted_talks = [talk for talk in talks if talk['state'] == 'accepted']

talk_page = """
{title_block}

Format: {talk_format}

Abstract
--------

{abstract}

Description
-----------

{abstract}

Speaker
-------

{name_block}

Bio
```

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
    :align: left

"""

title_block = """

{title}
{title_underline}

"""

for talk in accepted_talks:
    talk['title_underline'] = '='*len(talk['title'])
    talk['title_block'] = title_block.format(**talk)
    if talk.get('avatar'):
        talk['name_block'] = avatar_block.format(**talk)
    talk['name_block'] += talk['name']
    if talk.get('twitter'):
        talk['name_block'] += twitter_block.format(**talk)
    if talk.get('link'):
        talk['name_block'] += link_block.format(**talk)
    print(talk_page.format(**talk))



