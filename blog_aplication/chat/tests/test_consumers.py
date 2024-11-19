from channels.testing import ChannelsLiveServerTestCase
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from chat.models import RoomMessage, PrivateChat, PrivateMessage
from posts.models import Category


class ChatConsumerTestCase(ChannelsLiveServerTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.category = Category.objects.create(name="TestCategory", description="Test Description")
        self.private_chat = PrivateChat.objects.create(user1=self.user, user2=User.objects.create(username="otheruser"))

        self.group_ws_url = f"ws://{self.live_server_url}/ws/chat/group/{self.category.name}/"
        self.private_ws_url = f"ws://{self.live_server_url}/ws/chat/private/{self.private_chat.id}/"

    def test_group_chat_connection(self):
        communicator = self._connect_websocket(self.group_ws_url)
        connected, _ = self._start_communicator(communicator)
        self.assertTrue(connected)
        communicator.disconnect()

    def test_private_chat_connection(self):
        communicator = self._connect_websocket(self.private_ws_url)
        connected, _ = self._start_communicator(communicator)
        self.assertTrue(connected)
        communicator.disconnect()

    def test_send_group_message(self):
        communicator = self._connect_websocket(self.group_ws_url)
        self._start_communicator(communicator)

        message = {"message": "Hello Group Chat!"}
        async_to_sync(communicator.send_json_to)(message)

        response = async_to_sync(communicator.receive_json_from)()
        self.assertEqual(response["message"], message["message"])
        self.assertEqual(RoomMessage.objects.count(), 1)
        communicator.disconnect()

    def test_send_private_message(self):
        communicator = self._connect_websocket(self.private_ws_url)
        self._start_communicator(communicator)

        message = {"message": "Hello Private Chat!"}
        async_to_sync(communicator.send_json_to)(message)

        response = async_to_sync(communicator.receive_json_from)()
        self.assertEqual(response["message"], message["message"])
        self.assertEqual(PrivateMessage.objects.count(), 1)
        communicator.disconnect()

    def _connect_websocket(self, url):
        from channels.testing import WebsocketCommunicator
        from django.core.asgi import get_asgi_application

        application = get_asgi_application()
        return WebsocketCommunicator(application, url)

    def _start_communicator(self, communicator):
        return async_to_sync(communicator.connect)()