import os
import subprocess


def start_jack_server(hw_in_port='0', hw_out_port='0'):
    """
    Start the JACK server.

    Keyword arguments:
    inputport -- the port on which to listen for audio data
    outputport -- the port on which to send audio data to.

    Called ONLY when no existing JACK server is running on the machine.
    """
    PATH = "jack/jackd"

    if os.uname()[4].startswith("arm"):
        PATH = "jack/arm/jackd"

    jack_dir = os.path.join( os.path.dirname(os.path.abspath(__file__)), PATH)

    #cmd = 'jackd -P 70 -d alsa -r 48000 -p 512 -n 4 -D -C hw:{0} -P hw:{1} &'.format(hw_in_port, hw_out_port)
    cmd = [jack_dir, '-P', '70', '-t', '2000', '-d', 'alsa', '-r', '48000', '-p', '512', '-n', '4', '-D', '-C', 'hw:'+hw_in_port, '-P', 'hw:'+hw_out_port, '-s', '&']
    process = subprocess.Popen(cmd, shell=False)
    proc_id = process.pid
    print("ID OF JACK (supposedly): " + str(proc_id))
    return proc_id

def kill_jack_server(jack_id):
    '''it kills the jack server. this one isn't as nice as "stop" but it's more reliable'''
    cmd = ['kill', '-s', '9', str(jack_id)]
    process = subprocess.Popen(cmd, shell=False)

def stop_jack_server():
    '''this is the "correct" way to stop jack, but we were having issues with it so instead we workaround with kill_jack_server'''
    cmd = ['jack_control', 'stop']
    process = subprocess.Popen(cmd, shell=False)

def get_input_devices():
    """List the input devices captured by the ALSA interface"""
    process = subprocess.Popen(['arecord', '-l'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    return out


def get_output_devices():
    """List the output devices captured by the ALSA interface"""
    process = subprocess.Popen(['aplay', '-l'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    return out


def filter_shell_output(data):
    """
    Return only the data that identifies what ports are being used

    data -- the output from the call to either
            aplay or arecord.

    Returns a list of strings corresponding to the used ports
    """
    sound_devices = []
    data_arr = data.split("\n")
    for line in data_arr:
        if 'card' in line:
            sound_devices.append(line)
    return sound_devices


def filter_port_selection(selected_port):
    """
    Filter the port data received from the GUI.

    Will extract the card number and device number to allow
    JACK to identify the port selected and lock them for use.

    selected_port -- The raw data received from the GUI application

    Return the port selected formatted for JACK - hw:card,device
    """
    card_start = selected_port.find('card')
    card_port_start = card_start + len('card ')
    device_start = selected_port.find('device', card_start)
    device_port_start = device_start + len('device ')
    card_port_end = selected_port.rfind(':', card_port_start, device_start)
    device_port_end = selected_port.rfind(':', device_port_start)
    result = selected_port[card_port_start:card_port_end] + "," + selected_port[device_port_start:device_port_end]
    print('filter_port_selection({0}) => {1}'.format(selected_port, result))
    return result
    #print(str(card_num) + ", " + str(device_num))

def get_clean_inports():
    """
    Return the filtered input ports
    """
    arecord_res = get_input_devices()
    return filter_shell_output(arecord_res)

def get_clean_outports():
    """
    Return the filtered output ports
    """
    aplay_res = get_output_devices()
    return filter_shell_output(aplay_res)

