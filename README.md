# Tracking

Track stuff on a Raspberry Pi 4b!


## Install

- `git clone git@github.com:camoverride/tracking.git`
- `cd tracking`
- `python -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`


## Run

- `python display.py`


## Run in Production

Start a service with *systemd*. This will start the program when the computer starts and revive it when it dies. It expects that the username is `pi`:

- `mkdir -p ~/.config/systemd/user`
- `cat display.service > ~/.config/systemd/user/display.service`

Start the service using the commands below:

- `systemctl --user daemon-reload`
- `systemctl --user enable display.service`
- `systemctl --user start display.service`

Start it on boot: `sudo loginctl enable-linger pi`

Get the logs: `journalctl --user -u display.service`


## Increase System Longevity

Follow these steps in order:

- Install tailscale for remote access and debugging.
- Configure backup wifi networks.
- Set up periodic reboots (cron job)
- Set up Read-Only Filesystem.
