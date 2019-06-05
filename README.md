# motion-cctv
My implementation of Motion-Project/motion in Docker, including some scripts for ease of event integration.

## On licensing

My work in here is under the MIT license, so you can do with it what you will, even comercially if you like- however please note that Motion-Project/motion appears to be under under GPL-2.0 license.

## `motion` (the daemon)

### What's been done

- In the `configs` folder
    - Build a `motion.conf` for my use case
    - Build `camera1.conf`, `camera2.conf`, `camera3.conf` for my 3 x [Hikvision DS-2CD1H41WD-IZ](https://www.hikvision.com/au-en/Products/Network-Camera/Pro-Series(EasyIP)/EasyIP-3.0-Series/4MP/DS-2CD1H41WD-IZ) cameras
- In the `res` folder
    - Build `entrypoint.sh`
        - Generates a UUID that represents this "run" of `motion`

### How to use it

- Change to the appropriate folder
    - `cd motion_docker`
- Download the repo
    - `./get.sh`
- Build the image
    - `./build.sh`
- Run the instance in the foreground (NOTE: mounts `configs` and `target_dir` in the `motion_docker` folder)
    - `./run.sh`

If you want to run the instance in a more productionized way, I recommend you have a look at the contents of the `configs` folder and the contents of `run.sh` and tweak for your use case.

### How to integrate with it

Presently, the script `event_parser.py` looks at the contents of `target_dir` and knits a picture together in HTML form.
