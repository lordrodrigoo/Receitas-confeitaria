# Deploy do Projeto Receitas Confeitaria

Este guia cobre o passo a passo para realizar o deploy do projeto Django com Docker, Nginx e Postgres em produção (exemplo: AWS EC2, DigitalOcean, VPS, etc).

---

## 1. Pré-requisitos
- Docker e Docker Compose instalados no servidor
- Acesso SSH ao servidor
- Domínio configurado (opcional, mas recomendado)
- Certificados SSL (Let’s Encrypt ou similar, recomendado para produção)

---

## 2. Clonando o repositório

No servidor, clone o projeto:
```sh
git clone <URL_DO_REPOSITORIO>
cd Receitas-confeitaria
```

---

## 3. Configurando variáveis de ambiente

1. **NUNCA suba o arquivo `.env` real para o repositório!**
2. Copie o exemplo:
   ```sh
   cp .env.example .env
   ```
3. Edite o `.env` com os valores reais de produção (SECRET_KEY, credenciais do banco, hosts, etc):
   ```env
   DATABASE_ENGINE=django.db.backends.postgresql
   DATABASE_NAME=receitas
   DATABASE_USER=usuario_prod
   DATABASE_PASSWORD=senha_segura
   DATABASE_HOST=db
   DATABASE_PORT=5432
   ALLOWED_HOSTS=seusite.com,www.seusite.com
   CSRF_TRUSTED_ORIGINS=https://seusite.com,https://www.seusite.com
   CORS_ALLOWED_ORIGINS=https://seusite.com,https://www.seusite.com
   # ...demais variáveis...
   ```

---

## 4. Ajustando arquivos de deploy

- **docker-compose.yml**: Certifique-se de que está usando o serviço `db` (Postgres) e volumes corretos.
- **nginx.conf**: Configure o domínio, SSL e paths conforme produção.
- **entrypoint.sh**: Certifique-se de que está rodando as migrations, collectstatic e o Gunicorn.

---

## 5. Subindo a stack

No diretório do projeto, execute:
```sh
docker-compose up -d --build
```

---

## 6. Pós-deploy

- Acesse o site pelo domínio/IP para validar.
- Crie o superuser:
  ```sh
  docker-compose exec django-web python manage.py createsuperuser
  ```
- Verifique logs:
  ```sh
  docker-compose logs -f
  ```
- Teste upload de imagens, login/admin, etc.

---

## 7. SSL (Let’s Encrypt)

- Se usar Nginx no container, monte o volume `/etc/letsencrypt` e configure o SSL no `nginx.conf`.
- Use Certbot para gerar/renovar certificados:
  ```sh
  sudo certbot certonly --standalone -d seusite.com -d www.seusite.com
  ```
- Atualize o `nginx.conf` para apontar para os certificados.

---

## 8. Backup e manutenção

- Configure backup do volume do Postgres (pg_dump + cron/S3).
- Faça backup regular da pasta `media`.
- Documente o procedimento de restore.

---

## 9. Atualizando o deploy

1. Faça pull do repositório:
   ```sh
   git pull origin main
   ```
2. (Opcional) Atualize o `.env` se necessário.
3. Suba novamente:
   ```sh
   docker-compose up -d --build
   ```

---

## 10. Dicas finais

- Nunca suba `.env` real para o Git.
- Sempre teste local antes de subir para produção.
- Use `.env.example` para documentar as variáveis necessárias.

---


