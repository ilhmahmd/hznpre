import os
import subprocess
import sys

def install_dependencies():
    try:
        # Set environment variables for cmake and ninja
        os.environ['PATH'] = r'C:\Program Files\CMake\bin;' + os.environ['PATH']
        os.environ['PATH'] = r'C:\Users\anain\Downloads\ninja-win;' + os.environ['PATH']

        # Baca file requirements.txt
        with open('requirements.txt', 'r') as file:
            requirements = file.read().splitlines()

        # Filter baris komentar dan baris kosong
        requirements = [req for req in requirements if req and not req.startswith('#')]

        # Instal setiap requirement menggunakan pip
        for requirement in requirements:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', requirement])
        print("Semua dependensi berhasil diinstal.")

    except subprocess.CalledProcessError as e:
        print(f"Terjadi kesalahan saat menginstal dependensi: {e}")

# Panggil fungsi untuk menginstal dependensi
install_dependencies()
