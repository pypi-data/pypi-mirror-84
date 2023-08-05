from sallron.util import s3
import schedule
import datetime
import pytz

def send_logging_and_schedule_kill_process(key_path, log_dir, timezone):
    """
    Utility function to send the log file to S3 and kill the hole process

    Args:
        key_path (str): Path to AWS keys
        obj_path (str): Path to object to be sent
        timezone (str): Timezone string supported by pytz
    """

    schedule.every().day.at(
        datetime.time(hour=0, minute=1, tzinfo=pytz.timezone(timezone)).strftime("%H:%M")
    ).do(s3.send_to_s3, key_path=key_path, obj_path=log_dir)