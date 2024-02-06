import urllib.error
import urllib.request


def check_internet():
    try:
        urllib.request.urlopen('http://www.google.com', timeout=1)
        return True
    except urllib.error.URLError:
        return False


if check_internet():
    print("Internet Connectivity is present.")
else:
    print("No Internet Connectivity.")
