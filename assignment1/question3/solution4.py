import socket


def get_public_ip():
    try:
        # Open a socket to a dummy server (does not actually make a connection)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("10.0.0.1", 1))  # Connect to a dummy IP address
            public_ip = s.getsockname()[0]
        return public_ip
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    public_ip = get_public_ip()
    if public_ip:
        print("Your public IP address is:", public_ip)
