"""Console script for techbox."""
import sys

import fire

from .cloud.aws.monitor import Billing
from .snippets import print_snippet, get_snippet
from .boto3_wrapper import Boto3Wrapper
from .tls import SSLCert


class TechboxCli:

    @staticmethod
    def snippet(path, from_line, to_line):
        snippet = get_snippet(path, from_line, to_line)
        print_snippet(snippet)

    @staticmethod
    def aws_instances_info(fields=None):
        boto3_wrapper = Boto3Wrapper()
        if fields:
            boto3_wrapper.describe_instances_from_fields(fields)
        else:
            boto3_wrapper.describe_instances_basic()

    @staticmethod
    def aws_daily_cost():
        billing = Billing()
        print(billing.get_daily_blended_cost())

    @staticmethod
    def aws_monthly_cost():
        billing = Billing()
        print(billing.get_monthly_blended_cost())

    @staticmethod
    def get_ssl_expiration(hostname, port=443, timeout=10):
        ssl = SSLCert(hostname=hostname, port=port, timeout=timeout)
        print(ssl.get_cert_expiration_to_json())

    @staticmethod
    def get_ssl(hostname, port=443, timeout=10):
        ssl = SSLCert(hostname=hostname, port=port, timeout=timeout)
        print(ssl.to_json())


def ep():
    fire.Fire(TechboxCli)
