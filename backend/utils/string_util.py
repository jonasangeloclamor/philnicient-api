from datetime import datetime

class StringUtil:
    """
    Utility class for string operations.
    """

    @staticmethod
    def get_current_datetime():
        """
        Gets the current datetime in the format 'yyyy-MM-dd HH:mm:ss'.
        
        Returns:
            str: The current datetime string.
        """
        time = datetime.now()
        format = "%Y-%m-%d %H:%M:%S"
        current_datetime = time.strftime(format)

        return current_datetime
