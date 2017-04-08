import json, socket, subprocess, sys, configparser, jackserver

UDP_PORT = 10000
TCP_PORT = 10001

#TODO add ability for backend to send audio interfaces to frontend
class Bridge:
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
        #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.setblocking(0)
        #s.bind(('', UDP_PORT))
        #sock.bind(('', TCP_PORT))
        
        response = None
        #receive 1 byte message and send back to frontend
        if not self.TCP_CONN:
            try:
                data, wherefrom = s.recvfrom(1024)
                if data == "1":
                    print("Got a 1")
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
                print("Accepted connection from: " + str(self.addr))
            except socket.error:
                return
        
        if self.TCP_CONN:
            try:
                data = self.c.recv(1024)
                print("Received data!" + data)
                parsed_data = configparser.parse_json_data(data)
                response = self.respond_to_intent(parsed_data)
                self.c.send(response[1])
            except socket.error as error:
                print("Caught an error" + str(error))
            except ValueError:
                self.TCP_CONN = False
                pass

        return response
        """
        response = None
        try:
            data, wherefrom = s.recvfrom(1024)
            parsed_data = configparser.parse_json_data(data)

            response = respond_to_intent(parsed_data)

            s.sendto(response, wherefrom)
        except socket.error:
            pass
        return response
        """

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
            # update the effects
            configparser.update_config_file(parsed_data)
            return (intent, intent)
        elif intent == 'REQPORT':
            # request the ports
            ports = {}
            ports['input'] = jackserver.get_clean_inports()
            ports['output'] = jackserver.get_clean_outports()
            ports_str = json.dumps(ports)
            return (intent, ports_str)
        elif intent == 'UPDATEPORT':
            #update the ports
            return (intent, parsed_data['in'], parsed_data['out'])
        else:
            return ()
        
if __name__ == '__main__':
    #USAGE bridge <frontend|backend>
    #run the frontend THEN the backend
    if sys.argv[1] == 'frontend':
        frontend(sys.stdin.read())
    elif sys.argv[1] == 'backend':
        sys.stdout.write(backend())

