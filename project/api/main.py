from aiohttp import web
from routes import setup_routes
from db_connection import get_db_connection, close_db_connection

async def on_startup(app):
    app['db_connection'] = await get_db_connection()

async def on_shutdown(app):
    await close_db_connection(app['db_connection'])

print('Starting server',flush=True)

app = web.Application()
setup_routes(app)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

web.run_app(app, port=8080)