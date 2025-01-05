# client_tcp.py
import socket
import os
import logging
import time
from tqdm import tqdm  # type: ignore # Untuk progress bar

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Konfigurasi Client
IP = '192.168.110.184'  # Ganti dengan alamat IP server
PORT = 2302
ADDR = (IP, PORT)
SIZE = 4096  # Ukuran buffer 4 KB
FORMAT = "utf-8"

def main():
    filename = 'file_5120KB.bin'  # Ganti dengan nama file yang ingin dikirim
    if not os.path.exists(filename):
        logging.error(f"File {filename} tidak ditemukan.")
        return

    logging.info("[STARTING] Client is starting.")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        """ Mulai pengukuran waktu """
        start_time = time.perf_counter()

        client.connect(ADDR)
        logging.info(f"[CONNECTED] Terhubung ke server {IP}:{PORT}")

        """ Mengirim nama file ke server """
        client.send(filename.encode(FORMAT))
        response = client.recv(SIZE).decode(FORMAT)
        logging.info(f"[SERVER] {response}")

        """ Mengirim data file ke server dengan progress bar """
        filesize = os.path.getsize(filename)
        progress = tqdm(total=filesize, unit='B', unit_scale=True, desc='Sending', ncols=80)

        with open(filename, "rb") as file:
            while True:
                bytes_read = file.read(SIZE)
                if not bytes_read:
                    break
                client.sendall(bytes_read)
                progress.update(len(bytes_read))
        progress.close()
        logging.info("[SENT] File data telah dikirim.")

        """ Selesai pengukuran waktu setelah mengirim seluruh data dan menerima konfirmasi """
        end_time = time.perf_counter()
        time_taken = end_time - start_time
        logging.info(f"[TIME TAKEN] Sent '{filename}' in {time_taken:.4f} seconds.")

        """ Menerima konfirmasi dari server """
        response = client.recv(SIZE).decode(FORMAT)
        logging.info(f"[SERVER] {response}")

    except ConnectionRefusedError:
        logging.error(f"Connection refused. Pastikan server berjalan dan mendengarkan di {IP}:{PORT}.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        client.close()
        logging.info("[DISCONNECTED] Client telah terputus dari server.")

if __name__ == "__main__":
    main()