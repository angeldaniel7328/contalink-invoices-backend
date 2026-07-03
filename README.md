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

## Autenticación

Obtener un token JWT utilizando autenticación Basic.

```bash
curl --request POST \
  --url http://localhost:5000/api/auth/login \
  --user admin:admin123
```

Respuesta:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2026-07-04T12:30:45+00:00",
  "expires_in": 3600
}
```

---

## Consultar facturas

Utiliza el token obtenido en el endpoint de autenticación.

```bash
curl --request GET \
  --url "http://localhost:5000/api/invoices?start_date=2022-01-01&end_date=2022-01-31" \
  --header "Authorization: Bearer <ACCESS_TOKEN>"
```

Respuesta:

```json
{
  "total": 1454,
  "page": 1,
  "page_size": 10,
  "total_pages": 146,
  "items": [
    {
      "id": 1270,
      "invoice_number": "C29718",
      "total": "10.0",
      "invoice_date": "2022-01-03T07:50:08",
      "status": "Vigente",
      "active": false
    }
  ]
}
```