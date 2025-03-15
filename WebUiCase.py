#!/usr/bin/env python3
import http.server
import socketserver
import os
import subprocess
import signal

PORT = 30010
BRAVE_COMMAND = [
    'brave-browser',
    '--profile-directory=Default',
    '--app-id=[ id gerado pelo navegador do web app]',
    f'http://localhost:{PORT}/WebUiCase.html'
]

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
        elif self.path == '/sair':
            # Se a requisição for '/sair', finaliza o navegador
            # self.send_response(200)
            # self.send_header('Content-Type', 'text/html; charset=utf-8')
            # self.end_headers()
            # self.wfile.write("Saindo...".encode('utf-8'))
            # Finaliza o navegador
            subprocess.run(['pkill', '-f', 'WebUiCase'])

            # Finaliza o servidor
            self.server.shutdown()

            # Encerra o script
            sys.exit(0)
        else:
            # Para outros tipos de requisição, usa o comportamento padrão
            super().do_GET()

def run_server():
    # Configura o servidor
    server_address = ('', PORT)
    httpd = socketserver.TCPServer(server_address, CustomHTTPRequestHandler)

    print(f"Servidor rodando em http://localhost:{PORT}")

    # Abre o navegador Brave com o perfil e aplicativo especificados
    subprocess.Popen(BRAVE_COMMAND)

    # Inicia o servidor em loop infinito
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()