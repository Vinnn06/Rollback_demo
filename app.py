# deploy_pipeline.py
import subprocess
import sys


def run_cmd(command):
    return subprocess.run(command, shell=True, text=True, capture_output=True)


def get_current_commit():
    res = run_cmd("git rev-parse --short HEAD")
    return res.stdout.strip()


def deploy():
    print("=== MEMULAI PIPELINE CD & POST-DEPLOY VALIDATION ===")

    # 1. Simpan titik aman (Last Known Good Commit) sebelum pull
    previous_commit = get_current_commit()
    print(f"[CD] Commit stabil saat ini : {previous_commit}")

    # 2. Pull perubahan terbaru dari GitHub
    print("[CD] Menarik pembaruan dari GitHub (git pull)...")
    pull_res = run_cmd("git pull origin main")
    if pull_res.returncode != 0:
        print(f"[CD ERROR] Gagal git pull:\n{pull_res.stderr}")
        sys.exit(1)

    new_commit = get_current_commit()
    print(f"[CD] Commit aktif setelah pull: {new_commit}")

    # 3. Jalankan aplikasi (Post-Deploy Validation)
    print("[CD] Menjalankan aplikasi baru (python3 app.py)...")
    app_res = subprocess.run([sys.executable, "app.py"], text=True, capture_output=True)
    print(app_res.stdout.strip())

    # 4. Evaluasi Exit Code POSIX[cite: 8]
    if app_res.returncode == 0:
        print(f"[CD PASS] Deployment commit {new_commit} sukses (Exit Code: 0).\n")
    else:
        print(
            f"[CD ALERT] Deployment commit {new_commit} GAGAL (Exit Code: {app_res.returncode})!"
        )
        print(f"[CD STDERR] {app_res.stderr.strip()}")

        # 5. Eksekusi Rollback otomatis ke commit sebelumnya[cite: 5]
        if previous_commit != new_commit:
            print(
                f"[ROLLBACK] Mengembalikan kode ke commit stabil {previous_commit}..."
            )
            run_cmd(f"git reset --hard {previous_commit}")

            print("[ROLLBACK] Memverifikasi ulang layanan pasca-rollback...")
            verify_res = subprocess.run(
                [sys.executable, "app.py"], text=True, capture_output=True
            )
            print(verify_res.stdout.strip())
            print(
                f"[ROLLBACK SELESAI] Layanan pulih pada commit {previous_commit} (Exit Code: {verify_res.returncode}).\n"
            )
        else:
            print("[ROLLBACK] Tidak ada commit sebelumnya untuk di-rollback.\n")


if __name__ == "__main__":
    deploy()
