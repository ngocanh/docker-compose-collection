#!/usr/bin/env python

"""
otn-downloader.py: Script to download from Oracle Technology Network (OTN) from terminal.

https://github.com/ngocanh/docker-compose-collection/docker-context/scripts/otn-downloader.py
One of my first python scripts, bear with me :)
OTN provides no API to auth and access files for download, only by browser which is inconvenient for automation/contain-
erizing
"""


import re
import argparse
from requests import Session
from pyquery import PyQuery as pq
from clint.textui import progress

try:
    # Python2
    from urlparse import urljoin
except ImportError:
    # Python3
    from urllib.parse import urljoin


__author__ = "Ngoc Anh Doan"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Ngoc Anh Doan"
__email__ = "ngoc@nhdoan.de"
__status__ = "Development"


def main():
    """


    :return:
    """
    def _handle_args():
        """
        Terminal arguments handling

        :return:
        """
        ap = argparse.ArgumentParser(description='OracleTechnologyNetwork downloader')
        ap.add_argument('url', help='URL to download resource from OTN')
        ap.add_argument('--dest', help='path to store the downloaded file', default='.')

        # https://stackoverflow.com/a/24181138
        ap_group_req_names = ap.add_argument_group('named arguments (required)')
        ap_group_req_names.add_argument('-u', '--username', help='Oracle SSO account', required=True)
        ap_group_req_names.add_argument('-p', '--password', required=True)

        return ap.parse_args()

    args = _handle_args()

    if not args.username or not args.password:
        print('No (or empty) username/password provided')

    otn_authenticate_and_download(args.username, args.password, args.url, args.dest)


def otn_authenticate_and_download(username, password, url, dest_path='.'):
    """
    Authenticate against Oracles SSO and download the file

    :param username:
    :param password:
    :param url:
    :param dest_path:
    :return:
    """
    def _extract_post_form(_response):
        """
        Extract form inputs to post

        :param _response:
        :return: String, Dict
        """
        html_tree = pq(_response.content)
        _post_url = urljoin(_response.url, html_tree('form').attr('action'))
        _post_data = {elm.attr('name'): elm.attr('value') for elm in html_tree.items('form input')}

        # Depending on the form user input name is either username or ssousername
        _post_data.update({'username': username, 'ssousername': username, 'password': password})

        return _post_url, _post_data

    def _get_request_session():
        """
        Get prepared session object with *required* user-agent and accepted oraclelicense

        :return: Session
        """
        _sess = Session()

        _sess.headers.update({'User-Agent': 'Mozilla - OTN-Downloader/1.0'})
        _sess.cookies.update({'oraclelicense': 'yep, why not'})

        return _sess

    def _save():
        """
        Save the file with progress bar

        :return:
        """
        _file = dest_path + '/' + file_name

        print('save \'{0}\' with size: {1} KB'.format(_file, (total_length/1024)))
        with open(_file, 'wb') as _stream:
            for chunk in progress.bar(response.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                if chunk:
                    _stream.write(chunk)
                    _stream.flush()

    file_name = url.split('/')[-1]
    sess = _get_request_session()
    login_attemps = 1
    form_login_post_url = url
    form_login_post_data = None
    response = sess.get(form_login_post_url)
    url = re.sub(r'https*\:\/\/', '', url)

    try:
        print('login {0}: {1}'.format(login_attemps, response.url))

        # if the url in response matches original dl-url we are authenticated
        while not re.search(url, response.url) and (login_attemps < 10):
            form_login_post_url, form_login_post_data = _extract_post_form(response)
            # keeps POST'ing until we get redirected to file
            response = sess.post(form_login_post_url, data=form_login_post_data, stream=True)
            login_attemps += 1
            print('login {0}: {1}'.format(login_attemps, response.url))

        if re.search(url, response.url):
            print('successfully logged in, start downloading')
            total_length = int(response.headers.get('content-length'))
            _save()
        else:
            raise Exception('Could not login!')
    except Exception as exc:
        print(str(exc))


if __name__ == '__main__':
    main()
