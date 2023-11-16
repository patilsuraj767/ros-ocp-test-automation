import os

DOMAIN = os.getenv("DOMAIN", "test.example.com")
USERNAME = os.getenv("USERNAME", "test_user")
PASSWORD = os.getenv("PASSWORD", "test_password")
DEFAULT_SOURCE_NAME = os.getenv("DEFAULT_SOURCE_NAME", "ros-ocp-dev-test")