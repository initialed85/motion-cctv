import datetime
import time

from event_parser import parse_events

_PERIOD = 60

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 4:
        print('python event_parse.py [target_dir] [browse_url_prefix] [output_path]')

        sys.exit(1)

    target_dir = sys.argv[1]
    browse_url_prefix = sys.argv[2]
    output_path = sys.argv[3]

    period = datetime.timedelta(seconds=_PERIOD)

    while 1:
        before = datetime.datetime.now()

        html = parse_events(target_dir, browse_url_prefix)
        with open(output_path, 'w') as f:
            f.write(html)

        after = datetime.datetime.now()

        duration = after - before

        print('{}\ttook {} to generate HTML'.format(datetime.datetime.now(), duration))

        sleep_delta = period - duration

        sleep_seconds = sleep_delta.total_seconds()

        if sleep_seconds > 0:
            print('{}\tsleeping for {}'.format(datetime.datetime.now(), sleep_delta))
            time.sleep(sleep_seconds)
        else:
            print('{}\tnot sleeping'.format(datetime.datetime.now()))
