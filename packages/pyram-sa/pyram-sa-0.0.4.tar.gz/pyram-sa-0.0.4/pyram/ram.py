"""
Copyright (C) Kehtra Pty Ltd - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""
import os
from datetime import datetime, timedelta
from typing import Union

from .decorators import refresh_token
from zeep import Client as zeep_client
from zeep.transports import Transport
from zeep.cache import InMemoryCache


class Ram:

    __slots__ = ['uploads_client', 'tracking_client', 'tsm_client', 'user_id', 'password', 'token', 'expiry', 'expiry_delta']

    def __init__(self, user_id=None, password=None):

        transport = Transport(cache=InMemoryCache(timeout=(3600 * 24)))
        self.uploads_client = zeep_client('http://41.21.176.123/RAMConnectV2/Uploads/CustomerPortalWS.asmx?WSDL',
                                          transport=transport)
        self.tracking_client = zeep_client('http://services.ramgroup.co.za/ramconnectv2/Tracking/TrackingWS.asmx?WSDL',
                                           transport=transport)
        self.tsm_client = zeep_client('http://41.21.176.123/ramconnectv2/Tracking/ServiceMessagesWS.asmx?WSDL',
                                      transport=transport)
        self.user_id = user_id or os.environ.get('RAM_USER_ID')
        self.password = password or os.environ.get('RAM_PASSWORD')
        token = self.uploads_client.service.Logon(user_id, password)
        if token is None:
            raise
        self.token = token
        self.expiry = datetime.now() + timedelta(minutes=20)
        self.expiry_delta = 60 * 2

    def __str__(self) -> str:
        return str(['{}: {}'.format(k, v) for k, v in locals()])

    @refresh_token
    def logon(self, *args, **_) -> None:
        """
        Returns token to be used in further requests
        """
        if args is not None or len(args) == 0:
            res = self.uploads_client.service.Logon(*args)
            if res is not None:
                self.token = res
                self.token = self.uploads_client.service.Logon(self.user_id, self.password)
                self.expiry = datetime.now() + timedelta(minutes=20)
            else:
                raise
        else:
            self.token = self.uploads_client.service.Logon(self.user_id, self.password)
            self.expiry = datetime.now() + timedelta(minutes=20)

    @refresh_token
    def user_session_valid(self, *args, **_) -> bool:
        """
        Checks if the token associated with the current session is valid.
        :param args:
        :param _:
        :return:
        """
        return self.uploads_client.service.UserSessionValid(self.user_id, self.token, *args)

    @refresh_token
    def consignment_id_from_shipper_reference(self, *args, **_) -> str:
        """
        Retrieves the consignment ID associated with a shipper reference.
        :param args:
        :param _:
        :return:
        """
        return self.uploads_client.service.ConsignmentID_FromShipperReference(self.user_id, self.token, *args)

    @refresh_token
    def label_xml(self, *args, **_) -> object:
        """

        :param args:
        :param _:
        :return:
        """
        return self.uploads_client.service.Label_XML(self.user_id, self.token, *args)

    @refresh_token
    def upload_collection_request(self, *args, **_) -> str:
        """

        :param args:
        :param _:
        :return:
        """
        return self.uploads_client.service.Upload_CollectionRequest(self.user_id, self.token, *args)

    @refresh_token
    def suburb_search(self, *args, **_) -> object:
        """
        Performs a suburb search given a query and a maximum number of records to return
        :param args:
        :param _:
        :return:
        """
        return self.uploads_client.service.SuburbSearch(self.user_id, self.token, *args)

    @refresh_token
    def upload_consignment_get_by_status(self, *args, **_) -> object:
        """

        :param args:
        :param _:
        :return:
        """
        return self.uploads_client.service.Upload_Consignment_GetByStatus(self.user_id, self.token, *args)

    @refresh_token
    def upload_consignment_get_status(self, *args, **_) -> object:
        """

        :param args:
        :param _:
        :return:
        """
        return self.uploads_client.service.Upload_Consignment_GetStatus(self.user_id, self.token, *args)

    @refresh_token
    def upload_consignment(self, *args, **_) -> int:
        """

        :param args:
        :param _:
        :return:
        """
        return self.uploads_client.service.Upload_Consignment(self.user_id, self.token, *args)

    @refresh_token
    def upload_consignment_minimal(self, *args, **_) -> int:
        """

        :param args:
        :param _:
        :return:
        """
        return self.uploads_client.service.Upload_Consignment_Minimal(self.user_id, self.token, *args)

    @refresh_token
    def upload_consignment_specify_sender(self, *args, **_) -> int:
        """

        :param args:
        :param _:
        :return:
        """
        return self.uploads_client.service.Upload_Consignment_SpecifySender(self.user_id, self.token, *args)

    @refresh_token
    def upload_consignment_including_parcels(self, *args, **_) -> int:
        """

        :param args:
        :param _:
        :return:
        """
        return self.uploads_client.service.Upload_ConsignmentInclParcels(self.user_id, self.token, *args)

    @refresh_token
    def upload_consignment_including_parcels_minimal(self, *args, **_) -> int:
        """

        :param args:
        :param _:
        :return:
        """
        return self.uploads_client.service.Upload_ConsignmentInclParcels_Minimal(self.user_id, self.token, *args)

    @refresh_token
    def upload_consignment_including_parcels_specify_sender(self, *args, **_) -> int:
        """

        :param args:
        :param _:
        :return:
        """
        return self.uploads_client.service.Upload_ConsignmentInclParcels_SpecifySender(self.user_id, self.token, *args)

    @refresh_token
    def upload_parcel(self, *args, **_) -> bool:
        """

        :param args:
        :param _:
        :return:
        """
        return self.uploads_client.service.Upload_Parcel(self.user_id, self.token, *args)

    @refresh_token
    def waybill(self, *args, **_) -> Union[str, None]:
        """

        :param args:
        :param _:
        :return:
        """
        return self.uploads_client.service.Waybill(self.user_id, self.token, *args)

    @refresh_token
    def waybill_ext(self, *args, **_):
        """
        :param args: consignmentID, waybillType, waybillCopies, printParcelReports
        :param _:
        :return:
        """
        return self.uploads_client.service.Waybill_Ext(self.user_id, self.token, *args)

    @refresh_token
    def waybill_from_shipper_reference(self, *args, **_) -> Union[str, None]:
        """

        :param args:
        :param _:
        :return:
        """
        return self.uploads_client.service.Waybill_FromShipperReference(self.user_id, self.token, *args)

    """
    --------------------------
    Fields returned per record
    --------------------------
    
    DateTime            datetime            Time of the track event
    TrackType           string              Type of track – see list
    Hub                 string              Which hub it was tracked in
    Description         string              Human readable tracking details
    Driver              string              Responsible driver
    ConsignmentStatus   string              Current status of consignment
    """

    def consignment_tracking(self, *args, **_):
        """
        track using the unique ConsignmentID of the consignment.
        :return:
        """
        return self.uploads_client.service.ConsignmentTracking(self.user_id, self.token, *args)

    def consignment_tracking_by_shipper_reference(self, *args, **_):
        """
         track using the client’s own reference.
        :return:
        """
        return self.uploads_client.service.ConsignmentTrackingByShipperReference(self.user_id, self.token, *args)

    @refresh_token
    def generic_messages_get_batch(self, *args, **_) -> object:
        """

        :param args:
        :param _:
        :return:
        """
        return self.tsm_client.service.GenericMessages_GetBatch(self.user_id, self.token)

    @refresh_token
    def generic_messages_get_batch_typed(self, *args, **_) -> object:
        """
        Get the next batch of tracking and status messages. The return value will be strongly typed.
        This call has to be followed by a call to GenericMessages_UpdateBatch to confirm batch download success.
        Please note that Message elements might in future contain extra attributes.
        :return:
        """
        return self.tsm_client.service.GenericMessages_GetBatch_Typed(self.user_id, self.token)

    @refresh_token
    def generic_messages_update_batch(self, *args, **_) -> bool:
        """
        Confirm the download status of the batch
        :param args: BatchID, SendResult, Success, Failed
        :return:
        """
        return self.tsm_client.service.GenericMessages_UpdateBatch(self.user_id, self.token, *args)

    @refresh_token
    def pod_images_as_pdf(self, *args, **_) -> any:
        """
        Retrieve all the POD images for a consignment as a single PDF.
        :param args:
        :return:
        """
        return self.tsm_client.service.PODImagesAsPDF(self.user_id, self.token, *args)

    # tracking

    @refresh_token
    def consignment_details(self, *args):
        """
        Retrieves consignment details by a consignment id
        :param args: [consignment_id]
        :return: List
        """
        return self.tracking_client.service.ConsignmentDetails(self.user_id, self.token, *args)

    @refresh_token
    def consignment_details_by_shipper_reference(self, *args):
        """
        Returns consignment information using the shipper reference as a key
        :param args: [shipper_reference: str]
        :return:
        """
        return self.tracking_client.service.ConsignmentDetailsByShipperReference(self.user_id, self.token, *args)

    @refresh_token
    def consignments_consigned_by_day(self, *args):
        """

        :param args: day: DateTime
        :return:
        """
        return self.tracking_client.service.ConsignmentsConsignedByDay(self.user_id, self.token, *args)

    @refresh_token
    def consignments_delivered_by_day(self, *args):
        """

        :param args: day: DateTime
        :return:
        """
        return self.tracking_client.service.ConsignmentsDeliveredByDay(self.user_id, self.token, *args)

    @refresh_token
    def consignments_tracking_status(self, *args):
        """

        :param args: consignment_ids: [str]
        :return:
        """
        return self.tracking_client.service.ConsignmentsTrackingStatus(self.user_id, self.token, *args)

    @refresh_token
    def consignments_tracking_status_by_shipper_references(self, *args):
        """

        :param args: shipper_references: [str]
        :return:
        """
        return self.tracking_client.service.ConsignmentsTrackingStatusByShipperReferences(self.user_id, self.token,
                                                                                          *args)

    @refresh_token
    def consignment_tracking(self, *args):
        """

        :param args: consignment_id: str
        :return:
        """
        return self.tracking_client.service.ConsignmentTracking(self.user_id, self.token, *args)

    @refresh_token
    def consignment_tracking_by_shipper_reference(self, *args):
        """

        :param args: shipper_reference: str
        :return:
        """
        return self.tracking_client.service.ConsignmentTrackingByShipperReference(self.user_id, self.token, *args)

    @refresh_token
    def get_quote_v3(self, *args):
        """

        :param args: billed_to, service_type_code, sender_zone_id, saturday_surcharge, after_hours_surcharge, insured,
        insured_value, armoured_vehicle, face_to_face_surcharge, weight, length, breadth, height, no_of_cards
        :return:
        """
        return self.tracking_client.service.GetQuoteV3(self.user_id, self.token, *args)

    @refresh_token
    def pod_image(self, *args):
        """
        Retrieves a POD image given a fragment ID
        :param args: fragment_id
        :return: POD image as byte array
        """
        return self.tracking_client.service.PODImage(self.user_id, self.token, *args)

    @refresh_token
    def pod_image_by_index(self, *args):
        """

        :param args: consignment_id, image_index
        :return: POD image as byte array
        """
        return self.tracking_client.service.PODImageByIndex(self.user_id, self.token, *args)

    @refresh_token
    def pod_images(self, *args):
        """
        retrieves a set of POD images given a consignment_id
        :param args: consignment_id
        :return: POD images as two-dimensional array
        """
        return self.tracking_client.service.PODImages(self.user_id, self.token, *args)

    @refresh_token
    def pod_images_list(self, *args):
        """
        Returns a list of POD images associated with a consignment_id
        :param args: consignment_id
        :return: XMLNode ??
        """
        return self.tracking_client.service.PODImagesList(self.user_id, self.token, *args)

    @refresh_token
    def suburbs_download(self, *args):
        """
        Returns a paginated list of suburbs stored on the RAM system
        :param args:
        :return:
        """
        return self.tracking_client.service.SuburbsDownload(self.user_id, self.token, *args)

    @refresh_token
    def suburb_search(self, *args):
        """

        :param args:
        :return:
        """
        return self.tracking_client.service.SuburbSearch(self.user_id, self.token, *args)
