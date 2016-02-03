class Track(object):
    id = 0
    header_line = 1
    filename = ""
    session_id_prefix = 10
    key_color = "#FF4D55"
    name = ""
    description = ""
    track_image_url = "http://lorempixel.com/400/200"

    def __init__(self, id, header_line, filename, session_id_prefix, key_color):
        super(Track, self).__init__()
        self.id = id
        self.header_line = header_line
        self.filename = filename
        self.session_id_prefix = session_id_prefix
        self.key_color = key_color
        self.track_image_url = "http://lorempixel.com/400/200"


class Speaker(object):

    def __init__(self):
        super(Speaker, self).__init__()


class Session(object):

    def __init__(self):
        super(Session, self).__init__()
