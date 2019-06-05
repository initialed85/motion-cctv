import datetime
import os
import re
import sys
from collections import namedtuple

_TARGET_DIR = '/media/storage/Cameras'

_BROWSE_URL_PREFIX = '/browse/'

_STYLE_SHEET = """
BODY {
    font-family: Tahoma;
    font-size: 8pt;
    font-weight: none;
    text-align: center;
}

TH {
    font-family: Tahoma;
    font-size: 8pt;
    font-weight: bold;
    text-align: center;
}

TD {
    font-family: Tahoma;
    font-size: 8pt;
    font-weight: none;
    text-align: center;
    border: 1px solid gray; 
}
"""

_HTML_TEMPLATE = """</html>
<head>
<title>Events as at {}</title>
<style type="text/css">
{}
</style>
</head>

<body>
<h1>Events as at {}</h1>

<center>
<table width="90%">

<tr>
<th>Event ID</th>
<th>Camera ID</th>
<th>Timestamp</th>
<th>Duration</th>
<th>Size</th>
<th>Camera</th>
<th>Screenshot</th>
<th>Clip</th>
</tr>

{}

</table>
<center>

</body>
</html>
"""

_HTML_REPEATER = """<tr>
<td>{}</td>
<td>{}</td>
<td>{}</td>
<td>{}</td>
<td>{}</td>
<td>{}</td>
<td><a target="_blank" href="{}"><img src="{}" alt="{}" width="320" height="180" /></a></td>
<td><a href="{}">Download</a></td>
</tr>"""

File = namedtuple('File', ['created', 'modified', 'size', 'name', 'prefix'])


def get_files():
    files = []
    for file_name in os.listdir(_TARGET_DIR):
        path = os.path.join(_TARGET_DIR, file_name)
        if not os.path.isfile(path):
            continue

        if file_name.startswith('.'):
            continue

        stat = os.stat(path)

        try:
            created = datetime.datetime.fromtimestamp(stat.st_birthtime)
        except Exception:
            created = None

        try:
            modified = datetime.datetime.fromtimestamp(stat.st_mtime)
        except Exception:
            modified = None

        try:
            file_size = round(stat.st_size / 1000000, 2)
        except Exception:
            file_size = None

        file_obj = File(created, modified, file_size, file_name, '__'.join(file_name.split('__')[0:2]))

        files += [(created, modified, file_obj)]

    return [x[2] for x in sorted(files)[::-1]]


def get_movies(files):
    return [x for x in files if x.name.endswith('.mkv')]


def get_pictures(files):
    return [x for x in files if x.name.endswith('.jpg')]


files = get_files()

movies = get_movies(files)

pictures = get_pictures(files)

pairs = []
while len(movies) > 0:
    movie = movies.pop(0)

    i = None
    picture = None

    for i, picture in enumerate(pictures):
        if picture.prefix == movie.prefix:
            break

    if picture is None:
        raise ValueError('failed to find picture for {}'.format(movie))

    pictures.pop(i)

    pairs += [(movie, picture)]

events = []
for movie, picture in pairs:
    duration = movie.modified - movie.created if movie.created is not None not in [
        movie.modified, movie.created
    ] else 'unknown'

    match = re.search(
        '(\d+)__(\d+)__(\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d)__(.*)\.',
        movie.name
    )

    if match is None:
        raise ValueError('failed to regex parts out of {}'.format(repr(movie)))

    event_id, camera_id, timestamp_str, camera_name = match.groups()

    timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d_%H-%M-%S')

    events += [[
        event_id,
        camera_id,
        timestamp,
        duration,
        '{} MB'.format(movie.size) if movie.size is not None else 'unknown',
        camera_name,
        '{}{}'.format(_BROWSE_URL_PREFIX, picture.name),
        '{}{}'.format(_BROWSE_URL_PREFIX, picture.name),
        picture.name,
        '{}{}'.format(_BROWSE_URL_PREFIX, movie.name)
    ]]

repeaters = []
for event in events:
    repeaters += [_HTML_REPEATER.format(*event)]

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

with open(sys.argv[1], 'w') as f:
    f.write(_HTML_TEMPLATE.format(
        now,
        _STYLE_SHEET,
        now,
        '\n\n'.join(repeaters)
    ))
