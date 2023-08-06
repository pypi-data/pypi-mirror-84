# import notify2
import click


class LinuxNotification:

    def _set_notification(self, message):
        """Set notification for unix system"""
        click.echo(message)
        # notify2.init('Exchange Rate Alert!')
        # n = notify2.Notification("Rate Alert!", message=(message+" Get that Money!"))
        # n.set_urgency(notify2.URGENCY_NORMAL)
        # n.show()

    def set_notification(self, message):
        """Set notification code for unix system"""
        return self._set_notification(message)
