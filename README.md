# Tracking

Track stuff!


## Requirements

Hardware requirements:

- Raspberry Pi 4b
- Google Coral TPU
- Webcam
- Monitor
- Power Supply

System requirements:

- Raspbian based off debian 10: Bookworm (legacy, 32-bit)
- Python 3.9


## Install

- `python3.9 -m venv .venv`
- `source .venv/bin/activate`
- `sudo apt-get install libopenblas-dev`
- `echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list`
- `curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -`
- `sudo apt-get update`
- `sudo apt-get install libedgetpu1-std`
- `sudo apt-get install python3-pycoral`

- `sudo apt-get install libjpeg-dev zlib1g-dev`


Test repo:

- `mkdir coral && cd coral`
- `git clone https://github.com/google-coral/pycoral.git`
- `cd pycoral`
- `bash examples/install_requirements.sh classify_image.py`
- `pip install numpy pillow pycoral`
- `sudo apt-get install python3-pandas`
- `pip install pycoral --no-deps`

```
python3 examples/classify_image.py \
--model test_data/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite \
--labels test_data/inat_bird_labels.txt \
--input test_data/parrot.jpg
```

Continue:

- `wget https://github.com/google-coral/edgetpu/raw/master/test_data/deeplabv3_mnv2_pascal_quant_edgetpu.tflite -P models/`


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
- Set up Read-Only Filesysyem.