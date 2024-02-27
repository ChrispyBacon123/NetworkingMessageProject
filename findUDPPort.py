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
