# HackatonF5Back
Repo del backend del hackaton

Estructua del .env para trabajar en local con Docker:

DATABASE_URL=postgresql+asyncpg://user:password@localhost:5433/db_name 
- DB_TYPE=postgresql+asyncpg 
- DB_HOST=localhost 
- DB_PORT=5433 
- DB_DB=db_name 
- DB_SCHEMA=schema_name 
- DB_USER=user 
- DB_PASSWORD=password
- DEBUG=true 

Estructura del .env para que el bot funcione:
- HUGGINGFACEHUB_API_TOKEN= "token de hf"//
- USER_AGENT= "nombre del bot"//
