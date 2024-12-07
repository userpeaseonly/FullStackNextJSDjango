You need to creat .local in env directory and put this example text.
```
DEBUG=1
SECRET_KEY=your secret key
DJANGO_ALLOWED_HOSTS=*




DJANGO_ENV=local
POSTGRES_ENGINE=django.db.backends.postgresql_psycopg2
POSTGRES_DB=shopping_backend_db
POSTGRES_USER=shopping_backend_db_user
POSTGRES_PASSWORD=shopping_backend_db_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

HTTP_URL=http://localhost:8010

ADMIN_EMAIL=admin@gmail.com
ADMIN_PASSWORD=aliphai4shiT0kai


CORS_ALLOWED_ORIGINS=http://0.0.0.0:8010,http://localhost:3000,http://0.0.0.0:8020,http://localhost:5173,http://172.19.0.2:5173,http://172.19.0.2:5173,http://localhost:8020
CSRF_ALLOWED_ORIGINS=http://0.0.0.0:8010,http://localhost:3000,http://0.0.0.0:8020,http://localhost:5173,http://172.19.0.2:5173,http://172.19.0.2:5173,http://localhost:8020
```
