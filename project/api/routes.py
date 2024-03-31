from views import *

def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_post('/post', post)
    # app.router.add_get('/hi', greet)