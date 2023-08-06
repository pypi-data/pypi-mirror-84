from win10toast import ToastNotifier


class WindowsNotification:

    def _set_notification(self, message):
        """Set notification for windows system"""
        print(f"The conversion rate is - ", message)

        toaster = ToastNotifier()
        toaster.show_toast("Rate Alert!",
                           message["source"] + " 1 = " + message["target"] + " " + str(message["rate"]),
                           duration=5)

    def set_notification(self, message):
        """Set notification code for windows system"""
        return self._set_notification(message)
