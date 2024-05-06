# test the serializer viewset
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from apps.event.models import Event
from apps.event.serializers import EventSerializer
from apps.event.views import EventViewSet


class EventViewSetTestCase(APITestCase):
    def setUp(self):
        self.event = Event.objects.create(
            title="Test Event",
            description="Test Event Description",
            date="2021-12-12",
            time="12:00:00",
            time_zone="UTC",
            location="Test Location",
            image="event/images/test.jpg"
        )
        self.serializer = EventSerializer(instance=self.event)
        self.view = EventViewSet()
        self.view.query_set = Event.objects.all()
        self.view.serializer_class = EventSerializer

    def test_create_event(self):
        data = {
            "title": "Test Event",
            "description": "Test Event Description",
            "date": "2021-12-12",
            "time": "12:00:00",
            "time_zone": "UTC",
            "location": "Test Location",
            "image": "event/images/test.jpg"
        }
        request = self.client.post(reverse("event-create"), data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_update_event(self):
        data = {
            "title": "Test Event",
            "description": "Test Event Description",
            "date": "2021-12-12",
            "time": "12:00:00",
            "time_zone": "UTC",
            "location": "Test Location",
            "image": "event/images/test.jpg"
        }
        request = self.client.put(reverse("event-update", kwargs={"pk": self.event.pk}), data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_delete_event(self):
        request = self.client.delete(reverse("event-delete", kwargs={"pk": self.event.pk}))
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_retrieve_event(self):
        request = self.client.get(reverse("event-retrieve", kwargs={"pk": self.event.pk}))
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_list_event(self):
        request = self.client.get(reverse("event-list"))
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_event_serializer(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(["id", "title", "description", "date", "time", "time_zone", "location", "image"])
        )
        self.assertEqual(data["title"], "Test Event")
        self.assertEqual(data["description"], "Test Event Description")
        self.assertEqual(data["date"], "2021-12-12")
        self.assertEqual(data["time"], "12:00:00")
        self.assertEqual(data["time_zone"], "UTC")
        self.assertEqual(data["location"], "Test Location")
        self.assertEqual(data["image"], "event/images/test.jpg")