from win10toast import ToastNotifier


class WindowsNotification:

    def _set_notification(self, message):
        """Set notification for windows system"""
        print(message)

        toaster = ToastNotifier()
        toaster.show_toast("Rate Alert!",
                           message + " Get that Money!",
                           duration=5)

    def set_notification(self, message):
        """Set notification code for windows system"""
        return self._set_notification(message)
