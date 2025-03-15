#!/bin/bash
# echo $0
PORT=3000

#echo -e "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"

WebUiCase() {

    REQUEST_HEADER=""
    while IFS= read -r line; do
        # Adiciona cada linha ao conteúdo do cabeçalho
        REQUEST_HEADER+="$line"$'\n'
        # Verifica se a linha está vazia (fim do cabeçalho HTTP)
        if [[ "$line" == $'\r' || -z "$line" ]]; then
            break
        fi
    done
    # echo $REQUEST_HEADER

    CONTENT_LENGTH=$(echo "$REQUEST_HEADER" | grep -i 'Content-Length:' | awk '{print $2}')
    CONTENT_LENGTH=${CONTENT_LENGTH//$'\r'/} # Remove o \r (retorno de carro)
    #     CONTENT_HOST=$(echo "$REQUEST_HEADER" | grep -i 'Host:' | awk '{print $2}')
    CONTENT_HOST=$(echo "$REQUEST_HEADER" | grep -i 'Origin:' | awk '{print $2}')

    #     echo $REQUEST_HEADER >file.txt
    CONTENT_HOST=${CONTENT_HOST//$'\r'/} # Remove o \r (retorno de carro)
    REQUISICAO=$(echo "$REQUEST_HEADER" | grep -i 'GET' | awk '{print $2}')

    #     echo -e "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
    [[ "$REQUISICAO" == '/' ]] && REQUISICAO='/WebUiCase.html'
    [[ "$REQUISICAO" == '/sair' ]] && pkill -f "WebUiCase"

    #     echo $REQUISICAO

    [[ "$REQUISICAO" =~ \.html ]] &&
        {
            echo -e "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
            [[ -f "$PWD$REQUISICAO" ]] && cat "$PWD$REQUISICAO" || echo "⚠️ Pagina não existe!! "
        } && exit

}

[[ -n "$1" ]] && $1 && exit
brave-browser --profile-directory=Default --app-id=hbblfifohofgngfbjbiimbbcimepbdcb
pgrep -f "ncat -l -p $PORT" >/dev/null 2>&1 && exit

while true; do
    ncat -l -p $PORT -e "$0 WebUiCase"
done
