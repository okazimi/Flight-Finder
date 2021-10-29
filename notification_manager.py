from twilio.rest import Client
import smtplib


class NotificationManager:

    def __init__(self):
        self.account_sid = MY_ACCT_SID
        self.auth_token = MY_AUTH_TOKEN
        self.client = Client(self.account_sid, self.auth_token)

    def send_text(self, message):
        message = self.client.messages \
                        .create(
                             body=message,
                             from_='+111111111',
                             to='+1111111111'
                         )

        print(message.sid)

    def send_emails(self, recipient_email, msg):
        USERNAME = "EMAIL@EMAIL.COM"
        PASSWORD = "PASSWORD"
        smtp = smtplib.SMTP("smtp.live.com")
        smtp.starttls()
        smtp.login(USERNAME, PASSWORD)
        smtp.sendmail(
            from_addr=USERNAME,
            to_addrs=recipient_email,
            msg=msg
        )

