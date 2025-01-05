# server_tcp.py
import socket
import os
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Konfigurasi Server
IP = '192.168.110.183'  # Bind ke semua interface
PORT = 4444
ADDR = (IP, PORT)
SIZE = 4096  # Ukuran buffer 4 KB
FORMAT = "utf-8"

SAVE_DIR = r"C:\Users\ASUS\Documents\received_files\\"
os.makedirs(SAVE_DIR, exist_ok=True)  # Membuat direktori jika belum ada

def main():
    logging.info("[STARTING] Server is starting.")
    """ Memulai socket TCP. """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        """ Bind IP dan PORT ke server. """
        server.bind(ADDR)
        server.listen()
        logging.info(f"[LISTENING] Server is listening on {IP}:{PORT}")

        while True:
            """ Menerima koneksi dari client. """
            conn, addr = server.accept()
            logging.info(f"[NEW CONNECTION] {addr} connected.")

            """ Menerima nama file dari client. """
            filename = conn.recv(SIZE).decode(FORMAT)
            logging.info(f"[RECV] Receiving the filename: {filename}")
            file_path = os.path.join(SAVE_DIR, filename)
            file = open(file_path, "wb")  # Mode tulis binary
            conn.send("Filename received.".encode(FORMAT))

            """ Menerima data file dari client. """
            while True:
                data = conn.recv(SIZE)
                if not data:
                    break
                file.write(data)
                logging.debug(f"[DEBUG] Received {len(data)} bytes.")
            logging.info(f"[RECV] Receiving the file data completed.")
            conn.send("File data received".encode(FORMAT))

            """ Menutup file dan koneksi. """
            file.close()
            conn.close()
            logging.info(f"[DISCONNECTED] {addr} disconnected.")

    
    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        server.close()
        logging.info("[SHUTDOWN] Server is shutting down.")

if __name__ == "__main__":
    main()