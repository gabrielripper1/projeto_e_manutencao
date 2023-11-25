# ChamaInteligente - Geoloc_e_BD - projeto_e_manutencao

Este é um projeto que utiliza Flask para integração com Banco de Dados.

## Configuração do Ambiente


### Instalação da Venv
1. Navegue até o diretório do projeto:
    ```bash
    cd ChamaInteligente/Geoloc_e_BD
    ```

2. Crie um ambiente virtual:
    ```python -m venv venv
    ```

3. Ative o ambiente virtual:
    ```.\venv\Scripts\Activate.ps1
    ```

4. Instalar as dependências necessárias:
    ```pip install -r requirements.txt
    ```

## Executando o Projeto

1. Certificar que a venv está ativada

2. Certificar que está na pasta `ChamaInteligente/Geoloc_e_BD`.

3. Execute o comando iniciar o servidor:
    ```flask run
    ```

4. O aplicativo estará acessível em `http://127.0.0.1:5000/` no seu navegador.


## Observações
1. Para checar se a venv foi ativada, no VSCODE aparece o `(venv)` em verde antes da linha de comando no terminal.
2. Para testar localmente uma mudança no código, além de salvar as alterações,deve-se rodar o comando `flask run` para conseguir testar/ver as alterações no seu navegador.
3. As conexões com o servidor estão no arquivo app.py
