# app.py - Versi 1.0 (Stabil)
import sys
import time

VERSION = "v1.0.0 - Stable"


def run_service():
    print(f"[APP] Menjalankan checkout-service ({VERSION})...")
    time.sleep(1)
    # Simulasi proses bisnis berhasil
    total_transaksi = 150000
    print(f"[APP] Transaksi berhasil diproses: Rp{total_transaksi}")
    print("[APP] Health check: OK")


if __name__ == "__main__":
    try:
        run_service()
        sys.exit(0)  # Exit code 0 = PASS[cite: 8]
    except Exception as e:
        print(f"[APP ERROR] {e}", file=sys.stderr)
        sys.exit(1)  # Exit code 1 = FAIL[cite: 8]
