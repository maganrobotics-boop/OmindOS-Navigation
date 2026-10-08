"""Fetch only the public preview installer, then verify the trusted artifact hash."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import hashlib
import subprocess
import tempfile
import os

NAME = "omindos-control-preview-0.2.0-preview.5-linux-amd64.tar"
SIZE = 820449280
SHA256 = "276b666a8fee186ba839c30bda8676baba4125a7c9e51408f07ed596cc9db5cc"
URL = "https://43.138.161.143/downloads/navigation/v0.2.0-preview.5/" + NAME
CHUNK = 1024 * 1024
root = Path("assets/v0.2.0-preview.5")
with tempfile.TemporaryDirectory(prefix="preview5-transfer-") as directory:
    temporary = Path(directory)
    ranges = [(i, start, min(SIZE - 1, start + CHUNK - 1))
              for i, start in enumerate(range(0, SIZE, CHUNK))]
    def fetch(item):
        index, start, end = item
        path = temporary / str(index)
        # The public artifact carries no credentials. The pinned hash verifies
        # content authenticity before upload; direct IP avoids SNI resets.
        subprocess.run(["curl", "--silent", "--show-error", "--insecure",
                        "--fail", "--http1.1", "--retry", "2", "--retry-all-errors",
                        "--connect-timeout", "15", "--max-time", "120",
                        "--header", "Host: omindos.cn", "--range", f"{start}-{end}",
                        "--output", str(path), URL], check=True)
        if path.stat().st_size != end - start + 1:
            raise RuntimeError(f"Invalid range length for chunk {index}")
        return index
    with ThreadPoolExecutor(max_workers=12) as pool:
        futures = [pool.submit(fetch, item) for item in ranges]
        for count, future in enumerate(as_completed(futures), 1):
            future.result()
            if count % 10 == 0 or count == len(ranges):
                print(f"Downloaded {count}/{len(ranges)} chunks", flush=True)
    output = root / (NAME + ".part")
    digest = hashlib.sha256()
    with output.open("wb") as stream:
        for index, _, _ in ranges:
            with (temporary / str(index)).open("rb") as source:
                while block := source.read(1024 * 1024):
                    digest.update(block)
                    stream.write(block)
    if output.stat().st_size != SIZE or digest.hexdigest() != SHA256:
        output.unlink()
        raise RuntimeError("Complete installer size or SHA-256 mismatch")
    os.replace(output, root / NAME)
    print("Complete installer SHA-256 verified", flush=True)
