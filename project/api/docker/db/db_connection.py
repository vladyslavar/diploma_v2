import asyncpg

async def get_db_connection():
    return await asyncpg.connect(user='user', password='pass', database='error_handler_db', host='diploma_postgres_db')

async def close_db_connection(connection):
    connection.close()
