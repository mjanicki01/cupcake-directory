from flask import Flask, request, jsonify, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
from forms import AddCupcake
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcake_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)

connect_db(app)
#db.drop_all()
db.create_all()


@app.route('/')
def render_page():

    addform = AddCupcake()
    cupcakes = Cupcake.query.all()

    return render_template('index.html', cupcakes=cupcakes, addform=addform)



@app.route('/api/cupcakes')
def list_cupcakes():

    all_cupcakes = [Cupcake.serialize(cupcake) for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes=all_cupcakes)
    


@app.route('/api/cupcakes', methods=["POST"])
def post_cupcake():

        flavor = request.json["flavor"],
        size = request.json["size"],
        rating = request.json["rating"],
        image = request.json["image"] or None

        new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

        db.session.add(new_cupcake)
        db.session.commit()

        serialized_cupcake = Cupcake.serialize(new_cupcake)

        return (jsonify(cupcake=serialized_cupcake))



@app.route('/api/cupcakes/<int:id>', methods=["GET"])
def cupcake_detail(id):

    cupcake = Cupcake.query.get_or_404(id)
    serialized_cupcake = Cupcake.serialize(cupcake)

    return jsonify(cupcake=serialized_cupcake)



@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def patch_cupcake(id):

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()

    return jsonify(cupcake=Cupcake.serialize())



@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):

    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted cupcake")