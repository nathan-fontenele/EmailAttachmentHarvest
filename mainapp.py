import os
import time
import schedule
from imap_tools import MailBox, AND
import configapp
import datetime

def load_configurations(config_dir):
    return configapp.load_configurations(config_dir)

def download_attachments(configurations):
    if not configurations:
        return

    username = configurations.get("USERNAME")
    password = configurations.get("PASSWORD")
    from_email = configurations.get("FROM_EMAIL")
    log_folder = configurations.get("LOG_FOLDER")
    destination_folder = configurations.get("DESTINATION_FOLDER")

    attachments_dir = os.path.join(destination_folder, "Anexos")
    log_dir = os.path.join(log_folder, "Log")
    log_file = os.path.join(log_dir, "Log.txt")

    try:
        my_email = MailBox("imap.gmail.com").login(username, password, initial_folder="Inbox")

        existing_attachments = set()

        # Filter
        email_list = my_email.fetch(AND(from_=from_email))

        # Current date
        current_date = datetime.date.today().strftime("%d-%m-%Y")

        # Capture attachments
        for message in email_list:
            for attachment in message.attachments:
                if attachment.filename not in existing_attachments:
                    existing_attachments.add(attachment.filename)

                    file_path = os.path.join(attachments_dir, attachment.filename)
                    size = attachment.size
                    content_type = attachment.content_type
                    attachment_info = attachment.payload

                    with open(file_path, "wb") as pdf_file:
                        pdf_file.write(attachment_info)

                    with open(log_file, "a+") as log_text:
                        new_line = f"{current_date} - {attachment.filename} - {size/1024/1024:.2f} Mb - {content_type} - ADDED\n"
                        log_text.seek(0)
                        lines = log_text.readlines()

                        print(new_line)

                        if not lines or new_line != lines[-1]:
                            log_text.write(new_line)

                    my_email.move([message.uid], "Feito")

    except Exception as ex:
        with open(log_file, "a+") as log_text:
            new_line = f"{ex}\n"
            log_text.seek(0)
            lines = log_text.readlines()
            if not lines or new_line != lines[-1]:
                log_text.write(new_line)

        print(new_line)

def main():
    config_dir = r".\\appconfig.json"
    configurations = configapp.load_configurations(config_dir)

    schedule_manager = schedule.Scheduler()
    schedule_manager.every(30).seconds.do(download_attachments, configurations)

    while True:
        schedule_manager.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
