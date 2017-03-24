import json, socket, subprocess, sys, configparser, jackserver

UDP_PORT = 10000
TCP_PORT = 10001

#TODO add ability for backend to send audio interfaces to frontend

def backend(s):
    """
    Handle the network communications between the GUI and this
    application.

    Begins by initiating a UDP server to listen for connections to
    send to a TCP server for reliable communications.

    s -- Socket information sent by the main process.

    Return the response sent to the GUI by the server.
    """
    #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.setblocking(0)
    #s.bind(('', UDP_PORT))
    #sock.bind(('', TCP_PORT))

    response = None

    #receive 1 byte message and send back to frontend
    data, wherefrom = s.recvfrom(1024)
    parsed_data = configparser.parse_json_data(data)
    if (parsed_data == "1")
        s.sendto(parsed_data, wherefrom)

    #TCP socket listens for frontend TCP socket to be created
    #then initiates TCP server that receieves JSON data
    sock.listen(1)
    c, addr = sock.accept()
       while True:
           data, wherefrom = sock.recvfrom(1024)
           parsed_data = configparser.parse_json_data(data)
           response = respond_to_intent(parsed_data)
           sock.sendto(response, wherefrom)
               if not data:
                   break
           c.send(data)
    c.close()
    else
        return response

#    response = None
#    try:
#        data, wherefrom = s.recvfrom(1024)
#        parsed_data = configparser.parse_json_data(data)
#
#        response = respond_to_intent(parsed_data)
#
#        s.sendto(response, wherefrom)
#    except socket.error:
#        pass
#    return response

def respond_to_intent(parsed_data):
    """
    Determine what action the GUI intends to perform.

    Reads the 'intent' data from the received data (as JSON) and
    performs the intended process dependent on the result of 'intent'

    parsed_data -- The data entire data message sent by the GUI

    Return the result of the actions performed to be sent to the GUI.
    """
    intent = parsed_data.pop('intent', None)
    if intent == 'EFFECT':
        # update the effects
        configparser.update_config_file(parsed_data)
        return 'Updated_effects'
    elif intent == 'REQPORT':
        # request the ports
        ports = {}
        ports['input'] = jackserver.get_clean_inports()
        ports['output'] = jackserver.get_clean_outports()
        ports_str = json.dumps(ports)
        return ports_str
    elif intent == 'UPDATEPORT':
        #update the ports
        return 'Updated_ports'
    else:
        return 'NO_INTENT'
    
if __name__ == '__main__':
    #USAGE bridge <frontend|backend>
    #run the frontend THEN the backend
    if sys.argv[1] == 'frontend':
        frontend(sys.stdin.read())
    elif sys.argv[1] == 'backend':
        sys.stdout.write(backend())

