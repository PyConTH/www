from nikola import utils
from nikola.packages.datecond import date_in_range
from nikola.plugin_categories import ShortcodePlugin
from docutils.core import publish_parts

import re

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
    
YOUTUBE_URL_KEY = "youtube_url"

import ruamel.yaml

youtube_script = '''
<script>
    ( function() {

        var youtube = document.querySelectorAll( ".youtube" );

        for (var i = 0; i < youtube.length; i++) {

            var source = "https://i.ytimg.com/vi/"+ youtube[i].dataset.embed +"/hqdefault.jpg";

            var image = new Image();
            image.src = source;
            image.addEventListener( "load", function() {
                youtube[ i ].appendChild( image );
            }( i ) );

            youtube[i].addEventListener( "click", function(event) {

                var iframe = document.createElement( "iframe" );

                iframe.setAttribute( "frameborder", "0" );
                iframe.setAttribute( "allowfullscreen", "" );
                iframe.setAttribute( "src", "https://www.youtube.com/embed/"+ this.dataset.embed +"?rel=0&showinfo=0&autoplay=1" );
                iframe.setAttribute( "allow" , "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" );

                this.innerHTML = "";
                this.appendChild( iframe );
                
                event.stopPropagation();
            } );    
        };

    } )();
</script>
'''

youtube_style = '''
    <style>
        .youtube {
            background-color: #000;
            margin-bottom: 30px;
            position: relative;
            padding-top: 56.25%;
            overflow: hidden;
            cursor: pointer;
        }
        .youtube img {
            width: 100%;
            top: -16.84%;
            left: 0;
            opacity: 0.7;
        }
        .youtube .play-button {
            width: 90px;
            height: 60px;
            background-color: #333;
            box-shadow: 0 0 30px rgba( 0,0,0,0.6 );
            z-index: 1;
            opacity: 0.8;
            border-radius: 6px;
        }
        .youtube .play-button:before {
            content: "";
            border-style: solid;
            border-width: 15px 0 15px 26.0px;
            border-color: transparent transparent transparent #fff;
        }
        .youtube img,
        .youtube .play-button {
            cursor: pointer;
        }
        .youtube img,
        .youtube iframe,
        .youtube .play-button,
        .youtube .play-button:before {
            position: absolute;
        }
        .youtube .play-button,
        .youtube .play-button:before {
            top: 50%;
            left: 50%;
            transform: translate3d( -50%, -50%, 0 );
        }
        .youtube iframe {
            height: 100%;
            width: 100%;
            top: 0;
            left: 0;
        }
    </style>
'''

class ScheduleShortcode(ShortcodePlugin):
    def set_site(self, site):
        """Set the site."""
        super(ScheduleShortcode, self).set_site(site)
        site.register_shortcode('schedule', self.handler)
        
    def timeadd(self,a,b):
        a = list(map(int,a.split(":")))
        b = list(map(int,b.split(":")))
        c = [a[0]+b[0],a[1]+b[1]]
        if c[1]>=60:
            c[0] += c[1]//60
            c[1] %= 60
        c[0] = "%02d"%c[0]
        c[1] = "%02d"%c[1]
        return ":".join(map(str,c))
    
    def resolve_room_anchor(self,track):
        if track==1: return "track-1-auditorium"
        elif track==2: return "track-2-forum"
        elif track==3: return "track-3-cubiculum"
        elif track==4: return "track-4-aquarium"
        return ""
    
    def resolve_floor_anchor(self,track):
        if track==1: return "level-6"
        elif track<5: return "level-7"
        return ""
    
    def youtube_id(self, url):
        return re.findall(r"^(.*)/(.*)(&|$)", url)[0][1].replace('watch?v=','')
        
    def handler(self, mode="schedule", file="../talks2019.yaml", schedule_page="schedule", talks_page="talks", speakers_page="speakers",                sections=None, slugs=None, post_type='post', type=False,
                lang=None, template='post_list_directive.tmpl', sort=None,
                id=None, data=None, state=None, site=None, date=None, filename=None, post=None):
        dep = [file]
        return self.handle_schedule(file,schedule_page,talks_page,speakers_page,mode), dep
    
    def handle_schedule(self,file,schedule_page,talks_page,speakers_page,mode):
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


        with open(file) as f:
            #data = yaml.load(f, Loader=Loader)
            data = ruamel.yaml.load(f, ruamel.yaml.RoundTripLoader)

        talks = sorted([t for t in data['talks'] if 'day' in t], key=lambda t: (t['day'],t['time'],t['dur'],t['track']))
        tracks_ = data['tracks']
        daylabel_ = data['days']
        
        specialid = 1
        for talk in talks:
            talk['specialid'] = specialid
            specialid += 1

        tracks = {}
        daylabel = {}

        for x in daylabel_: daylabel[list(x.keys())[0]] = list(x.values())[0]
        for x in tracks_: tracks[list(x.keys())[0]] = list(x.values())[0]
        tracks[5] = ""

        #print(daylabel)

        for talk in talks:
          talk['day_raw'] = talk['day']
          talk['day'] = daylabel[talk['day']]


        #print(tracks)


        sched = []

        cur = None
        for talk in talks:
            if talk['time'] != cur:
                cur = talk['time']
                dur = talk['dur']
                day = talk['day']
                slot = dict(time=cur, dur=dur, day=day, talks=[])
                sched.append(slot)
            # now try to fit in the track
            slot['talks'].append(talk)

        #print(talks)
        #sched

        schedule = {}
        currrow = 1
        
        foundtrackfour = 0
        for s in sched:
          time = s['time']
          day = s['day']
          key = day+" "+time
          if not key in schedule: schedule[key] = []
          
          for talk in s['talks']:
            talk['row'] = currrow
            talk['col'] = 1 if talk['track'] != 4 else 2
            if 'track' in talk:
              talk['subcol'] = 5 if type(talk['track']) == list else talk['track']
              talk['colspan'] = 2 if talk['track'] == [1,2,3,4] else 1
              if talk['subcol'] is None: talk['subcol'] = 5
              if talk['track'] == 4: foundtrackfour = 3
              if talk['subcol']<5:
                if talk['subcol']<4:
                  talk['format'] = 'Talk'
                else:
                  talk['format'] = 'Workshop'
            else:
              talk['subcol'] = 1
              talk['colspan'] = 2
            talk['time'] = time
            if talk['subcol'] is None:
              talk['subcol'] = 5
              talk['colspan'] = 2
            if not 'dur' in talk: talk['dur'] = "00:00"
            talk['timeend'] = self.timeadd(talk['time'],talk['dur'])
            if not 'speaker' in talk or talk['speaker'] is None: talk['speaker'] = ""
            if not 'description' in talk or talk['description'] is None: talk['description'] = ""
            if not 'bio' in talk or talk['bio'] is None: talk['bio'] = ""
            if 'twitter' not in talk: talk['twitter'] = ""
            if 'speakerimg' not in talk or str(talk['speakerimg']) == "None": talk['speakerimg'] = "https://secure.gravatar.com/avatar/7ebded1e9171acbf1b8cbf3532e25172?s=500"
            if not '<p>' in talk['bio']: talk['bio'] = publish_parts(talk['bio'].strip(), writer_name="html")['html_body']
            if not '<p>' in talk['description']: talk['description'] = publish_parts(talk['description'].strip(), writer_name="html")['html_body']
            if 'format' in talk:
                talk['timeplace'] = day+" "+time+" @ "+tracks[talk['track']]
            else:
                talk['timeplace'] = day+" "+time
            talk['room_anchor'] = self.resolve_room_anchor(talk['subcol'])
            talk['floor_anchor'] = self.resolve_floor_anchor(talk['subcol'])
            #talk[YOUTUBE_URL_KEY] = "https://www.youtube.com/watch?v=5cOOKMU0Ztw&feature=youtu.be" #For testing
            if YOUTUBE_URL_KEY in talk: talk["youtube_id"] = self.youtube_id(talk[YOUTUBE_URL_KEY])
            #talk.setdefault(YOUTUBE_URL_KEY,"https://www.youtube.com/watch?v=5cOOKMU0Ztw&feature=youtu.be")
            
            schedule[key].append(talk)
          
          for talk in s['talks']:
            if foundtrackfour <= 0:
                talk['colspan'] = 2
                
          foundtrackfour -= 1
          
          currrow += 1
        
        if mode == "schedule":

            html = '<h2>Tracks</h2> <div style="display:flex;">'

            for track in tracks:
              if tracks[track] != "": html += '<div class="schedule-item schedule-item-{}">{}</div>'.format(track,tracks[track])
            
            html += "</div>"

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
              subhtml = '<div class="timeflex" style="grid-row-start: {}; grid-row-end: {}; grid-column-start: {}; grid-column-end: {};"> <div class="timetext"><div><b>{}</b></div><div class="timetext-divider">&nbsp;-&nbsp;</div><div><b>{}</b></div></div> <div class="schedule-item-container" style="flex-grow:1;">'.format(talk['row']-rowoffset,talk['row']-rowoffset,talk['col'],talk['col']+talk['colspan'],talk['time'],talk['timeend'])
              for talk in s:
                if talk['col'] == 1:
                  subhtml += '''		<div class="schedule-item schedule-item-{}" style="order: {};" data-special-id="{}" id="{id}" onclick="var hid='hidden-field-'+$(this).data('special-id'); if (!$('#'+hid).hasClass('active')) $('#'+hid).fadeIn(250),$('#'+hid).addClass('active'); else $('#'+hid).fadeOut(250),$('#'+hid).removeClass('active');">
                  <div class="v-sign">v</div>
                  <div><b>{}</b></div>
                  <div>{}</div>
                  <div class="hidden-field" id="hidden-field-{}">
                    <br>
                    <div style="display:{youtube_display};">
                        <a href="{youtube_url}" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/YouTube_full-color_icon_%282017%29.svg/1280px-YouTube_full-color_icon_%282017%29.svg.png" style="height:18px; display: inline;"> WATCH IN YOUTUBE</a>
                        
                        <div style="margin-top: 5px;">
                            <!-- (1) video wrapper -->
                            <div class="youtube" data-embed="{youtube_id}"> 

                                <!-- (2) the "play" button -->
                                <div class="play-button"></div> 

                            </div>
                        </div>
                    </div>
                    <br>
                    <div><a href="/layout#{layoutanchor}">{}</a></div>
                    <br>
                    <div><b>Description:</b></div>
                    <div>{}</div>
                    <br>
                    <div><b>Bio:</b></div>
                    <div>{}</div>
                    <br>
                    <div><b>{}</b></div>
                    <br>
                    <a href="/talks#{id}">View more talks information</a> <br>
                    <a href="/speakers#{id}">View more speaker information</a>
                  </div>
                </div>'''.format(talk['subcol'],talk['subcol']-1,talk['specialid'],talk['title'],talk['speaker'],talk['specialid'],talk['timeplace'],talk['description'],talk['bio'],tracks[talk['subcol']],layoutanchor=talk['room_anchor'], 
                                 youtube_display = "block" if YOUTUBE_URL_KEY in talk else "none",
                                 youtube_url=talk[YOUTUBE_URL_KEY] if YOUTUBE_URL_KEY in talk else '',
                                 youtube_id=talk['youtube_id'] if 'youtube_id' in talk else '',
                                 id=str(talk['day_raw']) + "-" + str(talk['track']) + "-" + str(talk['time'])
                                )
              subhtml += '</div> </div>'
              for talk in s:
                if talk['col'] == 2:
                  subhtml += '''	<div class="workshop-item" style="grid-row-start:{}; grid-row-end:{}; grid-column-start: {}; grid-column-end: {};" data-special-id="{}" id="{id}" onclick="var hid='hidden-field-'+$(this).data('special-id'); if (!$('#'+hid).hasClass('active')) $('#'+hid).fadeIn(250),$('#'+hid).addClass('active'); else $('#'+hid).fadeOut(250),$('#'+hid).removeClass('active');">
                <div class="workshop-text">
                  <div class="v-sign">v</div>
                  <b>{}</b><br>
                  {}
                  <div class="hidden-field" id="hidden-field-{}">
                    <br>
                    <div style="display:{youtube_display};">
                        <a href="{youtube_url}" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/YouTube_full-color_icon_%282017%29.svg/1280px-YouTube_full-color_icon_%282017%29.svg.png" style="height:18px; display: inline;"> WATCH IN YOUTUBE</a>
                        
                        <div style="margin-top: 5px;">
                            <!-- (1) video wrapper -->
                            <div class="youtube" data-embed="{youtube_id}"> 

                                <!-- (2) the "play" button -->
                                <div class="play-button"></div> 

                            </div>
                        </div>
                    </div>
                    <br>
                    <div><a href="/layout#{layoutanchor}">{}</a></div>
                    <br>
                    <div><b>Description:</b></div>
                    <div>{}</div>
                    <br>
                    <div><b>Bio:</b></div>
                    <div>{}</div>
                    <br>
                    <div><b>{}</b></div>
                    <br>
                    <a href="/talks#{id}">View more talks information</a> <br>
                    <a href="/speakers#{id}">View more speaker information</a>
                  </div>
                </div>
              </div>'''.format(talk['row']-rowoffset,talk['row']-rowoffset+3,talk['col'],talk['col'],talk['specialid'],talk['title'],talk['speaker'],talk['specialid'],talk['timeplace'],talk['description'],talk['bio'],tracks[talk['subcol']],layoutanchor=talk['room_anchor'],
                                 youtube_display = "block" if YOUTUBE_URL_KEY in talk else "none",
                                 youtube_url=talk[YOUTUBE_URL_KEY] if YOUTUBE_URL_KEY in talk else '',
                                 youtube_id=talk['youtube_id'] if 'youtube_id' in talk else '',
                                 id=str(talk['day_raw']) + "-" + str(talk['track']) + "-" + str(talk['time'])
                              )

              html += subhtml

            #print(html)

            #Generate html file
            htmlhead = '''
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <meta name="date" content="2019-06-10 22:28" />
            <meta name="summary" content="Conference Schedule" />

            <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.js"></script>

            <style>
            .root-container a {
                color: white !important;
            }
            
            .v-sign {
                float: right;
                transform: scaleX(2);
                margin-top: -3px;
                margin-right: 5px;
            }

            .grid-container {
                width: 100%;
                display: grid;
                grid-template-columns: 60% auto;
                grid-row-gap: 10px;
                grid-column-gap: 5px;
            }

            .timeflex {
                display: flex;
                flex-direction: row;
            }

            .schedule-item-container {
                display:flex;
                flex-direction: column;
            }

            .schedule-item {
                padding: 5px;
                padding-left: 10px;
                color: white;
                width: 100%;
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
                padding: 5px;
                padding-left: 10px;
            }

            .workshop-item .workshop-text {

            }

            .timetext {
                padding-right: 5px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            
            .timetext .timetext-divider {
                display: none;
            }

            .hidden-field {
              display: none;
            }
            
            @media screen and (max-width: 576px) /* Mobile */ {
                .timeflex {
                    flex-direction: column;
                }
                
                .timetext {
                    flex-direction: row;
                    justify-content: flex-start;
                }
                
                .timetext .timetext-divider {
                    display: block;
                }
            }
            </style>
            ''' + youtube_style


            return ''+htmlhead+'<div class="root-container">'+html+'</div>'+youtube_script
        
        elif mode=="talks":
            html = '<div>'
            
            talks = sorted(talks,key=lambda t: t['title'])
            
            htmlhead = youtube_style
            
            htmlblock = '''
            <div class="clearfix section" id="{id}">
                <h1>{}</h1>
                <p>by <a href="/speakers#{id}">{}</a></p>
                <div style="display:{youtube_display};">
                    <!-- (1) video wrapper -->
                    <div class="youtube" data-embed="{youtube_id}"> 

                        <!-- (2) the "play" button -->
                        <div class="play-button"></div> 

                    </div>
                </div>
                <p>Format: {} (Duration: {})</p>
                <p><a href="/schedule#{id}">{}</a></p>
                <div class="section" id="abstract">
                    <h2>Abstract</h2>
                    <p>{}</p>
                </div>
            </div>
            '''
            
            for talk in talks:
                if not 'format' in talk: continue
                html += htmlblock.format(talk['title'],talk['speaker'],talk['format'],talk['dur'],talk['timeplace'],talk['description'], 
                                         youtube_display = "block" if YOUTUBE_URL_KEY in talk else "none",
                                         youtube_id=talk['youtube_id'] if 'youtube_id' in talk else '',
                                         id=str(talk['day_raw']) + "-" + str(talk['track']) + "-" + str(talk['time'])
                                        )
            
            html += '</div>'
            
            return htmlhead + html + youtube_script
        
        elif mode=="speakers":
            html = '<div>'
            
            talks = sorted(talks,key=lambda t: t['speaker'])
            
            htmlhead = '''
            <style>
                .profile-img { height: 200px; float:right; border-radius:50%; }
                @media screen and (max-width: 576px) /* Mobile */ {
                    .profile-img { float: none; }
                }
            </style>
            '''
            
            htmlblock = '''
            <div class="clearfix section" id="{id}">
                <h1>{}</h1>
                <img alt="{}" class="img-circle img-responsive align-right profile-img" src="{}">
                {}
                <p>Talk: <a href="/talks#{id}">{}</a></p>
                <p><a href="/schedule#{id}">{}</a></p>
                <div class="section" id="biography">
                  <h2>Biography</h2>
                  <p>{}</p>
                </div>
            </div>
            '''
            
            for talk in talks:
                if not 'format' in talk: continue
                html += htmlblock.format(talk['speaker'],talk['speaker'],talk['speakerimg'],
                                         '<p class="fa fa-twitter fa-fw"><a class="reference external" href="https://twitter.com/{}">{}</a></p>'.format(talk['twitter'],talk['twitter']) if len(talk['twitter'].strip()) > 0 else ""
                                         ,talk['title'],talk['timeplace'],talk['bio'],
                                        id=str(talk['day_raw']) + "-" + str(talk['track']) + "-" + str(talk['time']))
            
            html += '</div>'
            
            return htmlhead+html
