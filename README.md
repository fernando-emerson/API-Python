# API-Python

Desenvolvida em Python utilizando o Micro-Framework FLASK e hospedada em instância EC2 da AWS. Este documento tem por objetivo demonstrar as funcionalidades e modo de utilização dos recursos disponíveis da REST API.

Para se conectar à API, o usuário deve realizar um primeiro cadastro e confirmá-lo por e-mail. Após o login, uma chave token de autenticação é gerada automaticamente e através dela será possível utilizar os recursos da API. A chave token não é fixa, a cada nova sessão do usuário uma nova chave é criada. Referente ao armazenamento das informações da API, são mantidas em arquivo de banco de dados SQLite. 

Para consultar os dados que o teste prático solicita, é necessário realizar o cadastro na API, confirmar a conta acessando o link que será enviado para o email cadastrado, fazer o login e utilizar o token que será gerado para acessar através da URL /Fernando – (mais detalhes na sessão “consulta de dados”)

### Bibliotecas utilizadas:

- [aniso8601](https://pypi.org/project/aniso8601/)
- [Click](https://pypi.org/project/click/)
- [Flask](https://pypi.org/project/Flask/)
- [Flask-JWT-Extended](https://pypi.org/project/Flask-JWT-Extended/)
- [Flask-RESTful](https://pypi.org/project/Flask-RESTful/)
- [Flask-SQLAlchemy](https://pypi.org/project/Flask-SQLAlchemy/)
- [itsdangerous](https://pypi.org/project/itsdangerous/)
- [Jinja2](https://pypi.org/project/Jinja2/)
- [MarkupSafe](https://pypi.org/project/MarkupSafe/)
- [PyJWT](https://pypi.org/project/PyJWT/)
- [pytz](https://pypi.org/project/pytz/)
- [six](https://pypi.org/project/six/)
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)
- [Werkzeug](https://pypi.org/project/Werkzeug/)
- [yagmail](https://pypi.org/project/yagmail/)



## Como rodar a API localmente

#### Pré-requisitos

- Python 3.9 ou superior
- Pacote de bibliotecas (Você pode usar o ambiente virtual "venv" que já se encontra no repositório, ou baixar as bibliotecas listadas acima diretamente na sua máquina)

#### Instalação

1. Clone o repositório para sua máquina

   ```
   git clone https://github.com/fernando-emerson/API-Python
   ```

2. Instale as bibliotecas listadas acima, nas suas últimas versões

   ```
   ex: pip install Flask 
   ```

3. Caso seja necessário, o arquivo "requeriments.txt" contém todas as bibliotecas utilizadas juntamente com as versões, para instalar do arquivo utilize o comando

   ```
   pip install -r requirements.txt
   ```

4. Em qualquer IDE/editor de código rode o arquivo "app_local.py", ele é o arquivo que fará a conexão do Flask com a porta 5000 da sua máquina, disponibilizando a API para testes

#### Uso

Feito as instalações das bibliotecas, ao rodar o arquivo app_local.py no seu editor será exibido o seguinte resultado:

 * ```
   Serving Flask app 'app' (lazy loading)
   
   Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
   
    * Debug mode: on
    * Restarting with stat
    * Debugger is active!
    * Debugger PIN: 413-112-023
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   ```

   

#### Fim

No final do README.me você vai encontrar a documentação sobre a utilização dos recursos da API, e as rotas disponíveis para se utilizar a URL local gerada pelo Flask. 

## Rodando a API em servidor AWS

**Pré-requisitos**:

A API está hospedada em instância EC2 do tipo t2.micro da AWS, virtualizando o sistema operacional Linux. Dessa forma, para se fazer esse procedimento no Windows, é recomendável que se baixe o Putty para se conectar via ssh à instância ou crie uma máquina virtual Linux e execute o passo a passo a seguir.

​		**Criando a instância na AWS**

1. Logue no site da AWS, e acesse o menu services na opção "instância EC2"

2. Crie a instância utilizando a AMI (Machine Image) Ubuntu Server 18.04 LTS

3. Foi utilizado o Free tier t2.micro que é fornecido pela AWS gratuitamente

4. Na janela "Select an existing key pair or create a new key pair" selecione Create e defina um nome para a chave de acesso, por exemplo "flaskapp" e faça o donwload do arquivo

5. Lance a instância

   **Configurando linux e conexão via ssh com a instância**

6. Crie uma pasta chamada "aws" e mova a chave para lá

7. Agora, é necessário dar autorização para executar essa chave

8. Abra o terminal do Linux na pasta aws e digite os seguintes comandos

   ```
   chmod 400 "flaskapp.pem"
   ```

   ```
   ssh -i "flaskapp.pem" ubuntu@{ip_da_instancia}
   ```

9. Pronto, agora já está conectado diretamente à instância escolhida

10. Utilize o comando "sudo su" para dar autorizações de super usuário

    ```
    sudo su
    ```

11. Faça um git clone do repositório da API para dentro da pasta "aws" que foi criada

12. Exclua a pasta do ambiente virtual "venv", será criado um novo dentro da instância

13. Exclua o arquivo "app_local.py" pois para fazer o deploy será utilizado o "app.py"

14. Renomeie a pasta do repositório para "app" para facilitar

    **Movendo os arquivos da API para a instância**

15. Abra um terminal local na pasta aws e utilize os seguintes comandos para mover os arquivos

    ```
    scp -i "flaskapp.pem" -r app ubuntu@{ip_da_sua_instancia}:~/
    ```

    "app" é o nome da pasta que será criada dentro da instância

16. Pronto, os arquivos devem ter sido movidos.

    **Configurando instância**

17. No terminal da instância, digite sudo apt para atualizar todas as dependências

    ```
    sudo apt
    ```

18. Instalar o gerenciador de libs do python

    ```
    sudo apt install python3-pip
    ```

19. Instalar a versão 3.9 do python

    ```
    sudo apt install python3.9
    ```

20. Instalar virtualenv

    ```
    sudo pip3 virtualenv
    ```

21. Instalar o ambiente virtual

    ```
    virtualenv venv --python=python3.9
    ```

22. Agora, basta acessar o ambiente virtual que foi criado

    ```
    source ambvir/bin/activate
    ```

23. Feito isso, é necessário instalar todas as bibliotecas listadas abaixo utilizando o comando "pip install {nome_da_biblioteca}"

    * flask

    * flask-restful

    * flask-jwt-extended

    * flask-sqlalchemy

    * requests

    * gunicorn

    * yagmail

    **Configurando security group da aws**

    Para liberar as portas de conexão do Flask, acesse o menu security group no site da AWS

    Clique em editar e adicione as seguintes novas regras: HTTP, HTTPS e por fim Custom TCP definindo a Port Range em 5000

    **Configurando gunicorn e nginx**

    Como funciona? Recebida uma requisição, ela entra em contato com o nginx, que funciona como um proxy enviando as informações para o gunicorn, em seguida enviando para a aplicação flask.

24. Instalar nginx

    ```
    apt install nginx
    ```

25. É preciso remover a configuração padrão do nginx para criar uma nova

    ```
    sudo rm /etc/nginx/sites-enabled/default
    ```

26. Criando nova configuração

    ```
    sudo touch /etc/nginx/sites-available/flask_settings
    flask_settings é o nome escolhido para o arquivo de configuração
    ```

27. Associando configuração padrão do nginx ao arquivo flask_settings que foi criado

    ```
    sudo ln -s /etc/nginx/sites-available/flask_settings /etc/nginx/sites-enabled/flask_settings
    ```

28. Editar arquivo flask_settings para adicionar as regras de configuração

    ```
    sudo nano /etc/nginx/sites-enabled/flask_settings
    ```

29. Agora, estamos dentro do arquivo flask_settings, digite as seguintes informações para configurar o proxy (comunicação entre nginx e gunicorn)

    ```
    server {
    
    	location / {
    
    		proxy_pass http://127.0.0.1:8000;
    
    		proxy_set_header Host $host;
    
    		proxy_set_header X-Real-IP $remote_addr;
    
    	}
    
    }
    ```

    

30. Aperte CTRL+A para salvar, depois CTRL+X para sair e voltar ao terminal

    **Reiniciar nginx com as novas configurações**

    ```
    sudo /etc/init.d/nginx restart
    ```

    **Ativando e configuração "supervisor" para automatizar a execução do script, mantendo sempre o servidor flask rodando**

31. Instalando supervisor

    ```
    sudo apt install supervisor
    ```

32. Configurando supervisor

    ```
    nano /etc/supervisor/conf.d/flaskapp.conf
    "flaskapp.conf" é o nome do arquivo escolhido para receber as configurações do supervisor
    ```

33. Depois  do comando acima, será acessado o arquivo flaskapp.conf. Digite as seguintes informações:

    ```
    [program:app]
    directory=/home/ubuntu/app
    command=/home/ubuntu/app/venv/bin/gunicorn -w 3 app:app
    user=root
    autostart=true
    autorestart=true
    stopasgroup=true
    killasgroup=true
    stderr_logfile=/var/log/app.err.log
    stdout_logfile=/var/log/app.out.log
    ```

34. Aperte Ctrl+O e enter para salvar

35. Criando diretório dos arquivos de log

    ```
    mkdir -p /var/log/app
    ```

36. Criando arquivos de log

    ```
    touch /var/log/app/app.err.log
    touch /var/log/app/app.out.log
    ```

37. Por fim, basta reiniciar o supervisor 

    ```
    supervisorctl reload
    ```

38. Pronto! API configurada e hospedada na nuvem.



## Documentação

URL:  ec2-18-218-189-237.us-east-2.compute.amazonaws.com/

### Cadastro de usuário 

Exemplo de Requisição para cadastrar um novo usuário.

| Metodo | URL       |
| ------ | --------- |
| POST   | /register |

Header

| Content-Type | Application/json |
| ------------ | ---------------- |

```
Request Body
{
    "login": "usuario",
    "password": "senha",
    "email": "email"
}
```

**Resposta**

Feita a requisição com o método POST, será retornada uma mensagem informando que o usuário foi criado, seguido pelo status code correspondente (201).

| Status | 201 Created |
| ------ | ----------- |

```
Response Body
{
    "message": "Usuário criado com sucesso!"
}
```

**Exceções**

1. A senha deve conter no mínimo 8 dígitos, caso contrário a seguinte mensagem será exibida

| Status | 400 Bad Request |
| ------ | --------------- |

```
Response Body

{
           "message": "Senha muito fraca, por favor digite uma senha com pelo menos 8 							caracteres."

}
```




2.	Caso o login que o cliente digitou já exista no banco de dados

| Status | 400 Bad Request |
| ------ | --------------- |

```
Response Body
{
      "message": "Este login já existe, por favor escolha um diferente.”
}
```




3.	Caso o e-mail que o cliente digitou já exista no banco de dados	      

| Status | 400 Bad Request |
| ------ | --------------- |

```
Response Body
{
        "message": "O E-mail digitado já existe"
}
```



4.	Caso não tenha sido preenchido o campo e-mail

| Status | 400 Bad Request |
| ------ | --------------- |

```
 Response Body
 {
              "message": "O campo 'e-mail' precisa ser preenchido"
 }

```



5.	O E-mail é verificado através de Expressões regulares, e se inválido retornará a seguinte mensagem

| Status | 400 Bad Request |
| ------ | --------------- |

```
Response Body
{
           "message": "O e-mail é inválido, digite um e-mail válido e tente novamente.
}
```

## Login

Exemplo de Requisição para logar com um usuário.

| METODO | URL    |
| ------ | ------ |
| POST   | /login |

| Header       |                  |
| ------------ | ---------------- |
| Content-Type | Application/json |

```
Request Body
{
    "login": "joao",
    "password": "123456789",
    "email": "joao@gmail.com"
}
```

**Resposta** 

Retornará uma mensagem contendo o token de acesso que será necessário para fazer as requisições.
O Token expira a cada nova sessão do usuário.

| Status | 200 OK |
| ------ | ------ |

```
Response Body
{
    "token":  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzOTY4NTYxOCwianRpIjoiYzg2ODFkZGEtMTM1My00NjRlLTgwOWEtM2NiM2QyNzBlNjMzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJ mIjoxNjM5Njg1NjE4LCJleHAiOjE2Mzk2ODY1MTh9.OSRXRRncVvDbWDCCOqW_PGnDp2ZQpncON9GVXBdwoLE"     
}
```

**Exceções**

1.	Login ou senha que não existem

| Status | 401 unauthorized |
| ------ | ---------------- |

```
Response Body
	  {
           "message": "O usuário ou a senha está errado"
      }
```



2.	Conta não foi verificada

| Status | 401 Bad Request |
| ------ | --------------- |

```
Response Body
	  {
                   "message": "É preciso verificar a conta para se conectar à API"
      }
```



## Consultar dados 

| METHOD | URL       |
| ------ | --------- |
| GET    | /Fernando |

| Header        |                          |
| ------------- | ------------------------ |
| Content-Type  | application/json         |
| Authorization | Bearer {token_de_acesso} |

**Resposta**

| Status | 200 OK |
| ------ | ------ |

```
Response Body
	     {
            	"Nome": "Fernando Emerson",
           	 	"Idade": 22,
            	"Telefone": "(21)98931-9729",
            	"Status Code": "200 OK "
         }
```



**Exceções**

1.	Token incorreto

| Status | 422 UNPROCESSABLE ENTITY |
| ------ | ------------------------ |

```
 Response Body
	 	 {
              "message": "Token inválido"
         }
```




1.	Token expirou

| Status | 401 unauthorized |
| ------ | ---------------- |

```
	Response Body
	 		{
                       "msg": "Token expirou"
             }
```




## Logout

| METHOD | URL     |
| ------ | ------- |
| POST   | /logout |

| Header        |                          |
| ------------- | ------------------------ |
| Content-Type  | application/json         |
| Authorization | Bearer {token_de_acesso} |

```
Request Body
{
       “message”: “Você foi deslogado!”
}
```



