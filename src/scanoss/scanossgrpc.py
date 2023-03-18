"""
 SPDX-License-Identifier: MIT

   Copyright (c) 2021, SCANOSS

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in
   all copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
   THE SOFTWARE.
"""

import os
import uuid

import grpc
import json

from google.protobuf.json_format import MessageToDict, ParseDict
from pypac.parser import PACFile
from pypac.resolver import ProxyResolver
from urllib.parse import urlparse

from .api.cryptography.v2.scanoss_cryptography_pb2_grpc import CryptographyStub
from .api.dependencies.v2.scanoss_dependencies_pb2_grpc import DependenciesStub
from .api.cryptography.v2.scanoss_cryptography_pb2 import AlgorithmResponse
from .api.dependencies.v2.scanoss_dependencies_pb2 import DependencyRequest, DependencyResponse
from .api.common.v2.scanoss_common_pb2 import EchoRequest, EchoResponse, StatusResponse, StatusCode, PurlRequest
from .scanossbase import ScanossBase
from . import __version__

# DEFAULT_URL      = "https://osskb.org"
DEFAULT_URL = "https://scanoss.com"
SCANOSS_GRPC_URL = os.environ.get("SCANOSS_GRPC_URL") if os.environ.get("SCANOSS_GRPC_URL") else DEFAULT_URL
SCANOSS_API_KEY = os.environ.get("SCANOSS_API_KEY") if os.environ.get("SCANOSS_API_KEY") else ''


class ScanossGrpc(ScanossBase):
    """
    Client for gRPC functionality
    """

    def __init__(self, url: str = None, debug: bool = False, trace: bool = False, quiet: bool = False,
                 ca_cert: str = None, api_key: str = None, ver_details: str = None, timeout: int = 600,
                 proxy: str = None, grpc_proxy: str = None, pac: PACFile = None):
        """

        :param url:
        :param debug:
        :param trace:
        :param quiet:
        :param ca_cert:

        To set a custom certificate use:
            GRPC_DEFAULT_SSL_ROOTS_FILE_PATH=/path/to/certs/cert.pem
        More details here: https://grpc.github.io/grpc/cpp/grpc__security__constants_8h.html
                           https://github.com/grpc/grpc/blob/master/doc/environment_variables.md
        To enable a Proxy use:
            grpc_proxy='http://<ip>:<port>'
        """
        super().__init__(debug, trace, quiet)
        self.url = url if url else SCANOSS_GRPC_URL
        self.url = self.url.lower()
        self.orig_url = self.url  # Used for proxy lookup
        self.api_key = api_key if api_key else SCANOSS_API_KEY
        self.timeout = timeout
        self.proxy = proxy
        self.grpc_proxy = grpc_proxy
        self.pac = pac
        self.metadata = []
        if self.api_key:
            self.metadata.append(('x-api-key', api_key))  # Set API key if we have one
        if ver_details:
            self.metadata.append(('x-scanoss-client', ver_details))
        self.metadata.append(('user-agent', f'scanoss-py/{__version__}'))
        secure = True if self.url.startswith('https:') else False  # Is it a secure connection?
        if self.url.startswith('http'):
            u = urlparse(self.url)
            port = u.port
            if port is None:
                port = 443 if u.scheme == 'https' else 80  # Set the default port number if it's not available
            self.url = f'{u.hostname}:{port}'
        cert_data = None
        if ca_cert is not None:
            secure = True
            cert_data = ScanossGrpc._load_cert(ca_cert)
        self.print_debug(f'Setting up (secure: {secure}) connection to {self.url}...')
        self._get_proxy_config()
        if secure is False:  # insecure connection
            self.dependencies_stub = DependenciesStub(grpc.insecure_channel(self.url))
            self.crypto_stub = CryptographyStub(grpc.insecure_channel(self.url))
        else:
            if ca_cert is not None:
                credentials = grpc.ssl_channel_credentials(cert_data)  # secure with specified certificate
            else:
                credentials = grpc.ssl_channel_credentials()  # secure connection with default certificate
            self.dependencies_stub = DependenciesStub(grpc.secure_channel(self.url, credentials))
            self.crypto_stub = CryptographyStub(grpc.secure_channel(self.url, credentials))

    @classmethod
    def _load_cert(cls, cert_file: str) -> bytes:
        with open(cert_file, 'rb') as f:
            return f.read()

    def deps_echo(self, message: str = 'Hello there!') -> str:
        """
        Send Echo message to the Dependency service
        :param self:
        :param message: Message to send (default: Hello there!)
        :return: echo or None
        """
        request_id = str(uuid.uuid4())
        resp: EchoResponse
        try:
            metadata = self.metadata[:]
            metadata.append(('x-request-id', request_id))  # Set a Request ID
            resp = self.dependencies_stub.Echo(EchoRequest(message=message), metadata=metadata, timeout=3)
        except Exception as e:
            self.print_stderr(f'ERROR: {e.__class__.__name__} Problem encountered sending gRPC message '
                              f'(rqId: {request_id}): {e}')
        else:
            # self.print_stderr(f'resp: {resp} - call: {call}')
            # response_id = ""
            # if not call:
            #     self.print_stderr(f'No call to leverage.')
            # for key, value in call.trailing_metadata():
            #     print('Greeter client received trailing metadata: key=%s value=%s' % (key, value))
            #
            # for key, value in call.trailing_metadata():
            #     if key == 'x-response-id':
            #         response_id = value
            # self.print_stderr(f'Response ID: {response_id}. Metadata: {call.trailing_metadata()}')
            if resp:
                return resp.message
            self.print_stderr(f'ERROR: Problem sending Echo request ({message}) to {self.url}. rqId: {request_id}')
        return None

    def crypto_echo(self, message: str = 'Hello there!') -> str:
        """
        Send Echo message to the Cryptography service
        :param self:
        :param message: Message to send (default: Hello there!)
        :return: echo or None
        """
        request_id = str(uuid.uuid4())
        resp: EchoResponse
        try:
            metadata = self.metadata[:]
            metadata.append(('x-request-id', request_id))  # Set a Request ID
            resp = self.crypto_stub.Echo(EchoRequest(message=message), metadata=metadata, timeout=3)
        except Exception as e:
            self.print_stderr(f'ERROR: {e.__class__.__name__} Problem encountered sending gRPC message '
                              f'(rqId: {request_id}): {e}')
        else:
            if resp:
                return resp.message
            self.print_stderr(f'ERROR: Problem sending Echo request ({message}) to {self.url}. rqId: {request_id}')
        return None

    def get_dependencies(self, dependencies: json, depth: int = 1) -> dict:
        if not dependencies:
            self.print_stderr('ERROR: No dependency data supplied to submit to the API.')
            return None
        resp = self.get_dependencies_json(dependencies, depth)
        if not resp:
            self.print_stderr(f'ERROR: No response for dependency request: {dependencies}')
        return resp

    def get_dependencies_json(self, dependencies: dict, depth: int = 1) -> dict:
        """
        Client function to call the rpc for GetDependencies
        :param dependencies: Message to send to the service
        :param depth: depth of sub-dependencies to search (default: 1)
        :return: Server response or None
        """
        if not dependencies:
            self.print_stderr(f'ERROR: No message supplied to send to gRPC service.')
            return None
        request_id = str(uuid.uuid4())
        resp: DependencyResponse
        try:
            files_json = dependencies.get("files")
            if files_json is None or len(files_json) == 0:
                self.print_stderr(f'ERROR: No dependency data supplied to send to gRPC service.')
                return None
            request = ParseDict(dependencies, DependencyRequest())  # Parse the JSON/Dict into the dependency object
            request.depth = depth
            metadata = self.metadata[:]
            metadata.append(('x-request-id', request_id))  # Set a Request ID
            self.print_debug(f'Sending dependency data for decoration (rqId: {request_id})...')
            resp = self.dependencies_stub.GetDependencies(request, metadata=metadata, timeout=self.timeout)
        except Exception as e:
            self.print_stderr(f'ERROR: {e.__class__.__name__} Problem encountered sending gRPC message '
                              f'(rqId: {request_id}): {e}')
        else:
            if resp:
                if not self._check_status_response(resp.status, request_id):
                    return None
                return MessageToDict(resp, preserving_proto_field_name=True)  # Convert gRPC response to a dictionary
        return None

    def get_crypto_json(self, purls: dict) -> dict:
        """
        Client function to call the rpc for Cryptography GetAlgorithms
        :param purls: Message to send to the service
        :return: Server response or None
        """
        if not purls:
            self.print_stderr(f'ERROR: No message supplied to send to gRPC service.')
            return None
        request_id = str(uuid.uuid4())
        resp: AlgorithmResponse
        try:
            request = ParseDict(purls, PurlRequest())  # Parse the JSON/Dict into the purl request object
            metadata = self.metadata[:]
            metadata.append(('x-request-id', request_id))  # Set a Request ID
            self.print_debug(f'Sending crypto data for decoration (rqId: {request_id})...')
            resp = self.crypto_stub.GetAlgorithms(request, metadata=metadata, timeout=self.timeout)
        except Exception as e:
            self.print_stderr(f'ERROR: {e.__class__.__name__} Problem encountered sending gRPC message '
                              f'(rqId: {request_id}): {e}')
        else:
            if resp:
                if not self._check_status_response(resp.status, request_id):
                    return None
                resp_dict = MessageToDict(resp, preserving_proto_field_name=True)  # Convert gRPC response to a dictionary
                del resp_dict['status']
                return resp_dict
        return None

    def _check_status_response(self, status_response: StatusResponse, request_id: str = None) -> bool:
        """
        Check the response object to see if the command was successful or not
        :param status_response: Status Response
        :return: True if successful, False otherwise
        """
        if not status_response:
            self.print_stderr(f'Warning: No status response supplied (rqId: {request_id}). Assuming it was ok.')
            return True
        self.print_debug(f'Checking response status (rqId: {request_id}): {status_response}')
        status_code: StatusCode = status_response.status
        if status_code > 1:
            self.print_stderr(f'Not such a success (rqId: {request_id}): {status_response.message}')
            return False
        return True

    def _get_proxy_config(self):
        """
        Set the grpc_proxy/http_proxy/https_proxy environment variables if PAC file has been specified
        or if an explicit proxy has been supplied
        :param self:
        """
        if self.grpc_proxy:
            self.print_debug(f'Setting GRPC (grpc_proxy) proxy...')
            os.environ["grpc_proxy"] = self.grpc_proxy
        elif self.proxy:
            self.print_debug(f'Setting GRPC (http_proxy/https_proxy) proxies...')
            os.environ["http_proxy"] = self.proxy
            os.environ["https_proxy"] = self.proxy
        elif self.pac:
            self.print_debug(f'Attempting to get GRPC proxy details from PAC for {self.orig_url}...')
            resolver = ProxyResolver(self.pac)
            proxies = resolver.get_proxy_for_requests(self.orig_url)
            if proxies:
                self.print_trace(f'Setting proxies: {proxies}')
            os.environ["http_proxy"] = proxies.get("http") or ""
            os.environ["https_proxy"] = proxies.get("https") or ""

#
# End of ScanossGrpc Class
#
