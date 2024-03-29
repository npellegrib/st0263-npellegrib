# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import file_service_pb2 as file__service__pb2


class FileServiceStub(object):
    """El servicio gRPC para la búsqueda, transferencia y descubrimiento de archivos entre peers
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SearchFile = channel.unary_unary(
                '/fileshare.FileService/SearchFile',
                request_serializer=file__service__pb2.SearchRequest.SerializeToString,
                response_deserializer=file__service__pb2.SearchResponse.FromString,
                )
        self.DownloadFile = channel.unary_unary(
                '/fileshare.FileService/DownloadFile',
                request_serializer=file__service__pb2.DownloadRequest.SerializeToString,
                response_deserializer=file__service__pb2.DownloadResponse.FromString,
                )
        self.DiscoverPeers = channel.unary_unary(
                '/fileshare.FileService/DiscoverPeers',
                request_serializer=file__service__pb2.DiscoverRequest.SerializeToString,
                response_deserializer=file__service__pb2.DiscoverResponse.FromString,
                )


class FileServiceServicer(object):
    """El servicio gRPC para la búsqueda, transferencia y descubrimiento de archivos entre peers
    """

    def SearchFile(self, request, context):
        """Solicita la búsqueda de un archivo en la red
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DownloadFile(self, request, context):
        """Solicita la descarga de un archivo específico
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DiscoverPeers(self, request, context):
        """Solicita información de peers para el descubrimiento de nuevos peers
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FileServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SearchFile': grpc.unary_unary_rpc_method_handler(
                    servicer.SearchFile,
                    request_deserializer=file__service__pb2.SearchRequest.FromString,
                    response_serializer=file__service__pb2.SearchResponse.SerializeToString,
            ),
            'DownloadFile': grpc.unary_unary_rpc_method_handler(
                    servicer.DownloadFile,
                    request_deserializer=file__service__pb2.DownloadRequest.FromString,
                    response_serializer=file__service__pb2.DownloadResponse.SerializeToString,
            ),
            'DiscoverPeers': grpc.unary_unary_rpc_method_handler(
                    servicer.DiscoverPeers,
                    request_deserializer=file__service__pb2.DiscoverRequest.FromString,
                    response_serializer=file__service__pb2.DiscoverResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'fileshare.FileService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FileService(object):
    """El servicio gRPC para la búsqueda, transferencia y descubrimiento de archivos entre peers
    """

    @staticmethod
    def SearchFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fileshare.FileService/SearchFile',
            file__service__pb2.SearchRequest.SerializeToString,
            file__service__pb2.SearchResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DownloadFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fileshare.FileService/DownloadFile',
            file__service__pb2.DownloadRequest.SerializeToString,
            file__service__pb2.DownloadResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DiscoverPeers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fileshare.FileService/DiscoverPeers',
            file__service__pb2.DiscoverRequest.SerializeToString,
            file__service__pb2.DiscoverResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
