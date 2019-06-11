""""

Goal is to talk a yaml file of talks data and produce
- responsive schedule
- talks page
- speakers page
- embeded videos
- all linked together


Schedule grid assumes talks don't end in the middle of other talks.

Layout alg is

[11-12
  [11-11:30



"""


import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open('talks2019.yaml') as f:
    data = yaml.load(f, Loader=Loader)

talks = sorted([t for t in data['talks'] if 'day' in t], key=lambda t: (t['day'],t['time'],-t['dur'],t['track']))


sched = []

cur = None
for talk in talks:
    if talk['time'] != cur:
        cur = talk['time']
        dur = talk['dur']
        slot = dict(time=cur, dur=dur, talks=[])
        sched.append(slot)
    # now try to fit in the track
    slot['talks'].append(talk)

print(talks)




