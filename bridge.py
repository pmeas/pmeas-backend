import json, socket, subprocess, sys, configparser

PORT = 10000

#TODO add ability for backend to send audio interfaces to frontend

def backend(timeout=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', PORT))

    # I dont like this because it blocks -> we'll see if we need to keep listening for same messages
    data, wherefrom = s.recvfrom(1500, 0)
    configparser.update_config_file(data)
    s.sendto('received', wherefrom)

if __name__ == '__main__':
    #USAGE bridge <frontend|backend>
    #run the frontend THEN the backend
    if sys.argv[1] == 'frontend':
        frontend(sys.stdin.read())
    elif sys.argv[1] == 'backend':
        sys.stdout.write(backend())

