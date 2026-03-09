import asyncio
import random
import time

from core.logger import get_logger
from uploader.models import UploadResult

logger = get_logger(__name__)


async def _upload_one(url: str, semaphore: asyncio.Semaphore) -> UploadResult:
    """Ждёт свободный слот семафора, затем загружает одну картинку"""
    async with semaphore:
        logger.info(f"[async] старт + {url}")
        try:
            return await _fake_upload(url)
        except Exception as e:
            logger.error(f"[async] ошибка {url}: {e}")
            return UploadResult(url=url, success=False, duration=0.0, error=str(e))


async def _fake_upload(url: str) -> UploadResult:
    """Имитация загрузки картинки"""
    start = time.perf_counter()
    await asyncio.sleep(random.uniform(0.1, 0.8))
    duration = time.perf_counter() - start
    logger.info(f"[async] готово - {url} ({duration:.3f}s)")
    return UploadResult(url=url, success=True, duration=duration)


def upload_async(images: list[str], limit: int) -> list[UploadResult]:
    """
    Загружает картинки через asyncio + Semaphore

    Semaphore(limit) не даёт запустить больше `limit` корутин одновременно -
    остальные ждут в очереди не блокируя поток
    gather() запускает все задачи сразу, семафор сам регулирует очередь
    """

    async def _run() -> list[UploadResult]:
        semaphore = asyncio.Semaphore(limit)
        tasks = [_upload_one(url, semaphore) for url in images]
        return await asyncio.gather(*tasks)

    return asyncio.run(_run())
