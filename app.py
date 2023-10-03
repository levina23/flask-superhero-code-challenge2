from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


CORS(app)

migrate = Migrate(app, db)

db.init_app(app)
api =Api(app)



@app.route('/')
def home():
    return '<h1>id": 1, "name": "Kamala Khan", "super_name": "Ms. Marvel</h1>'
           

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(hero_list)

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        hero_info = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': hp.power.id, 'name': hp.power.name, 'description': hp.power.description} for hp in hero.powers]
        }
        return jsonify(hero_info)
    else:
        return jsonify({'error': 'Hero not found'}), 404

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(power_list)

@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power:
        power_info = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        return jsonify(power_info)
    else:
        return jsonify({'error': 'Power not found'}), 404

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    data = request.get_json()
    description = data.get('description')
    if not description:
        return jsonify({'errors': ['description is required']}), 400
    power.description = description
    db.session.commit()
    return jsonify({
        'id': power.id,
        'name': power.name,
        'description': power.description
    })

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')
    if not strength or strength not in ['Strong', 'Weak', 'Average']:
        return jsonify({'errors': ['strength must be one of: Strong, Weak, Average']}), 400
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)
    if not hero or not power:
        return jsonify({'errors': ['Hero or Power not found']}), 404
    hero_power = HeroPower(strength=strength, hero=hero, power=power)
    db.session.add(hero_power)
    db.session.commit()
    hero_info = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': [{'id': hp.power.id, 'name': hp.power.name, 'description': hp.power.description} for hp in hero.powers]
    }
    return jsonify(hero_info), 201

if __name__ == '_main_':
    app.run(port=5555)