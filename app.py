from flask import Flask # type: ignore
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Budget App Backend!'

if __name__ == '__main__':
    app.run(debug=True)

