# Flask & Postgres CRUD

1. Clonar proyecto

2. Crear el .env a partir de .env.template

3. Instalar dependencias

```bash
pipenv shell

pipenv install
```

4. Levantar la base de datos Postgres

```bash
docker-compose up -d
```

5. Crear tablas Postgres

```bash
http://127.0.0.1:5000/api/seed
```

6. Ejecutar el servidor

```bash
python app.py
```

Endpoint: <http://127.0.0.1:5000/api/users>

 ---

##### Made with ❤️ by Leandro Arturi
