from flask import Flask
import requests
 
app = Flask(__name__)
 
@app.route("/")
def index():
    nome = "João Gomes"
    numero = "a82238"
    curso = "MIEI"

    html = f"""
    <html>
      <head>
        <title>Exemplo a usar variavéis python</title>
        <meta charset="utf8"/>
      </head>
      <body>
        <ul>
            <li>Nome: {nome}</li>
            <li>Número: {numero}</li>
            <li>Curso: {curso}</li>
        </ul>
      </body>
    </html>
    """
    return html

 
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)


