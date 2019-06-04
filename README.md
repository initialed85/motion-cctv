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
    - Build `handle_event.sh`
        - Log of the following `motion` concepts (by timestamp, event ID, camera ID and name etc):
            - `on_event_start` the opening of a motion event
            - `on_event_end` the closing of a motion event
            - `on_video_end` the point at which the video for an event is available 

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

My plan is for users to watch the contents of the `target_dir/event.log`, which a stream of events like this:

    2019-06-04 07:50:26.423517800+00:00,event_end,19,101,Driveway 2019-06-04,07:50:26,640,360,0,0,0
    2019-06-04 07:50:26.461321000+00:00,movie_end,19,101,Driveway 2019-06-04,07:50:26,640,360,0,0,0
    2019-06-04 07:50:36.331984100+00:00,event_start,20,101,Driveway 2019-06-04,07:50:35,640,360,44,20,704
    2019-06-04 07:50:51.393430700+00:00,event_end,20,101,Driveway 2019-06-04,07:50:51,640,360,0,0,0
    2019-06-04 07:50:51.468745700+00:00,movie_end,20,101,Driveway 2019-06-04,07:50:51,640,360,0,0,0
    2019-06-04 07:52:28.950499900+00:00,event_start,21,101,Driveway 2019-06-04,07:52:28,640,360,56,20,785
    2019-06-04 07:52:40.471305000+00:00,event_end,21,101,Driveway 2019-06-04,07:52:40,640,360,0,0,0
    2019-06-04 07:52:40.490868600+00:00,movie_end,21,101,Driveway 2019-06-04,07:52:40,640,360,0,0,0
    2019-06-04 07:52:57.435047400+00:00,event_start,22,101,Driveway 2019-06-04,07:52:57,640,360,30,40,843
    2019-06-04 07:53:16.478571700+00:00,event_end,22,101,Driveway 2019-06-04,07:53:16,640,360,0,0,0
    2019-06-04 07:53:16.575596500+00:00,movie_end,22,101,Driveway 2019-06-04,07:53:16,640,360,0,0,0

The columns correspond to the following:

- time when `handle_event.sh was called`
- event type
- event ID
- camera ID
- camera name
- event date (according to `motion`)
- event time (according to `motion`)
- event time (according to `motion`)
- image width
- image height
- motion width
- motion height
- changed pixels
- threshold

Some points to note:

- event ID seems to be unique to camera ID (so you can't treat event ID as unique on it's own)
- on shutdown of `motion`, all cameras seems to write an `event_end` (often in the absence of anything else)
- event IDs are recycled on runs of `motion`

So, in the voice of the micro-manager:

- consider the event ID and the camera ID together to be unique
- seek backwards, and throw away `event_end` events without any `event_start`
- make use of the `instance UUID` and `run UUID` I've included in the `event.log` to ensure you're not matching events for a now-shut-down instance of `motion`
