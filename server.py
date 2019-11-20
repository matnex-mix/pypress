'''
Listen to port 2020 and run PyPress
might use another implementation at production
'''

from wsgiref.simple_server import make_server
from models.artifacts import Validator
from models.template import Render
import os,mimetypes

status = '200 OK'
mime = "text/html"

def routeProcessing( request_path ):
    global status, mime
    allowInitFiles = True

    if( request_path.endswith('.py') and request_path.startswith('/models/ajax') and os.path.isfile('.'+request_path) ):
        return os.popen('python .'+request_path).read().encode('utf-8')
    elif( request_path.startswith('/uploads') and os.path.isfile('.'+request_path) ):
        mime = mimetypes.MimeTypes().guess_type('.'+request_path)[0]
        if(not(mime)):
            mime = 'text/plain'
        with open('.'+request_path) as static_file:
            return static_file.read().encode('utf-8')
    # Use the artifacts validator
    elif( Validator.isPost('') ):
        return os.popen('python controllers/post.py '+request_path).read().encode('utf-8')
    else:
        status = '404 ERROR'
        return os.popen('python controllers/404.py').read().encode('utf-8')

def application (environ, start_response):
    # response_body = routeProcessing(environ['PATH_INFO'])
    response_body = Render('views\\pypress-2020\\templates\\test',{
        'test': 1,
        'triple': 2
    }).show().encode('utf-8')
    
    response_headers = [
        ('Content-Type', mime),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)
    return [response_body]


httpd = make_server ('', 2020, application)
httpd.serve_forever()