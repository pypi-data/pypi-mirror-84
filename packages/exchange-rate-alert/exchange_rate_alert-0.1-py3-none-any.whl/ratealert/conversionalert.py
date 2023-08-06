import json
import time
from sys import platform
from ratealert.transferwiseclient import TransferwiseClient
from ratealert.auth.linuxauth import LinuxAuth
from ratealert.auth.windowsauth import WindowsAuth
from ratealert.notification.linuxnotification import LinuxNotification
from ratealert.notification.windowsnotification import WindowsNotification


class ConversionAlert(object):

    def __init__(self, source, target):
        """
        Checks the transfer rate and creates an alert on demand

        :param source: source currency
        :param target: target currency
        """
        self._thread = None
        self.set_alert(source, target)

    def __init__(self, source, target, interval):
        """
        Creates a transfer alert which polls at the interval
        :param source: source currency
        :param target: target currency
        :param interval: interval for polling
        """
        self._thread = None
        self.set_alert(source, target)
        try:
            while True:
                self.set_alert(source, target)
                time.sleep(int(interval))
        except KeyboardInterrupt:
            exit(0)
        except InterruptedError:
            exit(0)

    def set_alert(self, source, target):
        """Displays a notification on the desktop with the conversion rate

        :param source: Source currency
        :param target: Target currency
        :return: None
        """

        client = TransferwiseClient()

        authentication, notification = _identify_platform()

        try:
            token = client.load_auth_token(authentication)
        except FileNotFoundError:
            print('Unable to find a bearer token. Exiting.')
            print("""The program will try and find the access token in the following manner
                     1. System Variable named TCR
                     2. Configuration file - located at ~/.tcr on linux or %HOMEDRIVE%%HOMEPATH%/.tcr on windows""")
            exit()

        response = client.get_conversion_rate(source, target, token)
        parsed_response = _handle_response(response)
        notification.set_notification(parsed_response)


def _handle_response(response):
    json_response = json.loads(response.content.decode('utf8'))[0]
    return json_response


def _identify_platform():
    """Identifies the system OS"""
    if platform == "linux" or platform == "linux2":
        return LinuxAuth(), LinuxNotification()
    elif platform == "win32":
        return WindowsAuth(), WindowsNotification()


