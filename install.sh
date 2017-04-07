#!/bin/bash
# Installer script for the backend application.
# Ensures the proper dependencies are installed to
# ensure successfull run of the application. Should be 
# run BEFORE running the modulator application - unless
# you are sure the dependencies are already installed (run this
# anyways just in case)

PYO_PKG_INSTALLED=$(dpkg-query -W --showformat='${Status}\n' python-pyo|grep "install ok installed")
JACK_PKG_INSTALLED=$(dpkg-query -W --showformat='${Status}\n' jackd|grep "install ok installed")

# Checks for ALSA package. Works for Ubuntu systems - has to be tested for other distros.
ALSA_PKG_INSTALLED=$(cat /proc/asound/version|grep "Advanced Linux Sound Architecture")

# Checks for ALSA installation. If not, print message + exit.
if [ "" == "$ALSA_PKG_INSTALLED" ]
then
    echo "ALSA not installed. Could not proceed with installation."
    exit 0
    echo "[OK]"
fi

# Check for successful Pyo installation. If not, force install.
if [ "" == "$PYO_PKG_INSTALLED" ]
then
    echo "Could not find Pyo installation. Installing Pyo."
    sudo apt-get --force-yes --yes install python-pyo
    # Code to install Pyo here
    echo "[OK]"
fi

echo "Setting up systemd service"
printf "[Unit]\nDescription=PMEAS Audio System\n\n[Service]\nType=forking\nExecStart=/bin/bash $PWD/pmeas.sh\nRestart=on-abort\n\n[Install]\nWantedBy=multi-user.target" > /etc/systemd/system/pmeas.service
sudo systemctl enable pmeas.service
printf "Systemd service successfully registered\n"

printf "Creating bash startup script\n"
printf "#/bin/bash\n\npython $PWD &" > pmeas.sh
printf "Bash script successfully created\n"

echo "Installation complete. PMEAS Ready for use."
