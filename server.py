import socket
import os

# Percorsi assoluti per evitare problemi se il file viene spostato
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WWW_DIR = os.path.join(BASE_DIR, 'www')

def handle_request(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8', errors='ignore')
        if not request:
            client_socket.close()
            return

        request_line = request.splitlines()[0]
        print(f"[DEBUG] Richiesta: {request_line}")

        try:
            method, path, _ = request_line.split()
        except ValueError:
            client_socket.close()
            return

        if method != 'GET':
            response = "HTTP/1.1 405 Method Not Allowed\r\n\r\nSolo il metodo GET è supportato.".encode('utf-8')
        else:
            if path == '/':
                path = 'index.html'
            else:
                path = path.lstrip('/')  # Rimuove lo slash iniziale

            file_path = os.path.join(WWW_DIR, path)

            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    content = f.read()
                header = "HTTP/1.1 200 OK\r\n\r\n".encode('utf-8')
                response = header + content
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\nFile non trovato.".encode('utf-8')

        client_socket.sendall(response)

    except Exception as e:
        print("[ERRORE]", e)
    finally:
        client_socket.close()

def start_server():
    host = 'localhost'
    port = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server in ascolto su http://{host}:{port}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"[CONNESSIONE] Da {addr}")
            handle_request(client_socket)

if __name__ == '__main__':
    start_server()
