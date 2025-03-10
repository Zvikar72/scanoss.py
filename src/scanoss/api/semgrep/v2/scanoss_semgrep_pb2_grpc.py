# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""

import grpc

from scanoss.api.common.v2 import scanoss_common_pb2 as scanoss_dot_api_dot_common_dot_v2_dot_scanoss__common__pb2
from scanoss.api.semgrep.v2 import scanoss_semgrep_pb2 as scanoss_dot_api_dot_semgrep_dot_v2_dot_scanoss__semgrep__pb2


class SemgrepStub(object):
    """
    Expose all of the SCANOSS Cryptography RPCs here
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Echo = channel.unary_unary(
            '/scanoss.api.semgrep.v2.Semgrep/Echo',
            request_serializer=scanoss_dot_api_dot_common_dot_v2_dot_scanoss__common__pb2.EchoRequest.SerializeToString,
            response_deserializer=scanoss_dot_api_dot_common_dot_v2_dot_scanoss__common__pb2.EchoResponse.FromString,
        )
        self.GetIssues = channel.unary_unary(
            '/scanoss.api.semgrep.v2.Semgrep/GetIssues',
            request_serializer=scanoss_dot_api_dot_common_dot_v2_dot_scanoss__common__pb2.PurlRequest.SerializeToString,
            response_deserializer=scanoss_dot_api_dot_semgrep_dot_v2_dot_scanoss__semgrep__pb2.SemgrepResponse.FromString,
        )


class SemgrepServicer(object):
    """
    Expose all of the SCANOSS Cryptography RPCs here
    """

    def Echo(self, request, context):
        """Standard echo"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetIssues(self, request, context):
        """Get Potential issues  associated with a list of PURLs"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SemgrepServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'Echo': grpc.unary_unary_rpc_method_handler(
            servicer.Echo,
            request_deserializer=scanoss_dot_api_dot_common_dot_v2_dot_scanoss__common__pb2.EchoRequest.FromString,
            response_serializer=scanoss_dot_api_dot_common_dot_v2_dot_scanoss__common__pb2.EchoResponse.SerializeToString,
        ),
        'GetIssues': grpc.unary_unary_rpc_method_handler(
            servicer.GetIssues,
            request_deserializer=scanoss_dot_api_dot_common_dot_v2_dot_scanoss__common__pb2.PurlRequest.FromString,
            response_serializer=scanoss_dot_api_dot_semgrep_dot_v2_dot_scanoss__semgrep__pb2.SemgrepResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler('scanoss.api.semgrep.v2.Semgrep', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Semgrep(object):
    """
    Expose all of the SCANOSS Cryptography RPCs here
    """

    @staticmethod
    def Echo(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/scanoss.api.semgrep.v2.Semgrep/Echo',
            scanoss_dot_api_dot_common_dot_v2_dot_scanoss__common__pb2.EchoRequest.SerializeToString,
            scanoss_dot_api_dot_common_dot_v2_dot_scanoss__common__pb2.EchoResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetIssues(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/scanoss.api.semgrep.v2.Semgrep/GetIssues',
            scanoss_dot_api_dot_common_dot_v2_dot_scanoss__common__pb2.PurlRequest.SerializeToString,
            scanoss_dot_api_dot_semgrep_dot_v2_dot_scanoss__semgrep__pb2.SemgrepResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
