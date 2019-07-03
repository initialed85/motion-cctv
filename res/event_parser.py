import datetime
import os
import re
import syslog
from collections import namedtuple

from config import TIMESTAMP_PATTERN, FILE_NAME_PATTERN, STYLE_SHEET, \
    HTML_TEMPLATE, HTML_REPEATER, HTML_SEPARATOR

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


def get_files(target_dir):
    files = []
    for file_name in os.listdir(target_dir):
        path = os.path.join(target_dir, file_name)
        if not os.path.isfile(path):
            continue

        if file_name.startswith('.'):
            continue

        stat = os.stat(path)

        try:
            file_size = round(stat.st_size / 1000000, 2)
        except Exception:
            file_size = None

        match = re.search(TIMESTAMP_PATTERN, file_name)
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


def parse_events(target_dir, browse_url_prefix, run_timestamp=None):
    run_timestamp = run_timestamp if run_timestamp is not None else datetime.datetime.now()

    files = get_files(target_dir)

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
        else:
            picture = get_empty_file('missing.png')

        if picture.timestamp is not None:  # case when movie is there but picture isn't after n tries
            if (picture.timestamp - movie.timestamp).total_seconds() > 60 * 60:  # ditch if over an hour's difference
                continue

        pairs += [(movie, picture)]

    events = []
    for movie, picture in pairs:
        match = re.search(
            FILE_NAME_PATTERN,
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
            '{}{}'.format(browse_url_prefix, picture.name),
            '{}{}'.format(browse_url_prefix, picture.name),
            picture.name,
            '{}{}'.format(browse_url_prefix, movie.name),
            '{}{}'.format(browse_url_prefix, movie.name)
        ]]

    repeaters = []
    last_timestamp = None
    for event in events:
        timestamp = event[2]
        date = datetime.datetime(year=timestamp.year, month=timestamp.month, day=timestamp.day)
        last_date = datetime.datetime(
            year=last_timestamp.year, month=last_timestamp.month, day=last_timestamp.day
        ) if last_timestamp is not None else None

        if last_date is None or last_date > date:
            repeaters += [HTML_SEPARATOR.format(
                date.strftime('%Y-%m-%d')
            )]

        last_timestamp = timestamp

        repeaters += [HTML_REPEATER.format(*event)]

    run_timestamp_str = run_timestamp.strftime('%Y-%m-%d %H:%M:%S')

    generated_html = HTML_TEMPLATE.format(
        run_timestamp_str,
        STYLE_SHEET,
        run_timestamp_str,
        '\n\n'.join(repeaters)
    ).strip()

    return generated_html


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 4:
        print('python event_parse.py [target_dir] [browse_url_prefix] [output_path]')

        sys.exit(1)

    target_dir = sys.argv[1]
    browse_url_prefix = sys.argv[2]
    output_path = sys.argv[3]

    html = parse_events(target_dir, browse_url_prefix)

    with open(output_path, 'w') as f:
        f.write(html)
