# coding=utf-8
"""
pyfastcom
https://github.com/ppizarror/pyfastcom
PYFASTCOM API

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2020 Pablo Pizarro R. @ppizarror
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

from bs4 import BeautifulSoup
from contextlib import contextmanager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from typing import Union, Dict, Tuple, Any
import os
import time
import unicodedata


@contextmanager
def get_chrome() -> 'Chrome':
    """
    Get chrome instance.
    # https://docs.python.org/3.7/library/contextlib.html#contextlib.contextmanager

    :return: Chrome object
    """
    opts = ChromeOptions()
    opts.headless = True
    driver = Chrome(options=opts)
    yield driver
    driver.close()


def wait_visible(driver: 'Chrome', selector: str, timeout: int = 5) -> None:
    """
    Wait for visible element.

    :param driver: Webdriver
    :param selector: Selector
    :param timeout: Max timeout
    """
    cond = ec.visibility_of_any_elements_located((By.CSS_SELECTOR, selector))
    try:
        WebDriverWait(driver, timeout).until(cond)
    except TimeoutException as exp:
        raise LookupError(f'{selector} is not visible after {timeout}s') from exp


def extract_info(soup: BeautifulSoup) -> Dict[str, Union[Tuple[int, str], str]]:
    """
    Extract info from the results page.

    :param soup: Extracted soup from web
    :return: Data dict
    """
    # Download speed
    dl_speed = int(soup.select_one('#speed-value').text)
    dl_unit = soup.select_one('#speed-units').text

    # Upload speed
    upload_speed = int(soup.select_one('#upload-value').text)
    upload_unit = soup.select_one('#upload-units').text

    # Download latency
    dl_latency_val = int(soup.select_one('#latency-value').text)
    dl_latency_unit = soup.select_one('#latency-units').text

    # Upload latency
    upload_latency_val = int(soup.select_one('#bufferbloat-value').text)
    upload_latency_unit = soup.select_one('#bufferbloat-units').text

    return {
        'client_ip': soup.select_one('#user-ip').text,
        'client_isp': soup.select_one('#user-isp').text,
        'client_location': soup.select_one('#user-location').text,
        'download': (dl_speed, dl_unit),
        'latency_download': (dl_latency_val, dl_latency_unit),
        'latency_upload': (upload_latency_val, upload_latency_unit),
        'server_info': unicodedata.normalize('NFKD', soup.select_one('#server-locations').text),
        'upload': (upload_speed, upload_unit),
    }


def query_results(timeout: int) -> str:
    """
    Get results.
    """
    with get_chrome() as driver:
        driver.get('https://fast.com')

        # Wait for more info button to click
        t0 = time.time()
        more_btn = 'show-more-details-link'
        wait_visible(driver, '#' + more_btn, timeout=timeout)
        btn = driver.find_element_by_id(more_btn)
        btn.click()
        timeout -= time.time() - t0

        # Wait until upload results come in
        wait_visible(driver, '#upload-units.succeeded', timeout=timeout)

        # This is the parent element that contains both download and upload results
        results_selector = '.speed-controls-container'
        results_el = driver.find_element_by_css_selector(results_selector)
        results_html = results_el.get_attribute('outerHTML')
        return results_html


class PyFastCom(object):
    """
    Fast.com API class.
    """
    _results: Union[dict, None]

    def __init__(self):
        """
        Constructor.
        """
        self._results = None

    @staticmethod
    def set_driver_path(path: str) -> None:
        """
        Set the driver path.

        :param path: Path
        """
        assert os.path.isdir(path), 'Given path "{}" is not a directory or does not exists'.format(path)
        os.environ['PATH'] += os.pathsep + path

    def run(self, timeout: int = 240) -> Dict[str, Union[Tuple[int, str], str]]:
        """
        Run speed test.
        """
        self._results = None  # Remove the results
        assert timeout > 0, 'Timeout must be greater than zero'
        try:
            results_html = query_results(timeout=timeout)
            soup = BeautifulSoup(results_html, 'html.parser')
            self._results = extract_info(soup)
            return self._results.copy()
        except LookupError as e:
            print(e)
            raise Exception('Cannot get speed results')

    def _get(self, key: str) -> Any:
        """
        Assert that run has been done and return the given value.
        """
        assert self.ready(), 'Results not exists. Execute .run() method first'
        return self._results[key]

    def ready(self) -> bool:
        """
        Return true if the results exists.
        """
        return self._results is not None

    def get_client_ip(self) -> str:
        """
        Return client IP.
        """
        return self._get('client_ip')

    def get_client_isp(self) -> str:
        """
        Return client ISP.
        """
        return self._get('client_isp')

    def get_client_location(self) -> str:
        """
        Return client location.
        """
        return self._get('client_location')

    def get_download_speed(self) -> Tuple[int, str]:
        """
        Return download speed (value, unit).
        """
        return self._get('download')

    def get_upload_speed(self) -> Tuple[int, str]:
        """
        Return upload speed (value, unit).
        """
        return self._get('upload')

    def get_download_latency(self) -> Tuple[int, str]:
        """
        Return download latency (value, unit).
        """
        return self._get('latency_download')

    def get_upload_latency(self) -> Tuple[int, str]:
        """
        Return upload latency (value, unit).
        """
        return self._get('latency_upload')

    def get_server_info(self) -> str:
        """
        Return server info.
        """
        return self._get('server_info')
