import platform
import subprocess


def check_internet():
    system_platform = platform.system().lower()

    if system_platform == "windows":
        try:
            subprocess.run(["ping", "-n", "1", "www.google.com"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    elif system_platform == "darwin" or system_platform == "linux":
        try:
            subprocess.run(["ping", "-c", "1", "www.google.com"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    else:
        # Unsupported platform
        return False


# Example usage
if check_internet():
    print("Internet Connectivity is present.")
else:
    print("No Internet Connectivity.")
