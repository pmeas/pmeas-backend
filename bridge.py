import json, socket, subprocess, sys, configparser, jackserver

UDP_PORT = 10000
TCP_PORT = 10001

class Bridge:
    '''Bridge class is responsible for handling network communication in the app'''
    def __init__(self):
        self.TCP_CONN = False
        self.c = None
        self.addr = None

    def backend(self,s,sock):
        """
        Handle the network communications between the GUI and this
        application.

        Begins by initiating a UDP server to listen for connections to
        send to a TCP server for reliable communications.

        s -- UDP Socket information sent by the main process.
        sock -- TCP Socket information sent by the main process.

        Return the response sent to the GUI by the server.
        """
        response = None
        # Receive 1 byte message and send back to frontend
        # If there is already a connection, don't accept another one.
        if not self.TCP_CONN:
            try:
                data, wherefrom = s.recvfrom(1024)
                if data == "1":
                    print("Got a request")
                    s.sendto(str(TCP_PORT), wherefrom)
            except socket.error:
                pass
        
        #TCP socket listens for frontend TCP socket to be created
        #then initiates TCP server that receieves JSON data

        if not self.TCP_CONN:
            sock.listen(1)
            try:
                self.c, self.addr = sock.accept()
                if self.c is not None:
                    self.TCP_CONN = True
                    self.c.setblocking(0)
                print("Accepted connection from: " + str(self.addr))
            except socket.error:
                return


        # If there is a connection, see if there is data to be read.
        if self.TCP_CONN:
            try:
                data = self.c.recv(1024)
                print("Received data!" + data)
                # There is data to be read - see what the request is.
                parsed_data = configparser.parse_json_data(data)
                response = self.respond_to_intent(parsed_data)
                # Send back the result of the response.
                self.c.send(response[1] + "\n")
            except socket.error as error:
                pass
            except ValueError:
                self.TCP_CONN = False
                pass

        return response

    def respond_to_intent(self, parsed_data):
        """
        Determine what action the GUI intends to perform.

        Reads the 'intent' data from the received data (as JSON) and
        performs the intended process dependent on the result of 'intent'

        parsed_data -- The data entire data message sent by the GUI

        Return the result of the actions performed to be sent to the GUI.
        """
        intent = parsed_data.pop('intent', None)
        if intent == 'EFFECT':
            # The intent wants to add new effects.
            configparser.update_config_file(parsed_data)
            return (intent, intent)
        elif intent == 'REQPORT':
            # Intent wants to see what audio ports are available.
            ports = {}
            ports['input'] = jackserver.get_clean_inports()
            ports['output'] = jackserver.get_clean_outports()
            ports_str = json.dumps(ports)
            return (intent, ports_str)
        elif intent == 'UPDATEPORT':
            # Intent wants to set new audio ports (playback/capture)
            return (intent, parsed_data['in'], parsed_data['out'])
        else:
            return ()
        
