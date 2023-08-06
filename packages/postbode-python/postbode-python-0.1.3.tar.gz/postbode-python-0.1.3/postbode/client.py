import base64
import json
import logging
import os

import requests

API_BAS_URL = "https://app.postbode.nu/api"
HEADERS = {"Content-Type": "application/json"}


class Client(object):
    def __init__(self, api_token: str):
        """Instantiate Postbode API client.

        :param api_base_url: API url starting point
        :type api_base_url: str
        :param token: API Token
        :type token: str
        :param mailbox: Mailbox id
        :type mailbox: str
        """

        self.api_base_url = API_BAS_URL
        self.headers = HEADERS

        # prepare header with authorization token.
        # self.headers['X-Authorization'] = api_token

        # setup session object
        self.session = requests.Session()
        self.session.headers = HEADERS
        self.session.headers["X-Authorization"] = api_token

    def hash_document(self, filepath: str) -> str:
        """Base64 encode PDF file.

        :param filepath: The file to use
        :type filepath: str.
        :returns: str of hashed file.
        """
        with open(filepath, "rb") as document:
            encoded_string = base64.b64encode(document.read()).decode("utf-8")
        return encoded_string

    def file_name_check(self, doc_name: str) -> str:
        """Get filename.

        :param doc_name: Full name of document
        :type doc_name: str.
        :returns: str of filename base.

        """
        if doc_name == "":
            self.send_letter.doc_file = os.path.splitext(
                self.send_letter.doc_file)[0]
        else:
            return doc_name

    def get_mailboxes(self):
        """Get all available mailboxes of token."""
        url = "{}/mailbox".format(self.api_base_url)
        response = self.session.get(url)

        if response.status_code == 200:
            return json.loads(response.content)
        else:
            return logging.error(
                "[!] HTTP {} calling {} with headers {}".format(
                    response.status_code, url, self.session.headers
                )
            )

    def get_mailbox(self, mailbox: int):
        """Get mailbox information."""
        url = "{}/mailbox/{}".format(self.api_base_url, mailbox)
        response = self.session.get(url)

        if response.status_code == 200:
            return json.loads(response.content)
        else:
            return logging.error(
                "[!] HTTP {} calling {} with headers {}".format(
                    response.status_code, url, self.session.headers
                )
            )

    def get_letters(self, mailbox: int):
        """Get letters from mailbox."""
        url = "{}/mailbox/{}/letters".format(self.api_base_url, mailbox)
        response = self.session.get(url)

        if response.status_code == 200:
            return json.loads(response.content)
        else:
            return logging.error(
                "[!] HTTP {} calling {} with headers {}".format(
                    response.status_code, url, self.session.headers
                )
            )

    def send_letter(
        self,
        mailbox_id: int,
        doc_name: str,
        doc_file: str,
        envelope_id: int,
        country: str,
        registered: bool,
        color: str,
        printing: str,
        printer: str,
        send: bool,
    ):
        """Send a letter."""

        url = "{}/mailbox/{}/letters".format(self.api_base_url, mailbox_id)

        payload = {
            "documents": [{"name": doc_name, "content": self.hash_document(doc_file)}],
            "envelope_id": envelope_id,
            "country": country,
            "registered": registered,
            "color": color,
            "printing": printing,
            "printer": printer,
            "send": send,
        }

        response = self.session.post(url, json=payload)

        if response.status_code == 200:
            return json.loads(response.content)
        else:
            return logging.error(
                "[!] HTTP {} calling {} with headers {}".format(
                    response.status_code, url, self.session.headers
                )
            )

    def send_letters(
        self,
        mailbox_id: int,
        envelope_id: int,
        country: str,
        registered: bool,
        color: str,
        printing: str,
        printer: str,
        send: bool,
        *letters: str
    ):
        """Send multiple letters at once.

        example:
        letters = ('./file1', './file2')
        client.send_letters(2522, 2, 'NL', False, 'FC', 'simplex', 'inkjet', True, *letters)
        """
        url = "{}/mailbox/{}/letters".format(self.api_base_url, mailbox_id)

        logging.info(">> send_letters docs: {}".format(letters))

        for letter in letters[0]:
            logging.info(">> doc: {}".format(letter))

            self.send_letter(
                mailbox_id,
                self.file_name_check(letter),
                letter,
                envelope_id,
                country,
                registered,
                color,
                printing,
                printer,
                send,
            )
