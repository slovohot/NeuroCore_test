import pytest
from unittest.mock import AsyncMock, patch

from uploader.models import UploadResult
from uploader.uploader import upload_images, UploadMethod
from uploader.async_uploader import upload_async
from uploader.thread_uploader import upload_threaded


# ── async ────────────────────────────────────────────────────────────────────

class TestAsyncUploader:
    def test_returns_all_results(self, sample_urls):
        assert len(upload_async(sample_urls, limit=5)) == len(sample_urls)

    def test_all_successful(self, sample_urls):
        assert all(r.success for r in upload_async(sample_urls, limit=5))

    def test_correct_urls(self, sample_urls):
        assert {r.url for r in upload_async(sample_urls, limit=5)} == set(sample_urls)

    def test_duration_positive(self, sample_urls):
        assert all(r.duration > 0 for r in upload_async(sample_urls, limit=5))

    def test_limit_one(self, sample_urls):
        assert len(upload_async(sample_urls, limit=1)) == len(sample_urls)

    def test_limit_exceeds_images(self, sample_urls):
        assert len(upload_async(sample_urls, limit=100)) == len(sample_urls)

    def test_error_stored_in_result(self, single_url):

        with patch("uploader.async_uploader._fake_upload", new=AsyncMock(side_effect=ConnectionError("network error"))):
            results = upload_async(single_url, limit=1)

        assert not results[0].success
        assert "network error" in results[0].error


# ── thread ───────────────────────────────────────────────────────────────────

class TestThreadUploader:
    def test_returns_all_results(self, sample_urls):
        assert len(upload_threaded(sample_urls, limit=5)) == len(sample_urls)

    def test_all_successful(self, sample_urls):
        assert all(r.success for r in upload_threaded(sample_urls, limit=5))

    def test_correct_urls(self, sample_urls):
        assert {r.url for r in upload_threaded(sample_urls, limit=5)} == set(sample_urls)

    def test_duration_positive(self, sample_urls):
        assert all(r.duration > 0 for r in upload_threaded(sample_urls, limit=5))

    def test_limit_one(self, sample_urls):
        assert len(upload_threaded(sample_urls, limit=1)) == len(sample_urls)

    def test_limit_exceeds_images(self, sample_urls):
        assert len(upload_threaded(sample_urls, limit=100)) == len(sample_urls)

    def test_error_stored_in_result(self, single_url):

        with patch("uploader.thread_uploader._fake_upload", side_effect=ConnectionError("network error")):
            results = upload_threaded(single_url, limit=1)

        assert not results[0].success
        assert results[0].error is not None


# ── upload_images (точка входа) ───────────────────────────────────────────────

class TestUploadImages:
    def test_empty_list(self):
        assert upload_images([], limit=5, method=UploadMethod.ASYNC) == []

    def test_invalid_limit(self, sample_urls):
        with pytest.raises(ValueError, match="limit должен быть >= 1"):
            upload_images(sample_urls, limit=0, method=UploadMethod.ASYNC)

    def test_async_method(self, sample_urls):
        results = upload_images(sample_urls, limit=5, method=UploadMethod.ASYNC)
        assert len(results) == len(sample_urls)

    def test_thread_method(self, sample_urls):
        results = upload_images(sample_urls, limit=5, method=UploadMethod.THREAD)
        assert len(results) == len(sample_urls)

    def test_result_type(self, single_url):
        for method in UploadMethod:
            results = upload_images(single_url, limit=1, method=method)
            assert isinstance(results[0], UploadResult)


