# LOGIN SYSTEM

- Sistema de login desenvolvido em Python com foco em fundamentos de backend,
segurança básica e arquitetura cliente-servidor.

- O projeto foi criado como prática de lógica de programação, validação de dados
e hash de senha utilizando werkzeug.security, sem uso de ORM, para reforçar
o entendimento de SQL.


# TECNOLOGIAS UTILIZADAS
- Python
- Flask (API REST)
- SQLite
- Tkinter (interface desktop)
- Werkzeug (hash e verificação de senha)
- Docker (containerização do backend)
- HTTP / JSON


# PARA QUE SERVE
- Treinar autenticação de usuários
- Praticar validação de dados no backend
- Compreender comunicação entre frontend e backend via API
- Aplicar boas práticas básicas de segurança (hash de senha)
- Consolidar conceitos de SQL sem ORM


# COMO USAR

1) Backend (API)

Comandos:
- docker build -t login-api .
- docker run -p 5000:5000 login-api

A API ficará disponível em:
- http://127.0.0.1:5000
---

2) Interface (Tkinter)
- Comando:
- python interface.py

---

3) Ao subir a API e rodar a interface.
- Basta fazer o seu cadastro, fazer o seu login e você já está pronto para usar o sistema!

---

4) Funcionalidades

Funcionalidades disponíveis no sistema:
- Cadastro de usuário
- Login com verificação de senha
- Criação de livros via POSTMAN ou pelo próprio sistema.
- Atualizar usuário (via POSTMAN) ou livro (via POSTMAN ou pela API)
- Deletar usuario (via POSTMAN) ou livro (via POSTMAN ou pela API)

# ENDPOINTS PRINCIPAIS
- POST /users  -> cadastro de usuário
- POST /login  -> autenticação
- GET /users  -> listagem de usuários (sem senha)
- DELETE /users/id  -> deleta usuário
- PATCH /users/id  -> atualiza usuário
- POST /books  -> cadastra livro
- GET /books  -> listagem de livros (por id)


# PRÓXIMOS PASSOS
- Implementar autenticação com JWT
- Criar CRUD completo de usuários e livros
- Adicionar testes automatizados
- Melhorar layout da interface
- Deploy da API em ambiente cloud

