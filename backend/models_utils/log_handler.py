from datetime import datetime
import inspect
import logging

class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        try:
            from ..models import BackendLog  # Import here to avoid circular import

            # Sanitize message to prevent multiple single quotes
            message = self.format(record)
            message = message.replace("'", "''")  # Double the single quotes for SQL compliance

            log_entry = BackendLog(
                level=record.levelname,
                message=message,
                module=record.module
            )
            log_entry.save()
        except Exception as e:
            print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")