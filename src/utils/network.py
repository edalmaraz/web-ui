"""
Network utilities with proper timeout and retry handling
"""

import time
from typing import Optional, Any, Dict
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class NetworkClient:
    """Network client with retry and timeout handling"""

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: int = 1,
        backoff_factor: float = 0.3,
    ):
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[500, 502, 503, 504],
        )

        # Create session with retry strategy
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """Make GET request with timeout and retry handling"""
        return self.session.get(
            url, params=params, headers=headers, timeout=self.timeout
        )

    def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """Make POST request with timeout and retry handling"""
        return self.session.post(
            url, data=data, json=json, headers=headers, timeout=self.timeout
        )

    def put(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """Make PUT request with timeout and retry handling"""
        return self.session.put(
            url, data=data, json=json, headers=headers, timeout=self.timeout
        )

    def delete(
        self, url: str, headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """Make DELETE request with timeout and retry handling"""
        return self.session.delete(url, headers=headers, timeout=self.timeout)

    def close(self):
        """Close the session"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
