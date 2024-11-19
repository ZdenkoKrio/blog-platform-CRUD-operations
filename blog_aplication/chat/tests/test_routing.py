from channels.testing import ChannelsLiveServerTestCase
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.urls import reverse
from django.contrib.auth.models import User


class ChatConsumerTestCase(ChannelsLiveServerTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.chat_type = "group"
        self.chat_id = "1"
        self.ws_url = f"ws://{self.live_server_url}/ws/chat/{self.chat_type}/{self.chat_id}/"

    def test_websocket_connection(self):
        communicator = self._connect_websocket()
        connected, subprotocol = self._start_communicator(communicator)
        self.assertTrue(connected)
        communicator.disconnect()

    def test_websocket_message_send_receive(self):
        communicator = self._connect_websocket()
        connected, subprotocol = self._start_communicator(communicator)
        self.assertTrue(connected)

        test_message = {"type": "chat.message", "message": "Hello, WebSocket!"}

        async_to_sync(communicator.send_json_to)(test_message)
        response = async_to_sync(communicator.receive_json_from)()

        self.assertEqual(response["message"], test_message["message"])
        communicator.disconnect()

    def _connect_websocket(self):
        from channels.testing import WebsocketCommunicator
        from django.core.asgi import get_asgi_application

        application = get_asgi_application()
        return WebsocketCommunicator(application, self.ws_url)

    def _start_communicator(self, communicator):
        return async_to_sync(communicator.connect)()