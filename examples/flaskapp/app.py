from flask import Flask, render_template

import conjur

app = Flask(__name__)

conjur.config.url = 'http://localhost:3030'
conjur.config.account = 'example'

api = conjur.new_from_password('admin', 'secret')  # TODO: swap this out with host creds


@app.route('/')
def home():
    secrets = [
        api.resource('variable', 'dbpassword'),
        api.resource('variable', 'aws_access_key_id'),
        api.resource('variable', 'aws_secret_access_key'),
    ]
    return render_template('home.html', secrets=secrets)

if __name__ == '__main__':
    app.run('0.0.0.0', 8080)
