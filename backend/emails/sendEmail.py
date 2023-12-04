"""
This module sends emails with attachments to the participants
Reference - https://developers.google.com/gmail/api/quickstart/python
"""

import base64
import mimetypes
import os
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def authentication():
    credentials = None

    # The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the time.
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file(
            'token.json',
            SCOPES
        )

    # If there are no valid credentials available, le the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES,redirect_uri='https://2976-24-23-158-128.ngrok-free.app')
            # flow.redirect_uri = 'https://2976-24-23-158-128.ngrok-free.app'
            credentials = flow.run_local_server(port=8080)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    return credentials


def prepare_and_send_email(recipient, subject, message_text, attachment):
    """
    Prepares and send email with attachment to the participants.
    :param attachment: file path of the attachment that you want to send.
    :param recipient: email-id of the recipient
    :param subject: subject of the email
    :param message_text: body of the email
    """

    credentials = authentication()

    try:
        # Call the Gmail API
        service = build(serviceName='gmail', version='v1', credentials=credentials)

        # create message
        message = create_message('cal160@ucsd.edu', recipient, subject, message_text, attachment)
        send_message(service, 'me', message)
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API
        print(f"An error occurred: {error}")


def create_message(sender, to, subject, message_text, attachment):
    """
    Create a message for an email.
    :param attachment: file path of the attachment that you want to send.
    :param sender: Email address of the sender.
    :param to: Email address of the receiver.
    :param subject: The subject of the email message.
    :param message_text: The text of the email message.
    :return: An object containing a base64url encoded email object.
    """

    # create gmail api client
    mime_message = EmailMessage()

    # headers
    mime_message['From'] = sender
    mime_message['To'] = to
    mime_message['Subject'] = subject

    # text
    mime_message.set_content(message_text)

    # attachment
    attachment_filename = attachment
    # guessing the MIME type
    type_subtype, _ = mimetypes.guess_type(attachment_filename)
    maintype, subtype = type_subtype.split('/')

    with open(attachment_filename, 'rb') as fp:
        attachment_data = fp.read()
    mime_message.add_attachment(attachment_data, maintype, subtype, filename=attachment_filename)

    return {'raw': base64.urlsafe_b64encode(mime_message.as_bytes()).decode()}


def send_message(service, user_id, message):
    """
    Send an email message.
    :param service: Authorized Gmail API service instance.
    :param user_id: User's email address. The special value 'me' can be used to indicate the authenticated user.
    :param message: Message to be sent.
    :return: Sent Message.
    """

    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print(f"Message Id: {message['id']}")
        return message
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    prepare_and_send_email('catherinelee274@yahoo.com', 'Your model is training', 'We will send you an email when your model is done training!', 'photo.jpg')
