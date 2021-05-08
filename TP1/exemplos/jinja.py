import jinja2 as j2
import random as ra

feelings = [{'feeling':'hate', 'object':'sweater'}, {'feeling':'love', 'object':'sunglasses'}, {'feeling':'despise', 'object':'shoes'}]
title = "Greetings"
username = 'João'
greet = [True, False]
g = ra.choice(greet)

txt = j2.Template('''
<html>
    <head>
        <title>{{ title }}</title>
    </head>
    <body>
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

print(txt)
