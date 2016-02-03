import csv
import json
import datetime
import simplejson
import validators
from models import *

# TODOS:
# 1. Multiple speakers
# 2. Sesion association

# Track config is filename, header
# Should have all track information
# ID Prefix = should be unique across tracks
# Color code
TRACK_CONFIG = [
    Track(id=1, name='Open Technologies', filename='opentech.tsv',
          header_line=2,
          session_id_prefix=100,
          key_color="#3DC8C3",),

    Track(id=2, name='DevOps', filename='devops.tsv',
          header_line=2,
          session_id_prefix=200,
          key_color="#3DC8CC",),

    Track(id=3, name='Exhibition', filename='exhibition.tsv',
          header_line=1,
          session_id_prefix=300,
          key_color="#3DC8FF",),
]

# Provide year of conference in case the date is impossible to parse
YEAR_OF_CONF = '2015'


def parse_file(track):
    HEADERS = []
    with open(track.filename) as tsv:
        i = 1
        speaker = None
        session = None
        for line in csv.reader(tsv, delimiter="\t"):
            if i == track.header_line:
                HEADERS = line
                print HEADERS
            elif i > track.header_line:
                #   parse_speaker
                result = create_associative_arr(line, HEADERS)
                (res_speaker, res_session) = parse_speaker(result,  speaker,
                                                           session, track, track.session_id_prefix + (10 * i),)
                if res_session is not None and res_speaker is not None:
                    speaker = res_speaker
                    session = res_session
                parse_session(result)
            i = i + 1


def create_associative_arr(line, headers):
    result = dict(zip(headers, line))
    return result

SPEAKERS = []
SESSIONS = []

GLOBAL_SPEAKER_IDS = {}


def parse_speaker(result,  last_speaker, last_session, current_track, id_prefix=10,):
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
    if result.has_key("Email") and len(result["Email"]) > 1:
        if GLOBAL_SPEAKER_IDS.has_key(result["Email"]) is not True:
            speaker = Speaker()
        else:
            speaker = GLOBAL_SPEAKER_IDS[result["Email"]]
        session = Session()
        speaker.email = result["Email"]
        speaker.name = result["Given Name"] + " " + result["Family Name"]
        speaker.organisation = result["Organization"]
        speaker.web = result["Website or Blog"]
        if hasattr(speaker, 'photo'):
            speaker.photo = validate_result(
                result["Photo for Website and Program"], speaker.photo, "URL")
        else:
            speaker.photo = result["Photo for Website and Program"]
        speaker.linkedin = result["Linkedin"]
        speaker.biography = result[
            "Please provide a short bio for the program"]
        speaker.github = result["github"]
        speaker.twitter = result["twitter"]
        speaker.country = result["Country/Region of Origin"]
        # Start session
        session_time = parse_time(result["Date"] + " " + result["Time"])
        session.id = id_prefix
        session.start_time = session_time.isoformat()
        if last_session is not None:
            last_session.end_time = session.start_time
        session.title = result["Session Topic"]
        session.subtitle = result["Field"]
        session.description = result["Abstract of talk or project"]
        session.type = result["Type"]
        # Use email more reliable
        if GLOBAL_SPEAKER_IDS.has_key(speaker.email):
            id = GLOBAL_SPEAKER_IDS[speaker.email].id
            speaker.id = id
        else:
            id = len(GLOBAL_SPEAKER_IDS.keys()) + 1
            speaker.id = id
            GLOBAL_SPEAKER_IDS[speaker.email] = speaker
            SPEAKERS.append(speaker)

        session.speakers = [{'name': speaker.name, 'id': speaker.id}]
        session.track = {'id': track.id, 'name': track.name}
        SESSIONS.append(session)
        return (speaker, session)
    return (None, None)

DATE_FORMATS = ["%Y %A %B %d %I:%M %p", "%Y %A %B %d %I.%M %p"]


def parse_time(time_str):
    # Fix up year first, some of them may not have it
    if YEAR_OF_CONF not in time_str:
        time_str = YEAR_OF_CONF + " " + time_str
    for date_format in DATE_FORMATS:
        try:
            iso_date = datetime.datetime.strptime(time_str, date_format)
        except ValueError as e:
            pass
        else:
            break
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
    return default


def parse_session(result):
    pass


def write_json(filename, the_json):
    f = open(filename + '.json', 'w')
    the_json = simplejson.dumps(simplejson.loads(
        the_json), indent=2, sort_keys=False)
    json_to_write = '{ "%s":%s}' % (filename, the_json)
    f.write(json_to_write)
    f.close()

import jsonpickle
if __name__ == "__main__":
    for track in TRACK_CONFIG:
        print jsonpickle.encode(track)
        parse_file(track)

    # print json.dumps(SPEAKERS[0].__dict__)
    speakers_json = jsonpickle.encode(SPEAKERS)
    write_json('speakers', speakers_json)
    session_json = jsonpickle.encode(SESSIONS)
    write_json('sessions', session_json)
    tracks_json = jsonpickle.encode(TRACK_CONFIG)
    write_json('tracks', tracks_json)
