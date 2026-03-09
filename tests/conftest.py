import pytest


@pytest.fixture
def sample_urls() -> list[str]:
    return [f"https://example.com/image_{i}.jpg" for i in range(10)]


@pytest.fixture
def single_url() -> list[str]:
    return ["https://example.com/image_1.jpg"]
