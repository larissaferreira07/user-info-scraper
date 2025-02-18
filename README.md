# User Info Scraper

Este projeto fornece uma API para obter informações básicas sobre um usuário do Instagram, como o número de seguidores, a foto de perfil e o nome completo, utilizando scraping.

## Tecnologias Utilizadas
- Python 3
- Flask
- Flask-CORS
- httpx

## Instalação

1. Clone este repositório:
   ```sh
   git clone https://github.com/larissaferreira07/instagram-user-info.git
   cd instagram-user-info
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows use: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

## Como Usar

1. Inicie o servidor:
   ```sh
   python app.py
   ```

2. Faça uma requisição GET para a rota `/user` com o parâmetro `username`:
   ```sh
   curl "http://127.0.0.1:5000/user?username=instagram"
   ```

3. Resposta esperada:
   ```json
   {
       "followers_count": 1234567,
       "profile_picture_url": "https://instagram.com/path/to/profile.jpg",
       "full_name": "Nome Completo"
   }
   ```

## Cache

O projeto implementa um cache simples em memória para reduzir o número de requisições ao Instagram. O tempo de vida do cache (TTL) é de **24 horas**.

## Tratamento de Erros

A API retorna mensagens de erro apropriadas em casos como:
- Falta do parâmetro `username`.
- Falha na requisição HTTP ao Instagram.
- Erros inesperados durante o processamento.