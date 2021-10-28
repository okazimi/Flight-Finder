from twilio.rest import Client
import smtplib


class NotificationManager:

    def __init__(self):
        self.account_sid = "ACe0b4deacc51b2b7e260de3cdba32a2df"
        self.auth_token = "3f6e7cf85a054c0f1c293fbd195a772d"
        self.client = Client(self.account_sid, self.auth_token)

    def send_text(self, message):
        message = self.client.messages \
                        .create(
                             body=message,
                             from_='+18482891475',
                             to='+15708142353'
                         )

        print(message.sid)

    def send_emails(self, recipient_email, msg):
        USERNAME = "pythoncreator@hotmail.com"
        PASSWORD = "THECHOSENONE1"
        smtp = smtplib.SMTP("smtp.live.com")
        smtp.starttls()
        smtp.login(USERNAME, PASSWORD)
        smtp.sendmail(
            from_addr=USERNAME,
            to_addrs=recipient_email,
            msg=msg
        )

