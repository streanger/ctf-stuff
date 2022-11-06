from rich import print
from flask import Flask
from flask import request

"""
useful:
    https://flask.palletsprojects.com/en/1.1.x/cli/
    Windows CMD:
        > set FLASK_APP=app
        > flask run
    Windows PowerShell:
        > $env:FLASK_APP = "app"
        > flask run
        
    https://stackoverflow.com/questions/22947905/flask-example-with-post
    https://stackoverflow.com/questions/29386995/how-to-get-http-headers-in-flask
    
info:
    you need to set dns or etc/hosts like this:
        127.0.0.1 flare-on.com
        
"""

app = Flask(__name__)

def response_content(key):
    base1 = 'TdQdBRa1nxGU06dbB27E7SQ7TJ2+cd7zstLXRQcLbmh2nTvDm1p5IfT/Cu0JxShk6tHQBRWwPlo9zA1dISfslkLgGDs41WK12ibWIflqLE4Yq3OYIEnLNjwVHrjL2U4Lu3ms+HQc4nfMWXPgcOHb4fhokk93/AJd5GTuC5z+4YsmgRh1Z90yinLBKB+fmGUyagT6gon/KHmJdvAOQ8nAnl8K/0XG+8zYQbZRwgY6tHvvpfyn9OXCyuct5/cOi8KWgALvVHQWafrp8qB/JtT+t5zmnezQlp3zPL4sj2CJfcUTK5copbZCyHexVD4jJN+LezJEtrDXP1DJNg=='
    base2 = 'F1KFlZbNGuKQxrTD/ORwudM8S8kKiL5F906YlR8TKd8XrKPeDYZ0HouiBamyQf9/Ns7u3C2UEMLoCA0B8EuZp1FpwnedVjPSdZFjkieYqWzKA7up+LYe9B4dmAUM2lYkmBSqPJYT6nEg27n3X656MMOxNIHt0HsOD0d+'
    if key == 'base1':
        return base1
    elif key == 'base2':
        return base2
    else:
        return ''
        
        
@app.route('/', methods = ['GET', 'POST'])
def index():
    print(request.headers)
    user_agent = request.headers.get('User-Agent')
    user_agent_end = user_agent.split()[-1].rstrip(')')
    content_length = request.headers.get('Content-Length')
    
    if request.method == 'GET':
        return 'not interested in that'
    elif request.method == 'POST':
        # if user_agent_end == 'CLR':
        if content_length == 24:
            return response_content('base1')
        else:
            return response_content('base2')
    else:
        return 'in that too'
        
        
if __name__ == "__main__":
    app.run(port=80)
    