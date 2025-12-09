#
## Demonstração
Veja abaixo algumas telas do sistema em funcionamento:

### Desktop
<p align="center">
	<img src="docs/home.png" alt="Home Desktop" width="700"/>
	<br>
	<img src="docs/dashboard.png" alt="Dashboard Desktop" width="700"/>
	<br>
	<img src="docs/dashboard-add-recipe.png" alt="Adicionar Receita" width="700"/>
</p>

### Mobile
<p align="center">
	<img src="docs/home-mobile.png" alt="Home Mobile" width="300"/>
	<br>
	<img src="docs/dashboard-mobile.png" alt="Dashboard Mobile" width="300"/>
	<br>
	<img src="docs/recipe-mobile.png" alt="Receita Mobile" width="300"/>
</p>

---
# Receitas Confeitaria 🍰

Sistema completo para gestão de receitas, usuários e dashboard administrativo para confeitarias.


![Python](https://img.shields.io/badge/python-3.12-blue?logo=python)
![Django](https://img.shields.io/badge/django-5.2-green?logo=django)
![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)
![Nginx](https://img.shields.io/badge/nginx-ready-green?logo=nginx)
![PostgreSQL](https://img.shields.io/badge/postgresql-ready-blue?logo=postgresql)
![SQLite](https://img.shields.io/badge/sqlite-ready-lightgrey?logo=sqlite)
![JavaScript](https://img.shields.io/badge/javascript-ES6-yellow?logo=javascript)
![HTML5](https://img.shields.io/badge/html5-ready-orange?logo=html5)
![CSS3](https://img.shields.io/badge/css3-ready-blue?logo=css3)
![Bootstrap](https://img.shields.io/badge/bootstrap-5.x-purple?logo=bootstrap)
![Pytest](https://img.shields.io/badge/pytest-tested-green?logo=pytest)
![Selenium](https://img.shields.io/badge/selenium-tested-green?logo=selenium)
![GitHub Actions](https://img.shields.io/badge/ci-github--actions-blue?logo=githubactions)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-97%25-success)


---

## Visão Geral

- **Frontend:** HTML5, CSS3, Bootstrap, responsivo e otimizado para mobile.
- **Backend:** Django 5.2, Python 3.12, REST API, autenticação JWT.
- **Testes:** Pytest, Selenium, cobertura profissional (>97%).
- **Infra:** Docker, Docker Compose, Nginx, PostgreSQL/SQLite.
- **CI/CD:** Workflows prontos para integração contínua.

---

## Funcionalidades
- Cadastro e login de usuários (admin e comum)
- CRUD de receitas, categorias e usuários
- Dashboard administrativo com permissões
- Upload de imagens
- Testes automatizados e cobertura
- Deploy fácil com Docker

---

## Instalação Rápida

```bash
# Clone o projeto
 git clone https://github.com/lordrodrigoo/Receitas-confeitaria.git
 cd Receitas-confeitaria

# Crie o .env (veja exemplo em .env.example)
 cp .env-example .env

# Suba com Docker
 docker-compose up -d --build

# Acesse: http://localhost:8000
```

---

## Testes

```bash
# Ative o venv e rode:
pytest --cov=.
# Ou com Docker:
docker-compose exec django-web pytest --cov=.
```

---

## Deploy

<p align="center">
  <img src="../docs/deploy.png" alt="Deploy realizado com sucesso" width="700"/>
</p>
<p align="center"><i>Deploy realizado com sucesso</i></p>

Veja instruções detalhadas em [deploy/README.md](deploy/README.md)

---

## Stack
- Python 3.12
- Django 5.2
- PostgreSQL/SQLite
- Docker, Nginx
- Pytest, Selenium

---


