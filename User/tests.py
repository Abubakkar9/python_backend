"""
This module contains test cases for your Django API views and endpoints.
"""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User

@pytest.fixture
def api_client():
    """
    Fixture to provide an instance of APIClient for testing.
    """
    return APIClient()

@pytest.fixture
def create_user():
    """
    Fixture to create a User instance for testing.
    """
    def _create_user(**kwargs):
        return User.objects.create(**kwargs)
    return _create_user

@pytest.fixture
def user_data():
    """
    Fixture to provide sample user data for testing.
    """
    return {
        "first_name": "Abubakkar",
        "last_name": "Arshad",
        "email": "abubakkar.arshad@example.com",
    }

@pytest.mark.django_db
def test_get_all_users(api_client, create_user):
    """
    Test retrieving all users using the API endpoint.
    """
    create_user(first_name="Abubakkar", last_name="Arshad", email="abubakkar.arshad@example.com")
    create_user(first_name="Faisal", last_name="Rajpoot", email="faisal.rajpoot@example.com")

    url = reverse("users")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

def test_get_user_not_found(api_client):
    """
    Test retrieving a user that does not exist.
    """
    url = reverse("users_update_delete", args=[999])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_get_user(api_client, create_user):
    """
    Test retrieving a user using the API endpoint.
    """
    user = create_user(first_name="Abubakkar", last_name="Arshad", email="abubakkar.arshad@example.com")
    url = reverse("users_update_delete", args=[user.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == "Abubakkar"

def test_create_user_invalid_data(api_client):
    """
    Test creating a user with invalid data.
    """
    url = reverse("users")
    response = api_client.post(url, {"first_name": "John"}, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_create_user(api_client, user_data):
    """
    Test creating a user using the API endpoint.
    """
    url = reverse("users")
    response = api_client.post(url, user_data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert User.objects.first().first_name == "Abubakkar"

# ... More test cases ...

@pytest.mark.django_db
def test_update_user_not_found(api_client, user_data):
    """
    Test updating a user that does not exist.
    """
    url = reverse("users_update_delete", args=[999])
    response = api_client.put(url, user_data, format="json")

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_update_user(api_client, create_user, user_data):
    """
    Test updating a user using the API endpoint.
    """
    user = create_user(first_name="Arshad",
                       last_name="Abubakkar",
                       email="arshad.abubakkar@example.com")

    url = reverse("users_update_delete", args=[user.id])
    response = api_client.put(url, user_data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert User.objects.get(id=user.id).first_name == "Abubakkar"

@pytest.mark.django_db
def test_delete_user(api_client, create_user):
    """
    Test deleting a user using the API endpoint.
    """
    user = create_user(first_name="Abubakkar",
                       last_name="Arshad",
                       email="abubakkar.arshad@example.com")

    url = reverse("users_update_delete", args=[user.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_200_OK
    assert User.objects.count() == 0

def test_delete_user_not_found(api_client):
    """
    Test deleting a user that does not exist.
    """
    url = reverse("users_update_delete", args=[999])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
