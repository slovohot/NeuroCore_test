# NeuroCore

Тестовое задание — параллельная загрузка картинок с ограничением одновременных загрузок.

Сделал две реализации как и просили, но немного расширил: вынес логику в отдельные модули, добавил нормальный результат загрузки с полями и тесты.

---

## Запуск

```bash
pip install -r requirements.txt

python main.py  # посмотреть как работает
pytest -v       # прогнать тесты
black .         # форматирование кода
```

---

## Как пользоваться

```python
from uploader.uploader import upload_images, UploadMethod

results = upload_images(urls, limit=5, method=UploadMethod.ASYNC)
# или
results = upload_images(urls, limit=5, method=UploadMethod.THREAD)

for r in results:
    print(r)  # [OK] https://... (0.312s)
```

---

## Две реализации

**async** — один поток, корутины переключаются между собой в момент `await`. `Semaphore(limit)` не даёт запустить больше N загрузок одновременно. Подходит когда используешь aiohttp, httpx.

**thread** — пул из N потоков через `ThreadPoolExecutor(max_workers=limit)`. Подходит когда используешь обычные синхронные библиотеки типа requests.