import datetime
import os
import re
import sys
from itertools import zip_longest

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
<td><img src="{}" width="320" height="180" /></td>
<td><a href="{}">Download</a></td>
</tr>"""


def get_movies():
    files = []
    for file_name in os.listdir(_TARGET_DIR):
        path = os.path.join(_TARGET_DIR, file_name)
        if not os.path.isfile(path):
            continue

        if file_name.startswith('.'):
            continue

        if not file_name.endswith('.mkv'):
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

        files += [
            (
                created,
                modified,
                file_size,
                file_name,
            )
        ]

    return files


def get_pictures():
    return [
        x for x in os.listdir(_TARGET_DIR) if x.endswith('.jpg') and not x.startswith('.')
    ]


movies = get_movies()

pictures = get_pictures()

events = []
for (created, last_modified, file_size, movie), picture in zip_longest(movies, pictures):
    duration = last_modified - created if created is not None not in [last_modified, created] else 'unknown'

    match = re.search(
        '(\d+)__(\d+)__(\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d)__(.*)\.',
        movie
    )

    if match is None:
        raise ValueError('failed to match {}'.format(repr(movie)))

    event_id, camera_id, timestamp_str, camera_name = match.groups()

    timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d_%H-%M-%S')

    events += [[
        event_id,
        camera_id,
        timestamp,
        duration,
        '{} MB'.format(file_size) if file_size is not None else 'unknown',
        camera_name,
        '{}{}'.format(_BROWSE_URL_PREFIX, picture),
        '{}{}'.format(_BROWSE_URL_PREFIX, movie)
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

