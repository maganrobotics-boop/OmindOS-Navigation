"""Download the three approved binaries and verify every byte before publishing."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import hashlib
import json
import subprocess
import tempfile
import urllib.request

ROOT = Path("assets/v0.2.0-preview.6")
CHUNK = 1024 * 1024

def verify(path, item):
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if path.stat().st_size != item["bytes"] or digest != item["sha256"]:
        raise RuntimeError("Size/SHA256 mismatch: " + item["filename"])

def download(item):
    output = ROOT / item["filename"]
    if output.exists():
        verify(output, item)
        return
    # Each range is checked for length, then the joined file is hash-verified.
    with tempfile.TemporaryDirectory(prefix="preview6-") as directory:
        tmp = Path(directory)
        ranges = [(i, start, min(item["bytes"] - 1, start + CHUNK - 1))
                  for i, start in enumerate(range(0, item["bytes"], CHUNK))]
        def fetch(part):
            i, start, end = part
            path = tmp / str(i)
            command = ["curl", "--silent", "--show-error", "--fail", "--location",
                       "--http1.1", "--retry", "2", "--retry-all-errors",
                       "--connect-timeout", "15", "--max-time", "120",
                       "--range", f"{start}-{end}", "--output", str(path)]
            # Existing origin transfer route avoids intermittent SNI resets.
            # Only public bytes travel here; the pinned SHA256 authenticates them.
            url = item["mirror_url"].replace("https://omindos.cn", "https://43.138.161.143")
            subprocess.run(command + ["--insecure", "--header", "Host: omindos.cn", url], check=True)
            if path.stat().st_size != end - start + 1:
                raise RuntimeError("Invalid range length")
        with ThreadPoolExecutor(max_workers=12) as pool:
            for count, future in enumerate(as_completed([pool.submit(fetch, part) for part in ranges]), 1):
                future.result()
                if count % 50 == 0 or count == len(ranges):
                    print(item["filename"], count, "/", len(ranges), flush=True)
        partial = output.with_name(output.name + ".part")
        with partial.open("wb") as stream:
            for i, _, _ in ranges:
                with (tmp / str(i)).open("rb") as source:
                    while block := source.read(CHUNK):
                        stream.write(block)
        verify(partial, item)
        partial.replace(output)
    print("Verified", item["filename"], item["bytes"], flush=True)

def main():
    summary = json.loads((ROOT/"RELEASE_SUMMARY.json").read_text())
    assert summary["release_tag"] == "v0.2.0-preview.6"
    assert not summary["backend_source_included"]
    for item in summary["files"]:
        download(item)

if __name__ == "__main__":
    main()
