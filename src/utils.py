#!/usr/bin/python3
# -*- coding: utf-8 -*-


from contextlib import closing
from datetime import timedelta
from smtplib import SMTP
from sys import stderr
from time import sleep
from urllib.error import URLError
from urllib.request import Request, urlopen

from config.config import Config


class Utils:

    @staticmethod
    def wait_for_internet() -> None:
        while True:
            try:
                req: Request = Request(Config.CONN_CHECK_ADDR)

                with closing(urlopen(req, timeout=Config.CONN_TIMEOUT)):
                    print('Internet connection is up.', end='\n\n')
                    break
            except URLError as url_error:
                print('Internet connection is down.', file=stderr)
                print('Can not reach', Config.CONN_CHECK_ADDR, file=stderr)
                print('Error:', url_error, file=stderr)
                print('Sleeping for', timedelta(seconds=Config.CONN_CHECK_REQ_DELAY), 'before trying again.',
                      end='\n\n', file=stderr)
                sleep(Config.CONN_CHECK_REQ_DELAY)

    @staticmethod
    def send_email(subject: str, text: str) -> None:
        message: str = 'Subject: {}\n\n{}'.format(subject, text)

        server: SMTP = SMTP(Config.SMTP_ADDR)
        server.ehlo()
        server.starttls()
        server.login(Config.SMTP_LOGIN, Config.SMTP_PWD)
        server.sendmail(Config.MAIL_FROM, Config.MAIL_TO, message)
        server.quit()

    @staticmethod
    def remove_control_symbols(input_object: str) -> str:
        output_object: str = ''

        for char in input_object:
            if ord(char) > 31:
                output_object += char

        return output_object
