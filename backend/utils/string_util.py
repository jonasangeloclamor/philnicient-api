import pytz
from datetime import datetime

class StringUtil:
    """
    Utility class for string operations.
    """

    @staticmethod
    def current_ph_time():
        """
        Gets the current datetime in the format 'yyyy-MM-dd HH:mm:ss' in Philippine Timezone.
        
        Returns:
            str: The current datetime string in Philippine Timezone.
        """
        ph_timezone = pytz.timezone('Asia/Manila')
        current_datetime = datetime.now(ph_timezone)
        format = "%Y-%m-%d %H:%M:%S"
        return current_datetime.strftime(format)
