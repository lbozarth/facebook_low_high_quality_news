import gzip
import os
import signal
import socket
import time
from http.cookiejar import MozillaCookieJar

import requests
# Disable warning
import urllib3
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, HTTPError, RetryError
from urllib3.exceptions import NewConnectionError, ConnectTimeoutError, MaxRetryError, SSLError, TimeoutError, \
    ReadTimeoutError, ResponseError
from urllib3.util.retry import Retry

# from requests_html import HTMLSession
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

hostname = socket.gethostname()
DEFAULT_SLEEP_TIME_FETCH = 3  # seconds
DEFAULT_READ_TIME = 15
DEFAULT_CONN_TIME = 15
DEFAULT_ITER_RESPONSE_TIME = 60
DEFAULT_MAX_TIME_PER_DAT = 45  #


def load_cookies_from_mozilla(filename):
    ns_cookiejar = MozillaCookieJar()
    ns_cookiejar.load(filename, ignore_discard=True)
    # print('number of cookies', len(ns_cookiejar))
    return ns_cookiejar


def get_url_write_filename(url, domain, base_dir):
    fn = url.split("://")[-1].replace("/", "+")
    if len(fn) > 201:
        fn = fn[:195] + fn[-5:]
    fn = fn + "_.html" + ".gz"
    fpn = os.path.join(base_dir, domain[0], fn)
    # print(fpn)
    return fpn


def get_default_session():
    s = requests.Session()
    # s = HTMLSession()
    retries = Retry(total=10,
                    backoff_factor=0.5,
                    status_forcelist=[429, 500, 502, 503, 504, 509, 520, 522, 524])

    adapter = HTTPAdapter(max_retries=retries)
    # adapter.max_retries.respect_retry_after_header = False
    s.mount('http://', adapter)
    s.mount('https://', adapter)
    return s


def get_session():
    # start session
    session = get_default_session()
    cookies = load_cookies_from_mozilla()
    session.cookies.update(cookies)
    # print('number of cookies in session', len(session.cookies))
    return session


def write_error_fn(wfn, estr):
    with gzip.open(wfn, 'wb') as f:
        f.write(estr.encode())
        f.close()
    return


def fetch(data, base_dir):
    session = get_session()

    def raise_session_hangs(signum, frame):
        # print('rank', MPI.COMM_WORLD.Get_rank(), 'session hanging error')
        raise RuntimeError("session left hanging")

    signal.signal(signal.SIGALRM, raise_session_hangs)

    results = []
    for row in data:
        try:
            domain = str(row['domain_highlevel'])
            url = str(row['url'])
            agent = row['agent']

            fpn = get_url_write_filename(url, domain, base_dir)
            if os.path.exists(fpn):
                continue

            time.sleep(DEFAULT_SLEEP_TIME_FETCH)  # sleep between each call

            headers = {'Accept-Encoding': 'gzip, deflate',
                       'Accept-Language': 'en-US,en;q=0.9',
                       'User-Agent': str(agent)}
            signal.alarm(DEFAULT_ITER_RESPONSE_TIME)
            resp = session.get(url, headers=headers, verify=False, stream=False,
                               timeout=(DEFAULT_CONN_TIME, DEFAULT_READ_TIME))  # stream=True,
            # resp.html.render
            status_code = resp.status_code
            resp_content = resp.content
            print('content', url, resp_content[:10])

            resp.close()  # close the response
            signal.alarm(0)

            results.append([url, status_code])
            with gzip.open(fpn, 'wb') as f:
                f.write(resp_content)
                f.close()

        except (
                MaxRetryError, NewConnectionError, ConnectTimeoutError, SSLError, ResponseError, TimeoutError,
                ReadTimeoutError,
                RetryError, ConnectionError, HTTPError) as e:
            results.append([url, 'H_error'])
            write_error_fn(fpn, str(e))
            continue
        except RuntimeError as e:
            results.append([url, 'R_error'])
            write_error_fn(fpn, str(e))
            continue
        except Exception as e:
            results.append([url, 'G_error'])
            write_error_fn(fpn, str(e))
            continue

    # signal.alarm(0)
    try:
        session.close()
    except Exception as e:
        pass

    return results


if __name__ == '__main__':
    # this script scrapes htmls webpages corresponding to a list of urls
    data = [['npr.org', 'https://www.npr.org/2023/05/26/1176823812/summer-books-list-2023', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36']] #list of list[domain, url, and user_agent]
    bas_dir = "./"
    results = fetch(data, bas_dir)
