from app import create_app
from config import Config


app = create_app()
debug_mode = Config.DEBUG

if __name__ == '__main__':
    app.run(debug=True)
