from website import create_app
from flask import Flask,render_template,request



app = create_app()


if __name__ == '__main__':
    app.run(debug=True)#It will run our flask application.
    #debug = True means every time we make a change to our python code,its going to automatically
    #rerun the webserver