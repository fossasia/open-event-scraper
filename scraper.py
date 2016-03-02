import csv
import json
import datetime
import simplejson
import validators
import jsonpickle
import logging
import parser
from pprint import pprint

from models import *

# TODOS:
# 1. Multiple speakers
# 2. Sesion association

# Track config is filename, header
# Should have all track information
# ID Prefix = should be unique across tracks
# Color code

#1. Tech Kids I
#2. Tech Kids II
#3. OpenTech and IoT
#4. OpenTech Workshops
#5. WebTech
#6. Exhibition
#7. Hardware and IoT
#8. Python
#9. Databases
#10.Big Data/Open Data
#11.DevOps
#12.Privacy and Security
#13.Internet, Society, Community
#14.Science Hack Day
#15.Linux and MiniDebConf
#16.Design, VR, 3D

TRACK_CONFIG = [
    Track(id=1, name='Tech Kids I', filename='TechKidsI.tsv',
          header_line=2,
          session_id_prefix=100,
          key_color="#3DC8C3",),

    # Track(id=2, name='Tech Kids II', filename='TechKidsII.tsv',
    #       header_line=2,
    #       session_id_prefix=100,
    #       key_color="#3DC8C3",),

    # Track(id=3, name='OpenTech and IoT', filename='opentech.tsv',
    #       header_line=2,
    #       session_id_prefix=100,
    #       key_color="#3DC8C3",),

    # Track(id=4, name='OpenTech Workshops', filename='OpenTechWorkshops.tsv',
    #       header_line=2,
    #       session_id_prefix=100,
    #       key_color="#3DC8C3",),

    # Track(id=5, name='WebTech', filename='WebTech.tsv',
    #       header_line=2,
    #       session_id_prefix=100,
    #       key_color="#3DC8C3",),

    # Track(id=6, name='Exhibition', filename='exhibition.tsv',
    #       header_line=2,
    #       session_id_prefix=100,
    #       key_color="#3DC8C3",),

    # Track(id=7, name='Hardware and IoT', filename='Hardware.tsv',
    #       header_line=2,
    #       session_id_prefix=100,
    #       key_color="#3DC8C3",),

    # Track(id=8, name='Python', filename='python.tsv',
    #       header_line=2,
    #       session_id_prefix=100,
    #       key_color="#3DC8C3",),

    # Track(id=9, name='Databases', filename='DB.tsv',
    #       header_line=2,
    #       session_id_prefix=100,
    #       key_color="#3DC8C3",),

    # Track(id=10, name='Big Data/Open Data', filename='Data.tsv',
    #       header_line=2,
    #       session_id_prefix=100,
    #       key_color="#3DC8C3",),

    # Track(id=11, name='DevOps', filename='devops.tsv',
    #       header_line=2,
    #       session_id_prefix=100,
    #       key_color="#3DC8C3",),

    # Track(id=12, name='Privacy and Security', filename='Privacy-Security.tsv',
    #       header_line=2,
    #       session_id_prefix=100,
    #       key_color="#3DC8C3",),

    # Track(id=13, name='Internet, Society, Community', filename='ISC.tsv',
    #       header_line=2,
    #       session_id_prefix=100,
    #       key_color="#3DC8C3",),

    # Track(id=14, name='Science Hack Day', filename='ScienceHackDay.tsv',
    #       header_line=2,
    #       session_id_prefix=100,
    #       key_color="#3DC8C3",),

    # Track(id=15, name='Linux and MiniDebConf', filename='Linux.tsv',
    #       header_line=2,
    #       session_id_prefix=100,
    #       key_color="#3DC8C3",),

    # Track(id=16, name='Design, VR, 3D', filename='Design.tsv',
    #       header_line=2,
    #       session_id_prefix=100,
    #       key_color="#3DC8C3",)
]

# Provide year of conference in case the date is impossible to parse
YEAR_OF_CONF = '2016'


def parse_file(track):
    HEADERS = []
    with open(track.filename) as tsv:
        i = 1
        speaker = None
        session = None
        for line in csv.reader(tsv, delimiter="\t"):
            if i == track.header_line:
                HEADERS = map(str.strip, line)
            elif i > track.header_line:
                #   parse_row
                row = create_associative_arr(line, HEADERS)
                # print row, "\n"
                (res_speaker, res_session) = parse_row(
                  row,  
                  speaker,
                  session, 
                  track, 
                  track.session_id_prefix + (10 * i),
                )

                if res_session is not None and res_speaker is not None:
                    speaker = res_speaker
                    session = res_session
            i = i + 1


def create_associative_arr(line, headers):
    result = dict(zip(headers, line))
    return result

SPEAKERS = []
SESSIONS = []

GLOBAL_SPEAKER_IDS = {}


def parse_row(row, last_speaker, last_session, current_track, id_prefix=10,):
    """
    Format of Data
    # Speaker
    # name = db.Column(db.String, nullable=False)
    # photo = db.Column(db.String)
    # biography = db.Column(db.Text)
    # email = db.Column(db.String, nullable=False)
    # web = db.Column(db.String)
    # twitter = db.Column(db.String)
    # facebook = db.Column(db.String)
    # github = db.Column(db.String)
    # linkedin = db.Column(db.String)
    # organisation = db.Column(db.String, nullable=False)
    # position = db.Column(db.String)
    # country = db.Column(db.String, nullable=False)
    # event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    # Session
    # id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String, nullable=False)
    # subtitle = db.Column(db.String)
    # abstract = db.Column(db.Text)
    # description = db.Column(db.Text, nullable=False)
    # start_time = db.Column(db.DateTime,
    #                        nullable=False)
    # end_time = db.Column(db.DateTime,
    #                      nullable=False)
    # track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'))
    # speakers = db.relationship('Speaker',
    #                            secondary=speakers_sessions,
    #                            backref=db.backref('sessions',
    #                                               lazy='dynamic'))
    # level_id = db.Column(db.Integer,
    #                      db.ForeignKey('level.id'))
    # format_id = db.Column(db.Integer,
    #                      db.ForeignKey('format.id'))
    # language_id = db.Column(db.Integer,
    #                      db.ForeignKey('language.id'))
    # microlocation_id = db.Column(db.Integer,
    #                      db.ForeignKey('microlocation.id'))
    #
    # event_id = db.Column(db.Integer,
    #                      db.ForeignKey('events.id'))
    """
    # pprint(row)
    # if row.has_key("Email") and len(row["Email"]) > 1 and len(validate_result(row["Email"], "", "EMAIL")) > 1:
    #     if GLOBAL_SPEAKER_IDS.has_key(row["Email"]) is not True:
    #         speaker = Speaker()
    #     else:
    #         speaker = GLOBAL_SPEAKER_IDS[row["Email"]]
    speaker = Speaker()
    session = Session()

    speaker.email = row["Email"]
    speaker.name = row["Given Name"] + " " + row["Family Name"]
    speaker.organisation = row["Company, Organization, Project or University"]
    speaker.web = row["Website or Blog"]

    if hasattr(speaker, 'photo'):
        speaker.photo = validate_result(
            parser.get_pic_url(row), speaker.photo, "URL")
    else:
        speaker.photo = parser.get_pic_url(row)

    speaker.linkedin = parser.get_linkedin_url(row)
    speaker.biography = row["Please provide a short bio for the program"]
    speaker.github = row["github"]
    speaker.twitter = row["twitter"]
    speaker.country = row["Country/Region of Origin"]

    # Start session
    session_time = parse_time(row["Date"] + " " + row["Time"])
    # print session_time
    # session.id = id_prefix
    
    if session_time is not None:
      session.start_time = session_time.isoformat()

    if last_session is not None and session_time is not None:
       last_session.end_time = session_time.isoformat()

    session.title = row["Topic or Name of proposed talk, workshop or project"]
    # session.subtitle = row["Field"]
    session.description = row["Abstract of talk or project"]
    session.type = row["Type"]

    # Use email more reliable
    if GLOBAL_SPEAKER_IDS.has_key(speaker.name):
        id = GLOBAL_SPEAKER_IDS[speaker.name].id
        speaker.id = id
    else:
        id = len(GLOBAL_SPEAKER_IDS.keys()) + 1
        speaker.id = id
        GLOBAL_SPEAKER_IDS[speaker.name] = speaker
        SPEAKERS.append(speaker)

    session.speakers = [{'name': speaker.name, 'id': speaker.id}]
    session.track = {'id': track.id, 'name': track.name}

    SESSIONS.append(session)
    return (speaker, session)
    # return (None, None)

DATE_FORMATS = ["%Y %A %B %d %I:%M %p", "%Y %A %B %d %I.%M %p"]


def parse_time(time_str):
    # Fix up year first, some of them may not have it
    iso_date = None
    if YEAR_OF_CONF not in time_str:
        time_str = YEAR_OF_CONF + " " + time_str

    print "parse_time " + time_str 

    for date_format in DATE_FORMATS:
        try:
            iso_date = datetime.datetime.strptime(time_str, date_format)
        except ValueError as e:
            pass
        else:
            break

    print iso_date

    return iso_date


def validate_result(current, default, type):
    """
    Validates the data, whether it needs to be url, twitter, linkedin link etc.
    """
    if current is None:
        current = ""
    if default is None:
        default = ""
    if type == "URL" and validators.url(current, require_tld=True) and not validators.url(default, require_tld=True):
        return current
    if type == "EMAIL" and validators.email(current) and not validators.email(default):
        return current
    return default


def write_json(filename, the_json):
    f = open(filename + '.json', 'w')
    the_json = simplejson.dumps(simplejson.loads(
        the_json), indent=2, sort_keys=False)
    json_to_write = '{ "%s":%s}' % (filename, the_json)
    f.write(json_to_write)
    f.close()

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    for track in TRACK_CONFIG:
        logging.info("[Parsing file] %s track_id = %d",
                     track.filename, track.id)
        parse_file(track)

    # print json.dumps(SPEAKERS[0].__dict__)
    speakers_json = jsonpickle.encode(SPEAKERS)
    write_json('speakers', speakers_json)
    session_json = jsonpickle.encode(SESSIONS)
    write_json('sessions', session_json)
    tracks_json = jsonpickle.encode(TRACK_CONFIG)
    write_json('tracks', tracks_json)
