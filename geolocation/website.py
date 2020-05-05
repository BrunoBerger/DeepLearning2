from bottle import route, run, template

import webbrowser


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

webbrowser.open('http://localhost:8080/hello/Test', new=2, autoraise=True)
print("all done")

run(host='localhost', port=8080)
