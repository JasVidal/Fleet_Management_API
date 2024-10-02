from flask import Flask

#Se crea instancia de clase
app = Flask(__name__)

#Usa decorador para indicar el URL
@app.route('/taxis', methods=['GET'])
def hello_world():
    return "¡Hola mundo  :DD!"


if __name__ == '__main__':
    app.run(debug=True)