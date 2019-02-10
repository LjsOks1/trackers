from wsgiref.simple_server import make_server

# obtain the WSGI request dispatcher
from roundup.cgi.wsgi_handler import RequestDispatcher
tracker_home = 'tpm'
application = RequestDispatcher(tracker_home)

#httpd = make_server('', 8080, application)
#httpd.serve_forever()
