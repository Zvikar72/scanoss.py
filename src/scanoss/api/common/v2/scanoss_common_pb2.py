# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: scanoss/api/common/v2/scanoss-common.proto
"""Generated protocol buffer code."""

from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n*scanoss/api/common/v2/scanoss-common.proto\x12\x15scanoss.api.common.v2"T\n\x0eStatusResponse\x12\x31\n\x06status\x18\x01 \x01(\x0e\x32!.scanoss.api.common.v2.StatusCode\x12\x0f\n\x07message\x18\x02 \x01(\t"\x1e\n\x0b\x45\x63hoRequest\x12\x0f\n\x07message\x18\x01 \x01(\t"\x1f\n\x0c\x45\x63hoResponse\x12\x0f\n\x07message\x18\x01 \x01(\t"r\n\x0bPurlRequest\x12\x37\n\x05purls\x18\x01 \x03(\x0b\x32(.scanoss.api.common.v2.PurlRequest.Purls\x1a*\n\x05Purls\x12\x0c\n\x04purl\x18\x01 \x01(\t\x12\x13\n\x0brequirement\x18\x02 \x01(\t*`\n\nStatusCode\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\x12\x1b\n\x17SUCCEEDED_WITH_WARNINGS\x10\x02\x12\x0b\n\x07WARNING\x10\x03\x12\n\n\x06\x46\x41ILED\x10\x04\x42/Z-github.com/scanoss/papi/api/commonv2;commonv2b\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'scanoss.api.common.v2.scanoss_common_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z-github.com/scanoss/papi/api/commonv2;commonv2'
    _STATUSCODE._serialized_start = 336
    _STATUSCODE._serialized_end = 432
    _STATUSRESPONSE._serialized_start = 69
    _STATUSRESPONSE._serialized_end = 153
    _ECHOREQUEST._serialized_start = 155
    _ECHOREQUEST._serialized_end = 185
    _ECHORESPONSE._serialized_start = 187
    _ECHORESPONSE._serialized_end = 218
    _PURLREQUEST._serialized_start = 220
    _PURLREQUEST._serialized_end = 334
    _PURLREQUEST_PURLS._serialized_start = 292
    _PURLREQUEST_PURLS._serialized_end = 334
# @@protoc_insertion_point(module_scope)
