import socket

def find_available_udp_port():
    """
    Find an available UDP port by letting the OS assign one.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('', 0))  # Bind to any available port
        return s.getsockname()[1]  # Return the assigned port

# Example usage:
available_port = find_available_udp_port()
print(f"Available UDP port: {available_port}")



import socket

def is_port_available(port):
    """
    Check if a given port is available.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.bind(("127.0.0.1", port))    # change the IP address to the server's 
            return True
        except OSError:
            return False

# Example usage:
port_to_check = 12345  # Replace this with the port you want to check
if is_port_available(port_to_check):
    print(f"Port {port_to_check} is available.")
else:
    print(f"Port {port_to_check} is not available.")
