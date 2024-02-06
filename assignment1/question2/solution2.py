import socket


def check_internet():
    try:
        host = socket.gethostbyname("www.google.com")
        socket.create_connection((host, 80), 2)
        return True
    except socket.error:
        return False


# Example usage
if check_internet():
    print("Internet Connectivity is present.")
else:
    print("No Internet Connectivity.")
