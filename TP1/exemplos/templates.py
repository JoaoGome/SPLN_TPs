from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def show():
    user = {'username': 'Joao', 'age': '22'}
    return render_template('template.html', title='Exemplo', user=user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)