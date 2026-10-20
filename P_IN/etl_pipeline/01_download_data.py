import os
import urllib.request
import ssl
import time

DATA_RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data_raw")
os.makedirs(DATA_RAW_DIR, exist_ok=True)

URLS = {
    "Base-INDICES-Matricula-2005-2026.xlsx": "https://cned.cl/wp-content/uploads/2026/08/Base-INDICES-Matricula-2005-2026.xlsx",
    "01_Esquema_Registro_Base_Pregrado.pdf": "https://cned.cl/wp-content/uploads/2026/08/01_Esquema_Registro_Base_Pregrado.pdf",
    "OfertaPregrado2026.xlsx": "https://cned.cl/wp-content/uploads/2026/01/OfertaPregrado2026.xlsx",
    "01_Esquema_Registro_Oferta2026_INDICES.pdf": "https://cned.cl/wp-content/uploads/2026/01/Esquema_Registro_Oferta2026_INDICES.pdf"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://cned.cl/bases-de-datos",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
}

def download_file(filename, url):
    dest_path = os.path.join(DATA_RAW_DIR, filename)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 10000:
        print(f"[SKIP] {filename} already exists ({os.path.getsize(dest_path):,} bytes).")
        return dest_path

    print(f"[DOWNLOADING] {filename} from {url}...")
    req = urllib.request.Request(url, headers=HEADERS)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    start_time = time.time()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=120) as response, open(dest_path, "wb") as out_file:
            total_bytes = 0
            while True:
                chunk = response.read(1024 * 1024) # 1MB chunks
                if not chunk:
                    break
                out_file.write(chunk)
                total_bytes += len(chunk)
                print(f"  Downloaded: {total_bytes / (1024*1024):.2f} MB...", end="\r")
        elapsed = time.time() - start_time
        print(f"\n[SUCCESS] {filename} downloaded: {total_bytes:,} bytes in {elapsed:.2f}s.")
        return dest_path
    except Exception as e:
        print(f"\n[ERROR] Failed downloading {filename}: {e}")
        if os.path.exists(dest_path):
            os.remove(dest_path)
        return None

if __name__ == "__main__":
    print("=== STARTING DATA DOWNLOAD FROM OFFICIAL CNED REPOSITORY ===")
    for fname, url in URLS.items():
        download_file(fname, url)
    print("=== DOWNLOAD PROCESS COMPLETED ===")
