from webob import Response

from api import API
app = API(static_dir="templates")

# @app.route('/')
# def hi(request, response: Response):
#     return 'Hello world'

# @app.route('/')
# def hi():
#     return 'Hello world'

@app.route('/')
def create_home(request, response):
    response.body = app.template('index.html').encode()

@app.route('/hi/{name}')
def hi_world(request, response: Response, name):
    response.text = f"Hi {name}"
    return response





class Pupil:

    # def get(self, request, response: Response):
    #     response.text = "This is get method"

    def get(self, request, response: Response):
        response.text = "Abror se gap"

app.add_route('/wow', Pupil)

# @app.route('/home')
# def hi(request, response):
#     response.text = "hi Abror"
#
# @app.route('/home')
# def hi(request, response):
#     response.text = "hi Me"