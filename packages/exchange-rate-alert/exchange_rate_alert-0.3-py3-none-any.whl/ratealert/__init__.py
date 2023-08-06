import json
import time
from sys import platform
from ratealert.transferwiseclient import TransferwiseClient
from ratealert.auth.linuxauth import LinuxAuth
from ratealert.auth.windowsauth import WindowsAuth
from ratealert.notification.linuxnotification import LinuxNotification
from ratealert.notification.windowsnotification import WindowsNotification


class ConversionAlert(object):

    def __init__(self, source, target, alert_rate):
        """
        Creates a transfer alert when the transfer rate is greater than target rate
        :param source: source currency
        :param target: target currency
        :param alert_rate: rate at which to raise alert
        """
        self._thread = None

        try:
            alert_rate = float(alert_rate)
        except ValueError:
            print('Enter a number as an alert rate')
            exit(0)

        authentication, notification = self._identify_platform()
        try:
            while True:
                current_rate = self._check_rate(source, target, authentication)
                print("The current exchange rate is - ", current_rate)
                if current_rate > alert_rate:
                    self._set_alert(current_rate, notification)
                time.sleep(int(300))
        except KeyboardInterrupt:
            exit(0)
        except InterruptedError:
            exit(0)

    def _check_rate(self, source, target, authentication):
        client = TransferwiseClient()

        try:
            token = client.load_auth_token(authentication)
        except FileNotFoundError:
            print('Unable to find a bearer token. Exiting.')
            print("""The program will try and find the access token in the following manner
                             1. System Variable named TCR
                             2. Configuration file - located at ~/.tcr on linux or 
                             %HOMEDRIVE%%HOMEPATH%/.tcr on windows""")
            exit()

        response = client.get_conversion_rate(source, target, token)
        return self._handle_response(response)

    def _identify_platform(self):
        """Identifies the system OS"""
        if platform == "linux" or platform == "linux2":
            return LinuxAuth(), LinuxNotification()
        elif platform == "win32":
            return WindowsAuth(), WindowsNotification()

    def _handle_response(self, response):
        json_response = json.loads(response.content.decode('utf8'))[0]
        return json_response['rate']

    def _set_alert(self, current_rate, notification):
        """Displays a notification on the desktop with the conversion rate

        :param notification:
        :param current_rate:
        :return: None
        """
        alert_text = 'The conversion rate is ' + str(current_rate)
        notification.set_notification(alert_text)
