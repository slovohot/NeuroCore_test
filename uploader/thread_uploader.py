import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.logger import get_logger
from uploader.models import UploadResult

logger = get_logger(__name__)


def _fake_upload(url: str) -> UploadResult:
    """Имитация загрузки картинки"""
    start = time.perf_counter()
    time.sleep(random.uniform(0.1, 0.8))
    return UploadResult(url=url, success=True, duration=time.perf_counter() - start)


def upload_threaded(images: list[str], limit: int) -> list[UploadResult]:
    """
    Загружает картинки через ThreadPoolExecutor

    max_workers=limit ограничивает кол-во параллельных потоков
    submit() отправляет все задачи сразу не дожидаясь результата
    as_completed() отдаёт результаты по мере готовности
    """
    results: list[UploadResult] = []

    def _upload_with_log(url: str) -> UploadResult:
        logger.info(f"[thread] старт + {url} ({threading.current_thread().name})")
        result = _fake_upload(url)
        logger.info(f"[thread] готово - {result}")
        return result

    with ThreadPoolExecutor(max_workers=limit) as executor:
        futures = {executor.submit(_upload_with_log, url): url for url in images}
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                url = futures[future]
                logger.error(f"[thread] ошибка {url}: {e}")
                results.append(
                    UploadResult(url=url, success=False, duration=0.0, error=str(e))
                )

    return results
