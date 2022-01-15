from flaskpackage import create_app
from pyfladesk import init_gui

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    # init_gui(app, port=222, window_title="HDBM", icon="icon.png")
