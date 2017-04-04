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

if [ "-nojack" == "$1" ]
then
    echo "nojack option enabled. Do not re-install jack"
else
    echo "Installing patched JACK."
    sudo apt-get --force-yes --yes remove jackd
    wget -O - http://rpi.autostatic.com/autostatic.gpg.key| sudo apt-key add -
    sudo wget -O /etc/apt/sources.list.d/autostatic-audio-raspbian.list http://rpi.autostatic.com/autostatic-audio-raspbian.list
    sudo apt-get update
    sudo apt-get --no-install-recommends --force-yes --yes install jackd
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

echo "Installation complete. PMEAS Ready for use."
