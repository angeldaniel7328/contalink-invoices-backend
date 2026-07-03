# Contalink Invoices API

API REST desarrollada con Flask para consultar facturas almacenadas en una base de datos PostgreSQL.

## Repositorio

https://github.com/angeldaniel7328/contalink-invoices-backend

## Tecnologías

- Python 3.12
- Flask
- PostgreSQL
- SQLAlchemy
- Marshmallow
- JWT
- Flasgger
- Pytest

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/angeldaniel7328/contalink-invoices-backend.git
cd contalink-invoices-backend
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
DB_HOST=devtestdatabase.contalink.com
DB_PORT=5432
DB_NAME=testinvoices
DB_USER=developer
DB_PASSWORD=UQpaA9TA

AUTH_USERNAME=admin
AUTH_PASSWORD=admin123

JWT_SECRET_KEY=my-secret-key
```

## Ejecutar la aplicación

```bash
python run.py
```

La API estará disponible en:

```
http://localhost:5000
```

## Documentación

Swagger:

```
http://localhost:5000/apidocs/
```

## Ejecutar pruebas

```bash
python -m pytest tests
```