#
# Copyright 2017 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
This facade handles kafka-formatted messages from the Core, extracts the kafka
formatting and forwards the request to the concrete handler.
"""
import structlog
from twisted.internet.defer import inlineCallbacks
from zope.interface import implementer

from pyvoltha_min.adapters.interface import IAdapterInterface
from voltha_protos.inter_container_pb2 import IntType, InterAdapterMessage, StrType, Error, ErrorCode
from voltha_protos.device_pb2 import Device, Port, ImageDownload, SimulateAlarmRequest, PmConfigs
from voltha_protos.openflow_13_pb2 import FlowChanges, FlowGroups, Flows, \
    FlowGroupChanges, ofp_packet_out
from voltha_protos.voltha_pb2 import OmciTestRequest, FlowMetadata
from pyvoltha_min.adapters.kafka.kafka_inter_container_library import  get_messaging_proxy, \
    ARG_FROM_TOPIC

log = structlog.get_logger()


class MacAddressError(BaseException):
    def __init__(self, error):
        self.error = error


class IDError(BaseException):
    def __init__(self, error):
        self.error = error


@implementer(IAdapterInterface)
class AdapterRequestFacade:
    """
    Gate-keeper between CORE and device adapters.

    On one side it interacts with Core's internal model and update/dispatch
    mechanisms.

    On the other side, it interacts with the adapters standard interface as
    defined in
    """

    def __init__(self, adapter, core_proxy):
        self.adapter = adapter
        self.core_proxy = core_proxy

    @inlineCallbacks
    def start(self):
        log.debug('starting')

    @inlineCallbacks
    def stop(self):
        log.debug('stopping')

    # @inlineCallbacks
    # def createKafkaDeviceTopic(self, deviceId):
    #     log.debug("subscribing-to-topic", device_id=deviceId)
    #     kafka_proxy = get_messaging_proxy()
    #     device_topic = kafka_proxy.get_default_topic() + "_" + deviceId
    #     # yield kafka_proxy.create_topic(topic=device_topic)
    #     yield kafka_proxy.subscribe(topic=device_topic, group_id=device_topic, target_cls=self, offset=KAFKA_OFFSET_EARLIEST)
    #     log.debug("subscribed-to-topic", topic=device_topic)

    def start_omci_test(self, device, omcitestrequest, **_kwargs):
        if not device:
            return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                reason="device-invalid")
        if not omcitestrequest:
            return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                reason="omcitestrequest-invalid")

        d = Device()
        device.Unpack(d)
        omci_test = OmciTestRequest()
        omcitestrequest.Unpack(omci_test)
        result = self.adapter.start_omci_test(d, omci_test.uuid)
        return True, result

    def adopt_device(self, device, **kwargs):
        d = Device()
        if device:
            device.Unpack(d)

            # Update the core reference for that device as it will be used
            # by the adapter to send async messages to the Core.
            if ARG_FROM_TOPIC in kwargs:
                t = StrType()
                kwargs[ARG_FROM_TOPIC].Unpack(t)
                # Update the core reference for that device
                self.core_proxy.update_device_core_reference(d.id, t.val)

            # # Start the creation of a device specific topic to handle all
            # # subsequent requests from the Core. This adapter instance will
            # # handle all requests for that device.
            # reactor.callLater(0, self.createKafkaDeviceTopic, d.id)

            result = self.adapter.adopt_device(d)
            # return True, self.adapter.adopt_device(d)

            return True, result

        return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                            reason="device-invalid")

    def get_ofp_device_info(self, device, **_kwargs):
        d = Device()
        if device:
            device.Unpack(d)
            return True, self.adapter.get_ofp_device_info(d)

        return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                            reason="device-invalid")

    def reconcile_device(self, device, **_kwargs):
        d = Device()
        if device:
            device.Unpack(d)
            return True, self.adapter.reconcile_device(d)

        return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                            reason="device-invalid")

    def abandon_device(self, device, **_kwargs):
        return self.adapter.abandon_device(device)

    def disable_device(self, device, **_kwargs):
        d = Device()
        if device:
            device.Unpack(d)
            return True, self.adapter.disable_device(d)

        return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                            reason="device-invalid")

    def reenable_device(self, device, **_kwargs):
        d = Device()
        if device:
            device.Unpack(d)
            return True, self.adapter.reenable_device(d)

        return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                            reason="device-invalid")

    def reboot_device(self, device, **_kwargs):
        d = Device()
        if device:
            device.Unpack(d)
            return True, self.adapter.reboot_device(d)

        return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                            reason="device-invalid")

    def update_pm_config(self, device, pm_configs, **_kwargs):
        d = Device()
        if device:
            device.Unpack(d)
        else:
            return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                reason="device-invalid")
        pm = PmConfigs()
        if pm_configs:
            pm_configs.Unpack(pm)

        return True, self.adapter.update_pm_config(d, pm)

    def download_image(self, device, request, **_kwargs):
        d = Device()
        if device:
            device.Unpack(d)
        else:
            return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                reason="device-invalid")
        img = ImageDownload()
        if request:
            request.Unpack(img)
        else:
            return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                reason="port-no-invalid")

        return True, self.adapter.download_image(device, request)

    def get_image_download_status(self, device, request, **_kwargs):
        d = Device()
        if device:
            device.Unpack(d)
        else:
            return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                reason="device-invalid")
        img = ImageDownload()
        if request:
            request.Unpack(img)
        else:
            return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                reason="port-no-invalid")

        return True, self.adapter.get_image_download_status(device, request)

    def cancel_image_download(self, device, request, **_kwargs):
        d = Device()
        if device:
            device.Unpack(d)
        else:
            return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                reason="device-invalid")
        img = ImageDownload()
        if request:
            request.Unpack(img)
        else:
            return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                reason="port-no-invalid")

        return True, self.adapter.cancel_image_download(device, request)

    def activate_image_update(self, device, request, **_kwargs):
        d = Device()
        if device:
            device.Unpack(d)
        else:
            return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                reason="device-invalid")
        img = ImageDownload()
        if request:
            request.Unpack(img)
        else:
            return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                reason="port-no-invalid")

        return True, self.adapter.activate_image_update(device, request)

    def revert_image_update(self, device, request, **_kwargs):
        d = Device()
        if device:
            device.Unpack(d)
        else:
            return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                reason="device-invalid")
        img = ImageDownload()
        if request:
            request.Unpack(img)
        else:
            return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                reason="port-no-invalid")

        return True, self.adapter.revert_image_update(device, request)

    def enable_port(self, deviceId, port, **_kwargs):
        if not deviceId:
            return False, Error(code=ErrorCode.INVALID_PARAMETER,
                                reason="device-id")
        if not port:
            return False, Error(code=ErrorCode.INVALID_PARAMETER,
                                reason="port-invalid")
        t = StrType()
        deviceId.Unpack(t)
        p = Port()
        port.Unpack(p)

        return True, self.adapter.enable_port(t.val, p.port_no)

    def disable_port(self, deviceId, port, **_kwargs):
        if not deviceId:
            return False, Error(code=ErrorCode.INVALID_PARAMETER,
                                reason="device-id")
        if not port:
            return False, Error(code=ErrorCode.INVALID_PARAMETER,
                                reason="port-invalid")
        t = StrType()
        deviceId.Unpack(t)
        p = Port()
        port.Unpack(p)

        return True, self.adapter.disable_port(t.val, p.port_no)

    def child_device_lost(self, pDeviceId, pPortNo, onuID, **_kwargs):
        if not pDeviceId:
            return False, Error(code=ErrorCode.INVALID_PARAMETER,
                                reason="device-id")
        if not pPortNo:
            return False, Error(code=ErrorCode.INVALID_PARAMETER,
                                reason="p-port-no")
        if not onuID:
            return False, Error(code=ErrorCode.INVALID_PARAMETER,
                                reason="onu-id")
        t = StrType()
        pDeviceId.Unpack(t)

        port_no = IntType()
        pPortNo.Unpack(port_no)

        oid = IntType()
        onuID.Unpack(oid)

        return True, self.adapter.child_device_lost(t.val, port_no.val, oid.val)

    def self_test(self, device, **_kwargs):
        return self.adapter.self_test_device(device)

    def delete_device(self, device, **_kwargs):
        d = Device()
        if device:
            device.Unpack(d)
            result = self.adapter.delete_device(d)
            # return (True, self.adapter.delete_device(d))

            # Before we return, delete the device specific topic as we will no
            # longer receive requests from the Core for that device
            kafka_proxy = get_messaging_proxy()
            device_topic = kafka_proxy.get_default_topic() + "/" + d.id
            kafka_proxy.unsubscribe(topic=device_topic)

            return True, result

        return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                            reason="device-invalid")

    def get_device_details(self, device, **_kwargs):
        return self.adapter.get_device_details(device)

    def update_flows_bulk(self, device, flows, groups, **_kwargs):
        d = Device()
        if device:
            device.Unpack(d)
        else:
            return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                reason="device-invalid")
        f = Flows()
        if flows:
            flows.Unpack(f)

        g = FlowGroups()
        if groups:
            groups.Unpack(g)

        return True, self.adapter.update_flows_bulk(d, f, g)

    def update_flows_incrementally(self, device, flow_changes, group_changes, flow_metadata, **_kwargs):
        dev = Device()
        if device:
            device.Unpack(dev)
        else:
            return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                reason="device-invalid")
        flows = FlowChanges()
        if flow_changes:
            flow_changes.Unpack(flows)

        groups = FlowGroupChanges()
        if group_changes:
            group_changes.Unpack(groups)

        metadata = FlowMetadata()
        if flow_metadata:
            flow_metadata.Unpack(metadata)

        return True, self.adapter.update_flows_incrementally(dev, flows, groups, metadata)

    def suppress_event(self, event_filter, **_kwargs):
        return self.adapter.suppress_event(event_filter)

    def unsuppress_event(self, event_filter, **_kwargs):
        return self.adapter.unsuppress_event(event_filter)

    def process_inter_adapter_message(self, msg, **_kwargs):
        m = InterAdapterMessage()
        if msg:
            msg.Unpack(m)
        else:
            return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                reason="msg-invalid")
        log.debug('rx-message', message=m)
        # max_retry = 0
        # TODO: NOTE as per VOL-3223 a race condition on ONU_IND_REQUEST may occur,
        #       so if that's the message retry up to 10 times was the old way to handle
        #       this.  In tibit adapter, I am pausing 1 second but plan to watch admin_state
        #       for it to exit PREPROVISIONING and go to ENABLED to indicate 'adopt' was received from core
        return True, self.adapter.process_inter_adapter_message(m)

    def receive_packet_out(self, deviceId, outPort, packet, **_kwargs):
        try:
            d_id = StrType()
            if deviceId:
                deviceId.Unpack(d_id)
            else:
                return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                    reason="device-id-invalid")
            op = IntType()
            if outPort:
                outPort.Unpack(op)
            else:
                return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                    reason="outport-invalid")

            p = ofp_packet_out()
            if packet:
                packet.Unpack(p)
            else:
                return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                    reason="packet-invalid")

            return True, self.adapter.receive_packet_out(d_id.val, op.val, p)

        except Exception as e:
            log.exception("error-processing-receive_packet_out", e=e)

    def simulate_alarm(self, device, request, **_kwargs):
        d = Device()
        if device:
            device.Unpack(d)
        else:
            return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                reason="device-invalid")
        req = SimulateAlarmRequest()
        if request:
            request.Unpack(req)
        else:
            return False, Error(code=ErrorCode.INVALID_PARAMETERS,
                                reason="simulate-alarm-request-invalid")

        return True, self.adapter.simulate_alarm(d, req)
