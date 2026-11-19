import sys
import time

VERSION = "v2.0.0 - Broken Release"


def run_service():
    print(f"[APP] Menjalankan checkout-service ({VERSION})...", flush=True)
    time.sleep(1)

    # Simulasi bug fatal saat runtime
    diskon = 0
    harga_akhir = 150000 / diskon  # Memicu ZeroDivisionError
    print(f"[APP] Harga akhir: {harga_akhir}", flush=True)


if __name__ == "__main__":
    try:
        run_service()
        sys.exit(0)
    except Exception as e:
        print(f"[APP CRASH] Terjadi kesalahan fatal: {e}", file=sys.stderr, flush=True)
        sys.exit(1)
