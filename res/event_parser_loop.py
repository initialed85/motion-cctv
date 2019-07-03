import datetime
import os
import time

from event_parser import parse_events

_PERIOD = 60

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 4:
        print('python event_parse.py [target_dir] [browse_url_prefix] [output_path]')

        sys.exit(1)

    _target_dir = sys.argv[1]
    _browse_url_prefix = sys.argv[2]
    _output_path = sys.argv[3]

    _period = datetime.timedelta(seconds=_PERIOD)

    while 1:
        try:
            _before = datetime.datetime.now()

            _htmls = parse_events(_target_dir, _browse_url_prefix)

            for _output_file, _html in _htmls.items():
                with open(os.path.join(_output_path, _output_file), 'w') as f:
                    f.write(_html)

            _after = datetime.datetime.now()

            _duration = _after - _before

            print('{}\ttook {} to generate HTML'.format(datetime.datetime.now(), _duration))

            _sleep_delta = _period - _duration

            _sleep_seconds = _sleep_delta.total_seconds()

            if _sleep_seconds > 0:
                print('{}\tsleeping for {}'.format(datetime.datetime.now(), _sleep_delta))
                time.sleep(_sleep_seconds)
            else:
                print('{}\tnot sleeping'.format(datetime.datetime.now()))
        except KeyboardInterrupt:
            break
