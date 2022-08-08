from flask import Flask

app = Flask(__name__)


@app.route('/api/external/orders/v1/create')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
