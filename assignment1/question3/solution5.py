import socket


def get_public_ip():
    return socket.gethostbyname(socket.gethostname())


# Example usage
public_ip = get_public_ip()
print("Your public IP address is:", public_ip)
