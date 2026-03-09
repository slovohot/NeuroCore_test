from dataclasses import dataclass


@dataclass
class UploadResult:
    url: str
    success: bool
    duration: float
    error: str | None = None

    def __repr__(self) -> str:
        status = "OK" if self.success else "ERROR"
        return f"[{status}] {self.url} ({self.duration:.3f}s)"
