# powerdown
Python Flask app to power down a linux computer.

## Usage
1. Install Flask framework:

    `pip3 install flask`

2. Make app executable

    `chmod +x ./powerdown.py`

3. Run the app with elevated privileges:

    `sudo ./powerdown.py`

## Simpler way
Run 

   `./install.sh"` 

to install virtual environment and Flask library. 
It will also create a file in sudoers.d to allow "shutdown" to be run without elevated privileges.
After this run:

   `./powerdown.sh`

This will run the python script from venv.

## Powering down your computer

From another device, use the web browser to navigate to your computers IP at port 5000.
