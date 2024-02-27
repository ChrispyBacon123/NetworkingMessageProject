def find_avail_port(portNum):
    """Find an available port"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1',portNum))
    if result == 0:
       print "Port is open"
       return True
    else:
       print "Port is not open"
       return False
    sock.close()
