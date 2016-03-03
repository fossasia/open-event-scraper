class Track(object):
    id = 0
    header_line = 1
    filename = ""
    key_color = "#FF4D55"
    name = ""
    description = ""
    track_image_url = "http://lorempixel.com/400/200"

    def __init__(self, id, name, header_line, filename, key_color):
        super(Track, self).__init__()
        self.id = id
        self.name = name
        self.header_line = header_line
        self.filename = filename
        self.key_color = key_color
        self.track_image_url = "http://lorempixel.com/400/200"


class Speaker(object):

    def __init__(self):
        super(Speaker, self).__init__()


class Session(object):

    def __init__(self):
        super(Session, self).__init__()


class Microlocation(object):

    def __init__(self):
        super(Microlocation, self).__init__()
