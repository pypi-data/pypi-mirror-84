# https://github.com/sacOO7/socketcluster-client-python
from socketclusterclient import Socketcluster
# https://github.com/titouandk/emitter.py
from emitter import Emitter

from uuid import uuid4
from threading import Thread, Lock
from . import constants
from . import proto
from . import __version__
import os
from google.protobuf import message as _message
import base64
import traceback
import time
import socket as sock
import json
import re
from inspect import signature
from typing import Union


# The "official" socketcluster client doesn't respond to ping... let's fix that

class FixedSocketClusterClient(Socketcluster.socket):

    def on_message(self, ws, message):
        if message == "#1": ws.send("#2")
        return super().on_message(ws, message)


class RTI(Emitter):

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state
        if self.connected and not self.incognito:
            self._publish_state()

    @property
    def own_channel_prefix(self):
        return f"@{self.instance_id}:"

    def __init__(self, application_id="python", application_version=None, instance_id=None, federation_id=None, secret=None, user=None, password=None, incognito=False, connect=True):
        super().__init__()

        self.measurement_interval_time_scale = 1

        self.subscriptions = {}
        self.known_channels = {}
        self.used_channels = {}
        self.known_clients = {}
        self.used_metrics = {}
        self.known_metrics = {}

        self._state = proto.UNKNOWN
        self.connected = False
        self.cluster_version = None

        url = None
        if not url:
            url = os.environ.get('GEISTT_RTI_URL')
        if not url:
            url = constants.default_url
        self.url = url

        self.application_id = application_id
        self.application_version = application_version
        self.instance_id = instance_id
        if not self.instance_id: self.instance_id = str(uuid4())
        self.federation_id = federation_id
        if not self.federation_id: self.federation_id = os.environ.get('GEISTT_RTI_FEDERATION')
        if self.federation_id: self.federation_id = self.federation_id.replace("/", "_") # slashes quietly not allowed in federation id

        auth_secret = None
        if not auth_secret: auth_secret = os.environ.get('GEISTT_RTI_SECRET')
        if not auth_secret: auth_secret = secret
        self.user = user

        self._host = os.environ.get('GEISTT_RTI_HOST')
        if not self._host: self._host = sock.gethostname()
        self._station = os.environ.get('GEISTT_RTI_STATION')

        self.incognito = incognito

        auth_token = {
            'applicationId': self.application_id,
            'instanceId': self.instance_id,
            'clientLibraryVersion': __version__
        }
        if auth_secret: auth_token['secret'] = auth_secret
        if user: auth_token['user'] = user
        if password: auth_token['password'] = password
        if self.federation_id:
            auth_token['federationId'] = self.federation_id

        socket = FixedSocketClusterClient(url)
        socket.setdelay(2)
        socket.setreconnection(True)

        def on_connect(socket):
            pass

        def on_disconnect(socket):
            self.connected = False
            self.emit("disconnect")

        def on_fail(socket, error):
            self.emit("error", "fail", error, None)

        def on_connection_error(socket, error):
            self.emit("error", "connection", error, None)

        def on_set_auth(socket, token):
            self.connected = True
            socket.setAuthtoken(token)
            self.subscribe(constants.clients_channel, proto.Clients, on_clients)
            self.subscribe(constants.channels_channel, proto.Channels, on_channels)
            self.subscribe(constants.metrics_channel, proto.Metrics, on_metrics)
            if self.federation_id:
                self.publish_text(constants.federations_channel, self.federation_id)
                self.subscribe_text(constants.federations_channel, on_federations)
            for channel_name in self.subscriptions:
                socket.subscribe(channel_name)
            if not self.incognito:
                self._publish_client()
            self.emit("connect")

        def on_auth(socket, is_authenticated):
            socket.emit("auth", auth_token)

        def on_clients(message: proto.Clients):
            if message.HasField("request_clients") and not self.incognito:
                self._publish_client()
            elif message.HasField("client"):
                self.known_clients[message.client.instance_id] = message.client

        def on_channels(message: proto.Channels):
            if message.HasField("request_channel_usage"):
                message = proto.Channels()
                message.channel_usage.instance_id = self.instance_id
                message.channel_usage.usage.extend(self.used_channels.values())
                if not self.incognito:
                    self.publish(constants.channels_channel, message)
            elif message.HasField("channel_usage"):
                for use in message.channel_usage.usage:
                    self.known_channels[use.channel.name] = use.channel
            elif message.HasField("channel"):
                self.known_channels[message.channel.name] = message.channel

        def on_metrics(message: proto.Metrics):
            if message.HasField("request_metrics") and not self.incognito:
                self._publish_metrics()
            elif message.HasField("metric"):
                self.known_metrics[message.metric.id] = message.metric

        def on_federations(message: str):
            if message == "?":
                self.publish_text(
                    constants.federations_channel, self.federation_id)

        def on_cluster_version(channel: str, content: str):
            self.cluster_version = content

        socket.setBasicListener(on_connect, on_disconnect, on_connection_error)
        socket.setAuthenticationListener(on_set_auth, on_auth)
        socket.on("fail", on_fail)
        socket.on("cluster-version", on_cluster_version)
        self.socket = socket
        self.thread = None
        self.collect_measurements_thread = None
        self.collect_lock = Lock()
        self.collect_queue = {}
        self.last_collect = {}
        if connect:
            self.connect()

    def connect(self):
        self.thread = Thread(target=self.socket.connect)
        self.thread.daemon = True
        self.thread.start()

    def disconnect(self):
        self.socket.disconnect()
        self.connected = False
        self.emit("disconnect")

    def wait_until_connected(self):
        count = 0
        while count < 500 and not self.connected:
            count += 1
            time.sleep(0.01)
        return self.connected

    def subscribe(self, channel_name: str, message_class, handler):
        def handle_message(content):
            message = self.parse(message_class, content)
            if len(signature(handler).parameters) < 2:
                handler(message)
            else:
                handler(channel_name, message)
        return self.subscribe_text(channel_name, handle_message, str(message_class))

    @classmethod
    def parse(cls, message_class, content):
        message = message_class()
        message.ParseFromString(base64.b64decode(content))
        return message


    def subscribe_json(self, channel_name: str, handler):
        def handle_message(content):
            if len(signature(handler).parameters) < 2:
                handler(json.loads(content))
            else:
                handler(channel_name, json.loads(content))
        return self.subscribe_text(channel_name, handle_message, "json")

    def subscribe_text(self, channel_name: str, handler, data_type="text"):
        socket_channel_name = channel_name
        if self.federation_id and channel_name != constants.federations_channel:
            socket_channel_name = "//" + self.federation_id + "/" + channel_name
        if (socket_channel_name not in self.subscriptions):
            if self.connected:
                self.socket.subscribe(socket_channel_name)
            self.subscriptions[socket_channel_name] = []
            self._register_channel(channel_name, False, data_type)

            def handle_message(in_channel_name, content):
                for listener in self.subscriptions[socket_channel_name]:
                    try:
                        if len(signature(listener).parameters) < 2:
                            listener(content)
                        else:
                            listener(channel_name, content)
                    except Exception as e:
                        self.emit("error", channel_name, e,
                                  traceback.format_exc())
            self.socket.onchannel(socket_channel_name, handle_message)

        self.subscriptions[socket_channel_name].append(handler)
        return handler

    def unsubscribe(self, channel_name_or_handler):
        if channel_name_or_handler is str:
            if self.federation_id and channel_name_or_handler != constants.federations_channel:
                channel_name_or_handler = "//" + self.federation_id + "/" + channel_name_or_handler
            self.socket.unsubscribe(channel_name_or_handler)
            if channel_name_or_handler in self.subscriptions:
                del self.subscriptions[channel_name_or_handler]
        else:
            for channel_name in self.subscriptions:
                if channel_name_or_handler in self.subscriptions[channel_name]:
                    self.subscriptions[channel_name].remove(channel_name_or_handler)
                    if len(self.subscriptions[channel_name]) <= 0:
                        self.socket.unsubscribe(channel_name)
                        del self.subscriptions[channel_name]
                        break

    def publish(self, channel_name: str, message: _message.Message):
        try:
            self._register_channel(channel_name, True, data_type=str(type(message)))
            content = base64.b64encode(
                message.SerializeToString()).decode("utf8")
            if self.federation_id and not channel_name.startswith("@"):
                channel_name = "//" + self.federation_id + "/" + channel_name
            self.socket.publish(channel_name, content)
        except Exception as e:
            print(e)

    def publish_text(self, channel_name: str, content: str):
        try:
            self._register_channel(channel_name, True, data_type="text")
            if self.federation_id and not channel_name.startswith("@") and channel_name != constants.federations_channel:
                channel_name = "//" + self.federation_id + "/" + channel_name
            self.socket.publish(channel_name, content)
        except Exception as e:
            print(e)
    
    def publish_json(self, channel_name: str, message: object):
        try:
            self._register_channel(channel_name, True, data_type="json")
            if self.federation_id and not channel_name.startswith("@") and channel_name != constants.federations_channel:
                channel_name = "//" + self.federation_id + "/" + channel_name
            self.socket.publish(channel_name, json.dumps(message))
        except Exception as e:
            print(e)


    def publish_error(self, error_message, runtime_state: proto.RuntimeState = None):
        message = proto.RuntimeControl()
        message.error.application_id = self.application_id
        message.error.instance_id = self.instance_id
        message.error.message = error_message
        if runtime_state is not None:
            message.error.state = runtime_state
        self.publish(constants.control_channel, message)

    def _publish_client(self):
        message = proto.Clients()
        message.client.application_id = self.application_id
        message.client.instance_id = self.instance_id
        message.client.state = self._state
        message.client.client_library_version = __version__
        if self.application_version:
            message.client.application_version = self.application_version
        if self._host:
            message.client.host = self._host
        if self._station:
            message.client.station = self._station
        if self.user:
            message.client.user = self.user
        self.publish(constants.clients_channel, message)

    def _publish_metrics(self):
        for metric in self.used_metrics.values():
            message = proto.Metrics()
            message.metric.CopyFrom(metric)
            self.publish(constants.metrics_channel, message)

    def _publish_state(self):
        message = proto.RuntimeControl()
        message.state.application_id = self.application_id
        message.state.instance_id = self.instance_id
        message.state.state = self._state
        self.publish(constants.control_channel, message)

    def _register_channel(self, channel_name, publish, data_type=None):
        if channel_name.startswith("@"): return
        channel = proto.Channels.Channel()
        channel.name = channel_name
        data_type = re.sub("<class.*_pb2\\.", "", data_type)
        data_type = re.sub("'>", "", data_type)
        channel.data_type = data_type
        use = None
        if channel_name not in self.used_channels:
            use = proto.Channels.ChannelUse()
            use.channel.CopyFrom(channel)
            self.used_channels[channel_name] = use
        else:
            use = self.used_channels[channel_name]
        if publish: use.publish = True
        else: use.subscribe = True
        if channel_name not in self.known_channels:
            self.known_channels[channel_name] = channel
            if self.connected and not self.incognito:
                message = proto.Channels()
                message.channel.CopyFrom(channel)
                self.publish(constants.channels_channel, message)

    def register_metric(self, metric):
        metric.application_id = self.application_id
        self.used_metrics[metric.id] = metric
        if metric.id not in self.known_metrics:
            self.known_metrics[metric.id] = metric
            if self.connected and not self.incognito:
                message = proto.Metrics()
                message.metric.CopyFrom(metric)
                self.publish(constants.metrics_channel, message)
    
    def measure(self, metric_id: Union[str, proto.Metrics.Metric], value: float):
        metric = None
        if type(metric_id) is str:
            metric = self.used_metrics.get(metric_id)
            if not metric: metric = self.known_metrics.get(metric_id)
            if not metric:
                metric = proto.Metrics.Metric()
                metric.id = metric_id
                metric.application_id = self.application_id
        else:
            metric = metric_id

        if metric.id not in self.used_metrics: self.register_metric(metric)
        if metric.interval > 1e-5:
            if not self.collect_measurements_thread: 
                self.collect_measurements_thread = Thread(target=self._collect_measurements_thread_func)
                self.collect_measurements_thread.daemon = True
                self.collect_measurements_thread.start()
            with self.collect_lock:
                if metric.id not in self.collect_queue: self.collect_queue[metric.id] = []
                self.collect_queue[metric.id].append(value)
        else:
            measurement = proto.Measurement()
            measurement.metric_id = metric.id
            measurement.instance_id = self.instance_id
            measurement.value = value
            channel = metric.channel if metric.channel else constants.measurement_channel
            if self.connected: self.publish(channel, measurement)
    
    def _collect_measurements_thread_func(self):
        while self.connected:
            time.sleep(0.1)
            with self.collect_lock:
                for metric_id, values in self.collect_queue.items():
                    if metric_id not in self.last_collect: 
                        self.last_collect[metric_id] = time.time()
                    else:
                        metric = self.known_metrics[metric_id]
                        if (time.time() - self.last_collect[metric_id]) * self.measurement_interval_time_scale > metric.interval:
                            channel = metric.channel if metric.channel else constants.measurement_channel
                            measurement = proto.Measurement()
                            measurement.metric_id = metric.id
                            measurement.instance_id = self.instance_id
                            if len(values) == 1:
                                measurement.value = values.pop()
                                self.publish(channel, measurement)
                            elif len(values) > 1:
                                window = proto.Measurement.Window()
                                window.max = -float("inf")
                                window.min = float("inf")
                                while len(values) > 0:
                                    value = values.pop()
                                    window.count += 1
                                    window.mean += value
                                    if value > window.max: window.max = value
                                    if value < window.min: window.min = value
                                if window.count > 0: window.mean /= window.count
                                window.duration = (time.time() - self.last_collect[metric_id]) * self.measurement_interval_time_scale
                                measurement.window.CopyFrom(window)
                                self.publish(channel, measurement)
                            self.last_collect[metric_id] = time.time()




