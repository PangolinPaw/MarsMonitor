# Mars Monitor

Computer vision system for the Raspberry Pi designed to read the progress information from an Elegoo Mars 5 screen.

## Installation

Clone this repo, then:

`pip install -r requirements.txt`

## Usage

### Hardware

The Raspberry Pi camera must be positioned directly in front of the printer's display at a distance that lets the camera focus.

Inside the `assets/` directory is an STL for a bracket that will hold a full-size Pi (i.e. not a Zero) and an official Raspberry Pi camera module and slot beneath the printer is provided:

![3D model of the bracket described above](https://github.com/PangolinPaw/MarsMonitor/blob/main/assets/bracket_render.png?raw=true)


### Software

Status update notifications use the https://ntfy.sh/ service. To receive notifications, install this on your mobile device and set up your custom topic (see https://docs.ntfy.sh/#step-1-get-the-app)

Edit the `config.json` file to include your topic URL

Then run the application with `python mars_monitor.py`

You may want to set `mars_monitor.py` to run automatically at boot, but nstructions on how to do this are beyond the scope of this document.

