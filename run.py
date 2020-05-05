from tracker import create_app
from tracker.config import ConfigProd

#app = create_app()
app = create_app(ConfigProd)

if __name__ == '__main__':
    app.run(debug=False)
    #app.run(debug=True)