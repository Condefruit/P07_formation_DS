from flask import Flask, request, jsonify

# Crée l’objet application Flask, qui contient les données de l’application et les méthodes.
app = Flask(__name__)
# Modyfying part of the original config / check print(app.config)
app.config["DEBUG"] = True
#app.config['JSON_SORT_KEYS'] = False

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

    
if __name__ == '__main__':
    app.run()

