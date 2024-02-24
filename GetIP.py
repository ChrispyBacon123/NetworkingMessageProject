import socket

def get_ip_address():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Connect to a dummy server (Google's public DNS server)
        s.connect(("8.8.8.8", 80))
        
        # Get the socket's local address (which is your IP address)
        ip_address = s.getsockname()[0]
        
        return ip_address
    except Exception as e:
        print("Error:", e)
        return None

# Example usage:
ip_address = get_ip_address()
if ip_address:
    print("Your IP address is:", ip_address)
else:
    print("Failed to retrieve the IP address.")
