from urllib.request import Request, urlopen, ssl, socket
from urllib.error import URLError, HTTPError
import json

import yaml
import boto3

class SSLCert:

    def __init__(self, hostname, port=443, timeout=10):
        self.hostname = hostname
        self.port = port
        self.timeout = timeout
        self.cert = self.get_cert()

    def get_cert(self):
        """
        Get the certification material
        X: Should add timeout
        """
        context = ssl.create_default_context()

        try:
            with socket.create_connection((self.hostname, self.port), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    data = ssock.getpeercert()
        except Exception as e:
            data = dict(status="failed", message=str(e))
            return data
        data["status"] = "success"
        data["message"] = ""
        return data

    def get_cert_expiration(self):
        """
        Returns a dictionary with cert expiration dates
        """
        response = dict(hostname=self.hostname,
                        not_before=self.cert.get("notBefore"),
                        not_after=self.cert.get("notAfter"))
        return response

    def get_cert_expiration_to_json(self):
        response = self.get_cert_expiration()
        return json.dumps(response)

    def to_json(self):
        return json.dumps(self.cert, indent=2, sort_keys=True)
