CREATE DATABASE orbis_db;

DROP DATABASE orbis_db;

GRANT ALL PRIVILEGES ON orbis_db.* TO 'orbis_user'@'localhost';
FLUSH PRIVILEGES;

# Alembic
alembic revision --autogenerate -m "publication_contributors"
alembic upgrade head