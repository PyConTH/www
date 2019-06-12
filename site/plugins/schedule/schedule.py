from nikola import utils
from nikola.packages.datecond import date_in_range
from nikola.plugin_categories import ShortcodePlugin

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class ScheduleShortcode(ShortcodePlugin):
    def set_site(self, site):
        """Set the site."""
        super(ScheduleShortcode, self).set_site(site)
        site.register_shortcode('schedule', self.handler)
        
    def handler(self, mode="schedule", file="../talks2019.yaml", schedule_page="schedule", talks_page="talks", speakers_page="speakers", site=None):
        dep = [file]
        if mode=="schedule":
            return self.handle_schedule(file,schedule_page,talks_page,speakers_page), dep
    
    def handle_schedule(file,schedule_page,talks_page,speakers_page):
        with open(file) as f:
            data = yaml.load(f, Loader=Loader)

        talks = sorted([t for t in data['talks'] if 'day' in t], key=lambda t: (t['day'],t['time'],t['dur'],t['track']))
        tracks = data['tracks']

        #print(tracks)


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

        #print(talks)
        #sched

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
            if talk['subcol'] is None:
              talk['subcol'] = 5
              talk['colspan'] = 2
            if not 'speaker' in talk or talk['speaker'] is None: talk['speaker'] = ""
            if not 'description' in talk or talk['description'] is None: talk['description'] = ""
            if not 'bio' in talk or talk['bio'] is None: talk['bio'] = ""
            schedule[time].append(talk)
          currrow += 1

        html = '<h2>Tracks</h2>'

        for track in tracks:
          html += '<div class="schedule-item schedule-item-{}">{}</div>'.format(list(track.keys())[0],list(track.values())[0])

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
              subhtml += '''		<div class="schedule-item schedule-item-{}" style="order: {};" onclick="var hid='hidden-field-{}-{}'; if (!$('#'+hid).hasClass('active')) $('#'+hid).fadeIn(250),$('#'+hid).addClass('active'); else $('#'+hid).fadeOut(250),$('#'+hid).removeClass('active');">
              <div><b>{}</b></div>
              <div>{}</div>
              <div class="hidden-field" id="hidden-field-{}-{}">
                <br>
                <div><b>Description:</b></div>
                <div>{}</div>
                <br>
                <div><b>Bio:</b></div>
                <div>{}</div>
              </div>
            </div>'''.format(talk['subcol'],talk['subcol']-1,talk['row'],talk['subcol'],talk['title'],talk['speaker'],talk['row'],talk['subcol'],talk['description'],talk['bio'].strip() if 'bio' in talk else '')
          subhtml += '</div> </div>'
          for talk in s:
            if talk['col'] == 2:
              subhtml += '''	<div class="workshop-item" style="grid-row-start:{}; grid-row-end:{}; grid-column-start: {}; grid-column-end: {};" onclick="var hid='hidden-field-{}-{}'; if (!$('#'+hid).hasClass('active')) $('#'+hid).fadeIn(250),$('#'+hid).addClass('active'); else $('#'+hid).fadeOut(250),$('#'+hid).removeClass('active');">
            <div class="workshop-text">
              <b>{}</b><br>{}
              <div class="hidden-field" id="hidden-field-{}-{}">
                <br>
                <div><b>Description:</b></div>
                <div>{}</div>
                <br>
                <div><b>Bio:</b></div>
                <div>{}</div>
              </div>
            </div>
          </div>'''.format(talk['row']-rowoffset,talk['row']-rowoffset+3,talk['col'],talk['col'],talk['row'],talk['subcol'],talk['title'],talk['speaker'],talk['row'],talk['subcol'],talk['description'],talk['bio'].strip() if 'bio' in talk else '')

          html += subhtml

        #print(html)

        #Generate html file
        htmlhead = '''
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <meta name="date" content="2018-05-23 22:28" />
        <meta name="summary" content="Conference Schedule" />
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.js"></script>
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
        .schedule-item:hover, .workshop-item:hover {
          opacity: 0.8;
          cursor: pointer;
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
        .workshop-item, .schedule-item-4 {
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
        a {
          color: white;
        }
        .hidden-field {
          display: none;
        }
        </style>
        '''

        return ''+htmlhead+''+html+''
