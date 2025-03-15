#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 3000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Se o caminho for '/', redireciona para '/WebUiCase.html'
        if self.path == '/':
            self.path = '/WebUiCase.html'

        # Verifica se o caminho termina com '.html'
        if self.path.endswith('.html'):
            file_path = os.path.join(os.getcwd(), self.path.lstrip('/'))
            
            try:
                # Tenta abrir e ler o arquivo HTML
                with open(file_path, 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                # Se o arquivo não existir, retorna mensagem de erro
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write("⚠️ Pagina não existe!!".encode('utf-8'))
        else:
            # Para outros tipos de requisição, usa o comportamento padrão
            super().do_GET()

def run_server():
    # Configura o servidor
    server_address = ('', PORT)
    httpd = socketserver.TCPServer(server_address, CustomHTTPRequestHandler)
    
    print(f"Servidor rodando em http://localhost:{PORT}")
    # Inicia o servidor em loop infinito
    httpd.serve_forever()

if __name__ == '__main__':
    # Aqui você pode adicionar um comando para abrir o navegador, se desejar
    # Por exemplo, usando o módulo 'webbrowser':
    import webbrowser
    webbrowser.open(f'http://localhost:{PORT}')
    
    run_server()