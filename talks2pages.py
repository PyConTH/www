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

talks = sorted([t for t in data['talks'] if 'day' in t], key=lambda t: (t['day'],t['time'],t['dur'],t['track']))


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
sched

schedule = {}
currrow = 1
for s in sched:
  time = s['time']
  if not time in schedule: schedule[time] = []
  for talk in s['talks']:
    talk['row'] = currrow
    talk['col'] = 1 if talk['track'] != 4 else 2
    if 'track' in talk:
      talk['subcol'] = 5 if type(talk['track']) == list else talk['track']
      talk['colspan'] = 2 if talk['track'] == [1,2,3,4] else 1
    else:
      talk['subcol'] = 1
      talk['colspan'] = 2
    talk['time'] = time
    schedule[time].append(talk)
  currrow += 1
    
html = ''

currday = ""
rowoffset = 0

for t in schedule:
  s = schedule[t]
  if len(s) == 0: continue
  talk = s[0]
  if talk['day'] != currday:
    if currday != "": html += "</div>"
    html += '<h2>' + talk['day'] + '</h2> <div class="grid-container">'
    currday = talk['day']
    rowoffset = talk['row']-1
  subhtml = '<div class="timeflex" style="grid-row-start: {}; grid-row-end: {}; grid-column-start: {}; grid-column-end: {};"> <div class="timetext"><b>{}</b></div> <div class="schedule-item-container" style="flex-grow:1;">'.format(talk['row']-rowoffset,talk['row']-rowoffset,talk['col'],talk['col']+talk['colspan'],t)#,talk['row'],talk['row'],talk['col'],talk['col']+talk['colspan'])
  for talk in s:
    if talk['col'] == 1:
      subhtml += '''		<div class="schedule-item schedule-item-{}" style="order: {};">
			<div><b>{}</b></div>
			<div>{}</div>
		</div>'''.format(talk['subcol'],talk['subcol']-1,talk['title'],talk['speaker'])
  subhtml += '</div> </div>'
  for talk in s:
    if talk['col'] == 2:
      subhtml += '''	<div class="workshop-item" style="grid-row-start:{}; grid-row-end:{}; grid-column-start: {}; grid-column-end: {};">
		<div class="workshop-text">
			<b>{}</b><br>{}
		</div>
	</div>'''.format(talk['row']-rowoffset,talk['row']-rowoffset+3,talk['col'],talk['col'],talk['title'],talk['speaker'])
  html += subhtml

print(html)

schedule

#Generate html file
htmlhead = '''
<style>
.grid-container {
	width: 100%;
	display: grid;
	grid-template-columns: 60% auto;
	grid-row-gap: 10px;
}

.timeflex {
	display: flex;
	flex-direction: row;
}

@media screen and (max-width: 500px) /* Mobile */ {
	.timeflex {
		flex-direction: column;
	}
}

.schedule-item-container {
	display:flex;
	flex-direction: column;
}

.schedule-item {
	padding: 5px;
	padding-left: 10px;
	color: white;
	width: calc(100% - 20px);
	margin-bottom: 5px;
}

.schedule-item-1 {
	background-color: darkblue;
}

.schedule-item-2 {
	background-color: darkgreen;
}

.schedule-item-3 {
	background-color: darkred;
}

.schedule-item-5 {
	background-color: gray;
}

.p-5 {
	padding: 5px;
}

.workshop-item {
	grid-column-start:3;
	background-color: purple;
	color: white;
	margin-bottom: 5px;
	padding: 10px;
	margin-right: 5px;
}

.workshop-item .workshop-text {

}

.timetext {
	padding-top: 5px;
	padding-right: 5px;
}
</style>

<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
'''

with open('schedule_table.html','w') as f:
  f.write('<!doctype html><html><head>'+htmlhead+'</head><body>'+html+'</body></html>')

