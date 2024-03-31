from aiohttp import web

async def index(request):
    return web.Response(text="Hello, world")

# async def greet(request):
#     return web.Response(text="hello, buddy!")

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