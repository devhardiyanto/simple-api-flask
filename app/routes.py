# app/routes.py

from flask import Blueprint, request, jsonify
from .models import db, Item

main = Blueprint('main', __name__)

@main.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'id': item.id, 'name': item.name, 'description': item.description} for item in items])

@main.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify({'id': item.id, 'name': item.name, 'description': item.description})

@main.route('/items', methods=['POST'])
def create_item():
    data = request.json
    new_item = Item(name=data['name'], description=data.get('description', ''))
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item created', 'item': {'id': new_item.id, 'name': new_item.name, 'description': new_item.description}}), 201

@main.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.json
    item.name = data['name']
    item.description = data.get('description', item.description)
    db.session.commit()
    return jsonify({'message': 'Item updated', 'item': {'id': item.id, 'name': item.name, 'description': item.description}})

@main.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'})