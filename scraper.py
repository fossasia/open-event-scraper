import csv
import json
# TODOS:
# 1. Multiple speakers
# 2. Sesion association

# Track config is filename, header
# Should have all track information
TRACK_CONFIG = [
('opentech.tsv', 2),
]

def parse_file(filename, header):
    HEADERS = []
    with open(filename) as tsv:
        i = 1
        for line in csv.reader(tsv, delimiter="\t"):
            if i == header:
                HEADERS = line
                print HEADERS
            elif i > header:
                #   parse_speaker
                result = create_associative_arr(line, HEADERS)
                parse_speaker(result)
                parse_session(result)
            i = i+1


def create_associative_arr(line, headers):
    result = dict(zip(headers, line))
    return result

SPEAKERS = []

def parse_speaker(result):
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
    if len(result["Email"]) > 1:
        speaker = Speaker()
        speaker.email = result["Email"]
        speaker.name = result["Given Name"] + " " + result["Family Name"]
        speaker.organisation = result["Organization"]
        speaker.web = result["Website or Blog"]
        speaker.photo = result["Photo for Website and Program"]
        speaker.linkedin = result["Linkedin"]
        speaker.biography = result["Please provide a short bio for the program"]
        speaker.github = result["github"]
        speaker.twitter = result["twitter"]
        speaker.country = result["Country/Region of Origin"]
        SPEAKERS.append(speaker)

def parse_session(result):
    pass

class Speaker(object):
    def __init__(self):
        super(Speaker, self).__init__()

class Session(object):
    def __init__(self):
        super(Session, self).__init__()

def write_json(filename, the_json):
    f = open(filename+'.json','w')
    json_to_write = '{ "%s":%s}' % (filename, the_json)
    f.write(json_to_write)
    f.close()

import jsonpickle
if __name__ == "__main__":
    for key,value in TRACK_CONFIG:
        parse_file(key, value)

    # print json.dumps(SPEAKERS[0].__dict__)
    speakers_json = jsonpickle.encode(SPEAKERS)
    write_json('speakers', speakers_json)
