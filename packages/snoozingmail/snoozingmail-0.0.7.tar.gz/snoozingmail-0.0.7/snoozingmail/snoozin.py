import re
import html2text

import snoozingmail.gmail.creds as creds
import snoozingmail.gmail.read as read_email
import snoozingmail.gmail.send as send_email
import snoozingmail.gmail.modify as modify_email


class Snoozin:
    """Interface into the gmail api wrapper.

    Has methods to read, send, and modify messages
    in the connected gmail account.
    """
    def __init__(self, credentials):
        """Initialize the Snoozin object by creating the gmail
        service using the provided credentials file.

        Args:
            credentials: Local path to credentials file
        """
        self.service = creds.get_gmail_service(credentials)

    def get_matching_msgs(self, query):
        """Get message ids for messages that match the given query

        Args:
            query: String used to filter messages returned. (ex:
                   'from:user@some_domain.com' for Messages from
                   a particular sender.)

        Returns:
            List of message ids
        """
        msg_matches = read_email.ListMessagesMatchingQuery(self.service, query)
        return [msg_match["id"] for msg_match in msg_matches]

    def get_labeled_msgs(self, labels):
        """Get message ids for messages that have all the given labels

        Args:
            labels: list of labels (ex: '['STARRED', 'UNREAD']' for
                    starred unread emails)

        Returns:
            List of message ids
        """
        labeled_msgs = read_email.ListMessagesWithLabels(self.service, labels)
        return [labeled_msg["id"] for labeled_msg in labeled_msgs]

    def get_sender(self, msg_id):
        """Get the sender of the given message.

        Args:
            msg_id: The id of the message, which can be used to get details
                    of the message.

        Returns:
            The sender's email address with name ommitted.
        """
        # Get message
        message = read_email.GetMimeMessage(self.service, msg_id)

        # Get email address of sender
        sender_full = message["From"]
        sender_address = re.search('<(.*)>', sender_full).group(1)
        return sender_address

    def remove_msg_labels(self, msg_id, labels):
        """Remove labels from the given message.

        Args:
            msg_id: The id of the message, which can be used to get details
                    of the message.
            labels: list of labels (ex: '['STARRED', 'UNREAD']' for
                    starred unread emails)
        """
        msg_labels = {'removeLabelIds': labels}
        modify_email.ModifyMessage(self.service, msg_id, msg_labels)

    def add_msg_labels(self, msg_id, labels):
        """Add labels to the given message.

        Args:
            msg_id: The id of the message, which can be used to get details
                    of the message.
            labels: list of labels (ex: '['STARRED', 'UNREAD']' for
                    starred unread emails)
        """
        msg_labels = {'addLabelIds': labels}
        modify_email.ModifyMessage(self.service, msg_id, msg_labels)

    def get_msg_body(self, msg_id):
        """Get the message body in plain text format.

        Works as long as the message has a 'text/plain' or 'text/html' part.

        Args:
            msg_id: The id of the message, which can be used to get details
                    of the message.

        Returns:
            The body of the email in plain text format
        """
        # Get message
        message = read_email.GetMimeMessage(self.service, msg_id)

        # If message is multipart, then find the first 'text/plain' or
        # 'text/html' part
        if message.is_multipart():
            # Go through message and capture plain text of message body
            for part in message.walk():
                if part.get_content_type() in ['text/plain', 'text/html']:
                    message = part
                    break

        # Decode the message
        msg_bytes = message.get_payload(decode=True)
        decoded_message = msg_bytes.decode(message.get_content_charset())

        # Return the message, doing html decoding if necessary
        if message.get_content_type() == 'text/html':
            return html2text.html2text(decoded_message)
        elif message.get_content_type() == 'text/plain':
            return decoded_message
        else:
            return None

    def send(self, to, subject, message_body, html=False, attachments=[]):
        """Send a message.

        Args:
            to: Email address of the receiver.
            subject: The subject of the email message.
            plaintext_content: The plantext content of the email message.
            message_text: The plaintext content of the email message.
            html: (optional) Whether the mesage_body is formatted as html
            attachments: (optional) List of file paths to files that should
                         be attached to the email

        Returns:
            The message that was sent
        """

        message = send_email.CreateMessage(to, subject, message_body, html,
                                           attachments)
        return send_email.SendMessage(self.service, message)
