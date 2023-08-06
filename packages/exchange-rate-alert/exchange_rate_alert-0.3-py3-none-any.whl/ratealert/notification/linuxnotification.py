#import notify2 as notify2


class LinuxNotification:

    def _set_notification(self, message):
        """Set notification for unix system"""
        print(message)
        # notify2.init('Rate Alert!')
        # n = notify2.Notification(current_rate["source"] + " 1 = " + current_rate["target"] + " " + str(current_rate["rate"]))
        # n.show()

    def set_notification(self, message):
        """Set notification code for unix system"""
        return self._set_notification(message)
