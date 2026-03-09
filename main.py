import random
import time

from uploader.uploader import upload_images, UploadMethod

QUANTITY_IMG = 10  # количество картинок (X из тз)
LIMIT = 5  # количество загружаемых картинок за раз (N из тз)

IMAGE_URLS = [f"https://example.com/photo_{i}.jpg"
              for i in random.sample(range(1, 1000), QUANTITY_IMG)]


if __name__ == "__main__":
    for method in UploadMethod:
        print(f"\n{'=' * 30}\n  Метод: {method.value}\n{'=' * 30}")
        t0 = time.perf_counter()
        results = upload_images(IMAGE_URLS, limit=LIMIT, method=method)
        elapsed = time.perf_counter() - t0
        for r in results:
            print(r)
        print(f"\nВремя: {elapsed:.2f}s | {sum(r.success for r in results)}/{len(results)} успешно")


