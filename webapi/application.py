from tempfile import NamedTemporaryFile

from bottle import route, run, template, default_app, request

application = default_app()

#@route('/')
#def index(name):
#    return template('<b>Hello {{name}}</b>!', name='world')

@route('/', method='POST')
def do_upload():
    img = request.files.get('image')

    with NamedTemporaryFile('w+b') as f:
        img.save(f)

    return 'Trump'


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
