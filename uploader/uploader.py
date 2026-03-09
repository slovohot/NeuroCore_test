from enum import Enum

from uploader.models import UploadResult
from uploader.async_uploader import upload_async
from uploader.thread_uploader import upload_threaded


class UploadMethod(Enum):
    ASYNC = "async"
    THREAD = "thread"


def upload_images(
    urls: list[str], limit: int, method: UploadMethod
) -> list[UploadResult]:
    """
    Загружает список картинок с ограничением одновременных загрузок

    :param urls:   список URL картинок
    :param limit:  максимум одновременных загрузок
    :param method: UploadMethod.ASYNC или UploadMethod.THREAD
    """
    if not urls:
        return []
    if limit < 1:  # не имеет смысла, лучше сразу выбросить исключение
        raise ValueError(f"limit должен быть >= 1, получено: {limit}")

    if method == UploadMethod.ASYNC:
        return upload_async(urls, limit)
    return upload_threaded(urls, limit)
