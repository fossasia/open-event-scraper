import csv
import json
import datetime
import pytz
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

# We assume each row represents a time interval of 30 minutes and use that to calculate end time 
SESSION_LENGTH = datetime.timedelta(minutes=30)
TZ_UTC = pytz.utc
TZ_LOCAL = pytz.timezone('Asia/Hong_Kong')

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
    Track(id=1, name='Tech Kids I', 
            filename='data/TechKidsI.tsv',
            header_line=2,
            session_id_prefix=100,
            key_color="#3DC8C3",),

    Track(id=2, name='Tech Kids II', filename='data/TechKidsII.tsv',
           header_line=2,
           session_id_prefix=100,
           key_color="#3DC8C3",),

     Track(id=3, name='OpenTech and IoT', filename='data/opentech.tsv',
           header_line=2,
           session_id_prefix=100,
           key_color="#3DC8C3",),

     Track(id=4, name='OpenTech Workshops', filename='data/OpenTechWorkshops.tsv',
           header_line=2,
           session_id_prefix=100,
           key_color="#3DC8C3",),

     Track(id=5, name='WebTech', filename='data/WebTech.tsv',
           header_line=2,
           session_id_prefix=100,
           key_color="#3DC8C3",),

    #  Track(id=6, name='Exhibition', filename='data/exhibition.tsv',
    #        header_line=2,
    #        session_id_prefix=100,
    #        key_color="#3DC8C3",),

    #  Track(id=7, name='Hardware and IoT', filename='data/Hardware.tsv',
    #        header_line=2,
    #        session_id_prefix=100,
    #        key_color="#3DC8C3",),

    #  Track(id=8, name='Python', filename='data/python.tsv',
    #        header_line=2,
    #        session_id_prefix=100,
    #        key_color="#3DC8C3",),

    #  Track(id=9, name='Databases', filename='data/DB.tsv',
    #        header_line=2,
    #        session_id_prefix=100,
    #        key_color="#3DC8C3",),

    #  Track(id=10, name='Big Data/Open Data', filename='data/Data.tsv',
    #        header_line=2,
    #        session_id_prefix=100,
    #        key_color="#3DC8C3",),

    #  Track(id=11, name='DevOps', filename='data/devops.tsv',
    #        header_line=2,
    #        session_id_prefix=100,
    #        key_color="#3DC8C3",),

    #  Track(id=12, name='Privacy and Security', filename='data/Privacy-Security.tsv',
    #        header_line=2,
    #        session_id_prefix=100,
    #        key_color="#3DC8C3",),

    #  Track(id=13, name='Internet, Society, Community', filename='data/ISC.tsv',
    #        header_line=2,
    #        session_id_prefix=100,
    #        key_color="#3DC8C3",),

    #  Track(id=14, name='Science Hack Day', filename='data/ScienceHackDay.tsv',
    #        header_line=2,
    #        session_id_prefix=100,
    #        key_color="#3DC8C3",),

    #  Track(id=15, name='Linux and MiniDebConf', filename='data/Linux.tsv',
    #        header_line=2,
    #        session_id_prefix=100,
    #        key_color="#3DC8C3",),

    #  Track(id=16, name='Design, VR, 3D', filename='data/Design.tsv',
    #        header_line=2,
    #        session_id_prefix=100,
    #        key_color="#3DC8C3",)
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
                (res_speaker, res_session) = parse_row(row, speaker, session, track)

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

# Assume consequent rows with the same SessionID belong to the same session. 
# - Start time is taken from first row, end time from last row + 30 minutes. 
# - Title, description, etc. are taken from first row 
# - Speaker data on additional rows is appended to the speaker list for that session
# - Rows w/o SessionId are skipped
def parse_row(row, last_speaker, last_session, current_track):

    session_id = row["SessionID"]

    # no session id => skip row
    if not session_id:
        return (None, None)

    if last_session is None or last_session.session_id != session_id:
        session = Session()
        session.session_id = session_id
        session.speakers = []
        SESSIONS.append(session)
    else:
        session = last_session

    if row["Given Name"]:
        speaker = Speaker()
        SPEAKERS.append(speaker)

        speaker.organisation = row["Company, Organization, Project or University"]
        speaker.name = (row["Given Name"] + " " + row["Family Name"]).strip()
        speaker.web = row["Website or Blog"]
        speaker.linkedin = parser.get_linkedin_url(row)
        speaker.biography = row["Please provide a short bio for the program"]
        speaker.github = row["github"]
        speaker.twitter = row["twitter"]
        speaker.country = row["Country/Region of Origin"]

        if row["Email"]:
            speaker.email = row["Email"]

        if hasattr(speaker, 'photo'):
            speaker.photo = validate_result(
                parser.get_pic_url(row), 
                speaker.photo, 
                "URL"
            )
        else:
            speaker.photo = parser.get_pic_url(row)

            # Use email more reliable
        if GLOBAL_SPEAKER_IDS.has_key(speaker.name):
            id = GLOBAL_SPEAKER_IDS[speaker.name].id
            speaker.id = id
        else:
            id = len(GLOBAL_SPEAKER_IDS.keys()) + 1
            speaker.id = id
            GLOBAL_SPEAKER_IDS[speaker.name] = speaker
    else:
        speaker = None


    # set start time only the first time we encounter a session, but update end time for ever row
    # we encounter this session
    session_time = parse_time(row["Date"] + " " + row["Time"])
    if session_time is not None:
        session.end_time = (session_time + SESSION_LENGTH).isoformat() # TODO: +30 minutes
        if not hasattr(session, 'start_time'):
            session.start_time = session_time.isoformat()

    # only update attributes not already set
    if not hasattr(session, 'title'):
        session.title = row["Topic or Name of proposed talk, workshop or project"]
    if not hasattr(session, 'description'):
        session.description = row["Abstract of talk or project"]
    if not hasattr(session, 'type'):
        session.type = row["Type"]
    if not hasattr(session, 'track'):
        session.track = {'id': track.id, 'name': track.name}

    # TODO: append speaker
    if speaker is not None:
        session.speakers.append({'name': speaker.name, 'id': speaker.id})

    return (speaker, session)


DATE_FORMATS = ["%Y %A %B %d %I:%M %p", "%Y %A %B %d %I.%M %p"]

def parse_time(time_str):
    # Fix up year first, some of them may not have it
    iso_date = None
    if YEAR_OF_CONF not in time_str:
        time_str = YEAR_OF_CONF + " " + time_str

    for date_format in DATE_FORMATS:
        try:
            iso_date = datetime.datetime.strptime(time_str, date_format)
        except ValueError as e:
            pass
        else:
            break

    if iso_date is None:
        return None

    local_date = TZ_LOCAL.localize(iso_date)
    utc_date = local_date.astimezone(TZ_UTC)

    return utc_date


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


def write_json(filename, root_key, the_json):
    f = open(filename + '.json', 'w')
    the_json = simplejson.dumps(simplejson.loads(
        the_json), indent=2, sort_keys=False)
    json_to_write = '{ "%s":%s}' % (root_key, the_json)
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
    write_json('out/speakers', 'speakers', speakers_json)
    session_json = jsonpickle.encode(SESSIONS)
    write_json('out/sessions', 'sessions', session_json)
    tracks_json = jsonpickle.encode(TRACK_CONFIG)
    write_json('out/tracks', 'tracks', tracks_json)
