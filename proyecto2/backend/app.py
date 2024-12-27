from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/login")
def login():
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
    </head>
    <body>
        <h1>Login</h1>
        <form method="post" action="/login/submit">
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username"><br><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password"><br><br>
            <input type="submit" value="Login">
        </form>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route("/login/submit", methods=["POST"])
def submit_login():
    # Lógica para manejar el login (sin bases de datos)
    return "Login submitted (simulado)"

if __name__ == "__main__":
    app.run(port=5000)
