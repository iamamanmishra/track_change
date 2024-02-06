import requests


def get_public_ip():
    try:
        response = requests.get('https://ipinfo.io')
        ip_data = response.json()
        return ip_data['ip']
    except requests.RequestException as e:
        return str(e)


public_ip = get_public_ip()
print("Your public IP address is:", public_ip)
