# motion-cctv
My implementation of Motion-Project/motion in Docker, including some scripts for ease of event integration.

## On licensing

My work in here is under the MIT license, so you can do with it what you will, even comercially if you like- however please note that Motion-Project/motion appears to be under under GPL-2.0 license which will likely limit your ability to do that.

### Overview

A running instance of `motion-cctv` consists of the following:

- A [Docker](https://www.docker.com/) container with a [Supervisor](http://supervisord.org/) entrypoint, managing:
    - [nginx](https://www.nginx.com/)
    - [motion](https://github.com/Motion-Project/motion)
    - `event_parser_loop.py`
    - [logrotate](https://linux.die.net/man/8/logrotate) 

### What's been done

- In the `configs` folder
    - `motion.conf`
        - a basic configuration that suits my use case
    - `camera1.conf`, `camera2.conf`, `camera3.conf`
        - configurations for my 3 x [Hikvision DS-2CD1H41WD-IZ](https://www.hikvision.com/au-en/Products/Network-Camera/Pro-Series(EasyIP)/EasyIP-3.0-Series/4MP/DS-2CD1H41WD-IZ) cameras
- In the `res` folder
    - `config.py`
        - HTML templates for `event_parser.py`
    - `event_parser.py`
        - parses pictures and movies from `target_dir` and builds `events.html`
    - `event_parser_loop.py`
        - runs `event_parser.py` on a 60-second loop
    - `event_parser_test.py`
        - unit tests for `event_parser.py`
    - `index.html`
        - landing page
    - `motion-cctv.conf`
        - `supervisor` configuration for all the processes
    - `nginx.conf`
        - `nginx` web server configuration

### How to use it

- Define your `cameraN.conf` files
- Adjust `motion.conf` to suit
- Download the repo
    - `./get.sh`
- Build the image
    - `./build.sh`
- Run the instance in the foreground (you'll likely need to adjust the volumes)
    - `./run.sh`
- Browse to [http://localhost](http://localhost) and have a click around

If you want to run the instance in a more productionized way then `run_in_background.sh` shows a suitable example (but again, you'll need to adjust the volumes).
