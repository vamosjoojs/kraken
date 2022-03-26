
## Criar migração
`poetry run alembic revision --autogenerate -m "nome"`

## Aplicar migração
`poetry run alembic upgrade head`