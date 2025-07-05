import requests
import socket
import struct
import threading
import time

LOCAL_PORT = 12345

def handle_connection(conn):
    while True:
        data = conn.recv(4096)
        if not data:
            break
        request_header = data.decode('utf-8')
        if 'ads' in request_header:
            response = b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n"
            conn.sendall(response)
        else:
            original_request = data
            original_destination = (request_header.split(' ')[1], 80)
            with socket.create_connection(original_destination) as original_conn:
                original_conn.sendall(original_request)
                response = original_conn.recv(4096)
                conn.sendall(response)
    conn.close()

def start_proxy():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', LOCAL_PORT))
        s.listen(5)
        print(f"Proxy server listening on port {LOCAL_PORT}")
        while True:
            conn, addr = s.accept()
            print(f"Accepted connection from {addr}")
            threading.Thread(target=handle_connection, args=(conn,)).start()

def redirect_spotify_traffic():
    while True:
        try:
            with open('C:\Windows\System32\drivers\etc\hosts', 'r') as file:
                lines = file.readlines()
            with open('C:\Windows\System32\drivers\etc\hosts', 'w') as file:
                for line in lines:
                    if 'spotify.com' in line:
                        file.write(f"127.0.0.1 spotify.com\n")
                    else:
                        file.write(line)
            print("Hosts file updated to redirect Spotify traffic.")
        except Exception as e:
            print(f"Error updating hosts file: {e}")
        time.sleep(60)

proxy_thread = threading.Thread(target=start_proxy)
proxy_thread.start()

redirect_thread = threading.Thread(target=redirect_spotify_traffic)
redirect_thread.start()