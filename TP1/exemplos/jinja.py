import jinja2 as j2
from jinja2 import Environment, BaseLoader
import random as ra

feelings = [{'feeling':'hate', 'object':'sweater'}, {'feeling':'love', 'object':'sunglasses'}, {'feeling':'despise', 'object':'shoes'}]
title = "Greetings"
username = 'João'
g = False

txt = j2.Template('''
<html>
    <head>
        <title>{{ title }}</title>
    </head>
    <body>
        {% set hello=True %}
        {% if hello %}
        <h1>Hello {{ username }}</h1>
        {% else %}
        <h1>Goodbye {{ username }}</h1>
        {% endif %}
        {% for f in feelings %}
            <h2> I {{f.feeling}} your {{f.object}}.<h2>
        {% endfor %}
    </body>
</html>
''').render(feelings=feelings,title=title,username=username, hello=g)

form = j2.Environment(loader=j2.FileSystemLoader('.')).from_string('''
{% import 'forms.html' as forms %}
<dl>
    <dt>Username</dt>
    <dd>{{ forms.input('João') }}</dd>
    <dt>Password</dt>
    <dd>{{ forms.input('password', type='password') }}</dd>
</dl>
<p>{{ forms.textarea('comment', rows=15, cols=20) }}</p>
''').render()

print(form)