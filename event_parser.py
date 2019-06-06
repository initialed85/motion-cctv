import datetime
import os
import re
import sys
import syslog
import time
import traceback
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
<td style="width: 320px";><a target="_blank" href="{}"><img src="{}" alt="{}" width="320" height="180" /></a></td>
<td><a href="{}">Download</a></td>
</tr>"""

File = namedtuple('File', ['size', 'name', 'prefix', 'timestamp'])


class FailedToFindPictureError(Exception):
    pass


def _log(level, priority, message):
    message = repr(message).rstrip()

    print('{}: {}'.format(
        level,
        message
    ))

    syslog.syslog(priority, message)


def info(message):
    _log('info', syslog.LOG_INFO, message)


def error(message):
    _log('error', syslog.LOG_INFO, message)


def get_empty_file(name):
    return File(None, name, None, None)


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
            file_size = round(stat.st_size / 1000000, 2)
        except Exception:
            file_size = None

        match = re.search('.*(\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d).*', file_name)
        if match is None:
            continue

        groups = match.groups()
        if groups is None or len(groups) == 0:
            continue

        timestamp = datetime.datetime.strptime(groups[0], '%Y-%m-%d_%H-%M-%S')

        file_obj = File(
            file_size,
            file_name,
            '__'.join(file_name.split('__')[0:2]),
            timestamp
        )

        files += [file_obj]

    sorted_files = sorted([(x.timestamp, x) for x in files])[::-1]

    return [x[1] for x in sorted_files]


def get_movies(files):
    return [x for x in files if x.name.endswith('.mkv')]


def get_pictures(files):
    return [x for x in files if x.name.endswith('.jpg')]


def work(handle_missing):
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

        if picture is not None:
            pictures.pop(i)
        elif handle_missing:
            error('failed to find picture for {}; will stub out'.format(movie.name))
            picture = get_empty_file('missing.png')
        else:
            message = 'failed to find picture for {}; will try again'.format(movie.name)
            error(message)
            raise FailedToFindPictureError(message)

        pairs += [(movie, picture)]

    events = []
    for movie, picture in pairs:
        match = re.search(
            '(\d+)__(\d+)__\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d__(.*)\.',
            movie.name
        )

        if match is None:
            error('failed to regex parts out of {}; will skip'.format(repr(movie)))
            continue

        event_id, camera_id, camera_name = match.groups()

        events += [[
            event_id,
            camera_id,
            movie.timestamp,
            '{} MB'.format(movie.size) if movie.size is not None else 'unknown',
            camera_name,
            '{}{}'.format(_BROWSE_URL_PREFIX, picture.name),
            '{}{}'.format(_BROWSE_URL_PREFIX, picture.name),
            picture.name,
            '{}{}'.format(_BROWSE_URL_PREFIX, movie.name)
        ]]

    repeaters = []
    last_timestamp = None
    for event in events:
        timestamp = event[2]
        date = datetime.datetime(year=timestamp.year, month=timestamp.month, day=timestamp.day)

        if last_timestamp is None:
            repeaters += ['<tr><th colspan="8" style="background-color: silver;">{}</th></tr>'.format(
                date.strftime('%Y-%m-%d')
            )]
        else:
            last_date = datetime.datetime(year=last_timestamp.year, month=last_timestamp.month, day=last_timestamp.day)
            if last_date < date:
                repeaters += ['<tr><th colspan="8" style="background-color: silver;">{}</th></tr>'.format(
                    date.strftime('%Y-%m-%d')
                )]

        last_timestamp = timestamp

        repeaters += [_HTML_REPEATER.format(*event)]

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(sys.argv[1], 'w') as f:
        f.write(_HTML_TEMPLATE.format(
            now,
            _STYLE_SHEET,
            now,
            '\n\n'.join(repeaters)
        ))


if __name__ == '__main__':
    success = False
    for i in range(0, 5):
        before = datetime.datetime.now()

        try:
            work(not i < 4)

            success = True

            break
        except Exception as e:
            if not isinstance(e, FailedToFindPictureError):
                error(traceback.format_exc())

        after = datetime.datetime.now()

        duration = after - before

        sleep = datetime.timedelta(seconds=5) - duration

        if duration > datetime.timedelta(seconds=0):
            time.sleep(sleep.total_seconds())

    if not success:
        raise SystemExit('all attempts failed')
