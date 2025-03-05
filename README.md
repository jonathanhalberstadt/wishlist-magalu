
# 📌 Wishlist API

API RESTful para lista de desejos da Magalu, desenvolvida em Python e Dockerizada para o teste técnico.

A API permite a criação de clientes, lista de favoritos.

Por conta do enunciado estar em português, mantive tudo em linguagem nativa.

## 🛠 Tecnologias Utilizadas

- **Python**
- **Flask**
- **Docker & Docker Compose**
- **Postgree**
- **Composer**
- **Uwsgi**

## 🚀 Instalação e Configuração

## Dependências

- [GNU make](https://www.gnu.org/software/make/)
- [docker-engine](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/)
- [docker-compose](https://docs.docker.com/compose/install/)

### 1. Clonar o Repositório
```bash
git clone https://github.com/jonathanhalberstadt/wishlist-magalu
cd wishlist-magalu
```


### 2. Criar o Arquivo .env
```bash
cp .env.example .env
```

⚠️ **Configurar as variáveis do banco de dados e outros parâmetros necessários no arquivo `.env`.**

### 3. Construir e Rodar os Containers

```bash
make build
make up
```

### 4. Rodar as Migrações e Criar o banco
```bash
make migration
```

## 🔗 Rotas da API

### Auntenticação

**GET** `/auth/authenticate`

**Corpo da Requisição:**
```bash
{
    "email": "user@email.com",
    "password": "senha123"
}
```

### Todas as rotas a seguir exigem um Header de Authorization

### Criar Cliente

**POST** `/client`

**Corpo da Requisição:**
```bash
{
    "name": "teste",
    "email": "teste2@teste.com"
}
```

### Editar Cliente

**PUT** `/client/{id/email}`

**Corpo da Requisição:**
```bash
{
    "name": "teste"
}
```

### Visualizar Cliente

**GET** `/client/{id/email}`



### Editar Cliente

**DELETE** `/client/{id/email}`



### Adicionar Wishlist

**POST** `/wishlist`

**Corpo da Requisição:**
```bash
{
    "client_id": 1,
    "product_id": 123
}
```


### Adicionar Wishlist

**GET** `/wishlist?client_id=1`



## 🧪 Rodando os Testes

Para rodar os testes, utilize:
```bash
make test
```

```bash
php lint
```

## 📦 Gerenciamento do Container

- **Subir os containers:**
    ```
    make up 
    ```
- **Parar os containers:**
    ```
    make down 
    ```
- **Reiniciar:**
    ```
    make restart 
    ```
- **Ver logs:**
    ```
    make logs 
    ```
- **Acessar o container:**
    ```
    make exec 
    ```

## 🏁 Conclusão

O projeto `wishlist-magalu` fornece uma API para operações manipulação de clientes e salvar as lista de favoritos. O uso de Docker e um Makefile facilita a execução e testes do sistema.
Por motivos da api de produtos estar com instabilidade, criei um sistema de cache local, mas o correto seria usar um cache redis com o ultimo retorno da API.