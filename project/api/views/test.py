from aiohttp import web
from error_handler_diploma import test

async def index(request):
    test.some_method()
    return web.Response(text="Hello, world")


async def post(request):
    try:
        data = await request.json()
        error_code = int(data['error_code']) 
        error_message = data['error_message']
        await request.app['db_connection'].execute('''
            INSERT INTO handled_error (error_code, error_message)
            VALUES ($1, $2)
        ''', error_code, error_message)
        return web.Response(text="Success")
    except KeyError:
        return web.Response(text="Missing error_code or error_message", status=400)
    

async def data_structure(request):
    try:
        data = await request.json()
        name = data['name']
        username = data['user']['username']

        return web.Response(text=f"Hello, {name}! Your username is {username}.")
    except KeyError:
        return web.Response(text="Missing data", status=400)
