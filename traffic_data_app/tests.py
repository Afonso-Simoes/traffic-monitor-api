from rest_framework.test import APITestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.gis.geos import LineString
from .models import RoadSegment, TrafficReading


class APITests(APITestCase):
    """
    Base class for all API tests.
    Sets up a test user and test data.
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        Sets up the test data for the test suite.
        """
        # Create an admin user for creation/deletion tests
        cls.admin_user = User.objects.create_superuser(username='test_admin', email='admin@test.com', password='admin_password')
        
        # Create a regular user for read-only tests
        cls.regular_user = User.objects.create_user(username='test_user', email='user@test.com', password='user_password')

        # Create the road segments with geometry fields
        cls.segment_high_speed = RoadSegment.objects.create(
            name='High Speed Segment', length=100.0,
            geometry=LineString((0, 0), (1, 1))
        )
        cls.segment_medium_speed = RoadSegment.objects.create(
            name='Medium Speed Segment', length=100.0,
            geometry=LineString((2, 2), (3, 3))
        )
        cls.segment_low_speed = RoadSegment.objects.create(
            name='Low Speed Segment', length=100.0,
            geometry=LineString((4, 4), (5, 5))
        )
        cls.segment_no_reading = RoadSegment.objects.create(
            name='No Reading Segment', length=100.0,
            geometry=LineString((6, 6), (7, 7))
        )

        # Create traffic readings for the segments
        TrafficReading.objects.create(
            segment=cls.segment_high_speed, 
            speed_measured=65.0, 
            timestamp=timezone.now()
        )
        TrafficReading.objects.create(
            segment=cls.segment_medium_speed, 
            speed_measured=35.0, 
            timestamp=timezone.now()
        )
        TrafficReading.objects.create(
            segment=cls.segment_low_speed, 
            speed_measured=15.0, 
            timestamp=timezone.now()
        )


class RoadSegmentViewSetTests(APITests):
    """
    Tests for the RoadSegmentViewSet, including the characterization filter.
    """
    def setUp(self):
        # Authenticate as a superuser for permission tests
        self.client.force_authenticate(user=self.admin_user)

    def test_list_segments_with_serializer_fields(self):
        """Checks if the serializer returns the correct read-only fields."""
        url = reverse('roadsegment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('long_start', response.data['results'][0])
        self.assertIn('lat_start', response.data['results'][0])

    def test_filter_by_high_speed_characterization(self):
        """Checks if the API correctly filters for 'high_speed'."""
        url = reverse('roadsegment-list') + '?last_reading_characterization=high_speed'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], self.segment_high_speed.name)

    def test_filter_by_medium_speed_characterization(self):
        """Checks if the API correctly filters for 'medium_speed'."""
        url = reverse('roadsegment-list') + '?last_reading_characterization=medium_speed'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], self.segment_medium_speed.name)

    def test_filter_by_low_speed_characterization(self):
        """Checks if the API correctly filters for 'low_speed'."""
        url = reverse('roadsegment-list') + '?last_reading_characterization=low_speed'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], self.segment_low_speed.name)

    def test_filter_with_invalid_value_returns_empty_queryset(self):
        """Checks that the filter returns an empty list for an invalid value."""
        url = reverse('roadsegment-list') + '?last_reading_characterization=invalid_value'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)

    def test_readings_count_action(self):
        """Checks if the custom 'readings_count' action works."""
        url = reverse('roadsegment-readings-count', args=[self.segment_high_speed.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['readings_count'], 1)

    def test_create_roadsegment_with_write_only_fields(self):
        """Checks if a new road segment can be created using write-only fields."""
        url = reverse('roadsegment-list')
        data = {
            'name': 'New Segment from Test',
            'length': 150.5,
            'long_start_write': 10.0,
            'lat_start_write': 10.0,
            'long_end_write': 11.0,
            'lat_end_write': 11.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(RoadSegment.objects.filter(name='New Segment from Test').exists())
        
    def test_create_roadsegment_with_invalid_length(self):
        """Checks if creating a road segment with invalid length fails."""
        url = reverse('roadsegment-list')
        data = {
            'name': 'Invalid Segment',
            'length': -10.0, # Negative length should fail
            'long_start_write': 10.0,
            'lat_start_write': 10.0,
            'long_end_write': 11.0,
            'lat_end_write': 11.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('length', response.data)

    def test_unauthenticated_user_cannot_create_segment(self):
        """Checks if an unauthenticated user is denied write access."""
        self.client.force_authenticate(user=None)
        url = reverse('roadsegment-list')
        data = {'name': 'New Segment', 'length': 50.0, 'long_start_write': 1, 'lat_start_write': 1, 'long_end_write': 2, 'lat_end_write': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)
        
    def test_unauthenticated_user_can_list_segments(self):
        """Checks if an unauthenticated user can read data."""
        self.client.force_authenticate(user=None)
        url = reverse('roadsegment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class TrafficReadingViewSetTests(APITests):
    """
    Tests for the TrafficReadingViewSet.
    """
    def setUp(self):
        self.client.force_authenticate(user=self.admin_user)
    
    def test_delete_reading(self):
        """Checks if a traffic reading record can be deleted by an admin."""
        reading_to_delete = TrafficReading.objects.first()
        url = reverse('trafficreading-detail', args=[reading_to_delete.id])
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        
        self.assertFalse(TrafficReading.objects.filter(id=reading_to_delete.id).exists())
    
    def test_create_reading(self):
        """Checks if a new traffic reading record can be created by an admin."""
        url = reverse('trafficreading-list')
        data = {
            'speed_measured': 75.5,
            'segment': self.segment_high_speed.id
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        
        self.assertTrue(TrafficReading.objects.filter(speed_measured=75.5).exists())
        
    def test_create_reading_with_negative_speed_fails(self):
        """Checks that creating a reading with negative speed fails validation."""
        url = reverse('trafficreading-list')
        data = {
            'speed_measured': -10.0,
            'segment': self.segment_high_speed.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('speed_measured', response.data)

    def test_regular_user_cannot_delete_reading(self):
        """Checks that a regular user cannot delete a reading."""
        self.client.force_authenticate(user=self.regular_user)
        reading_to_delete = TrafficReading.objects.first()
        url = reverse('trafficreading-detail', args=[reading_to_delete.id])
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(TrafficReading.objects.filter(id=reading_to_delete.id).exists())