from flask import Flask

#Se crea instancia de clase
app = Flask(__name__)

#Usa decorador para indicar el URL
@app.route('/')
def hello_world():
    return "<p>¡Hello, World!</p>"


if __name__ == '__main__':
    app.run(debug=True)