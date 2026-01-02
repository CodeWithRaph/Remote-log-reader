from app import create_app
from config import Config

app = create_app(Config)

if __name__ == '__main__':
    import os
    debug = os.getenv('FLASK_DEBUG') == 1
    app.run(host="0.0.0.0", port="5000", debug=debug)