import requests


def get_public_ip():
    try:
        # Use a public IP address API to get your public IP
        response = requests.get('https://api64.ipify.org?format=json')
        ip_data = response.json()
        return ip_data['ip']
    except requests.RequestException as e:
        return str(e)


public_ip = get_public_ip()
print("Your public IP address is:", public_ip)
