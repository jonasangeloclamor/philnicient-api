import pytz
from datetime import datetime
from google.cloud.firestore import SERVER_TIMESTAMP

class StringUtil:
    """
    Utility class for string operations.
    """

    @staticmethod
    def current_ph_time():
        """
        Gets the current datetime in the format 'yyyy-MM-dd HH:mm:ss' in Philippine Timezone,
        by converting Firestore's SERVER_TIMESTAMP to the Philippine Timezone.
        
        Returns:
            str: The current datetime string in Philippine Timezone with UTC offset.
        """
        if SERVER_TIMESTAMP:
            utc_timezone = pytz.timezone('UTC')  
            current_server_time = datetime.now(utc_timezone)
            ph_timezone = pytz.timezone('Asia/Manila')
            ph_time = current_server_time.astimezone(ph_timezone)
            format = "%Y-%m-%d %H:%M:%S"  
            return ph_time.strftime(format)
        else:
            return "SERVER_TIMESTAMP_placeholder"
