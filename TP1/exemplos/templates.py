from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Sofia'}
    return render_template('template.html', title='Home', user=user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)