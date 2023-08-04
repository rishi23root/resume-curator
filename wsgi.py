from flaskApi import app 
from flaskApi.middleware import LoggingMiddleware

if __name__ == '__main__':
    # app.wsgi_app = LoggingMiddleware(app.wsgi_app) # type: ignore
    app.run(debug=False)
    # app.secret_key = 'super secret key'
