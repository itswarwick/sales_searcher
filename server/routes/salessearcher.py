from flask import Blueprint, jsonify, request
import os

salessearcher = Blueprint('salessearcher', __name__)

# Dummy login endpoint
@salessearcher.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data['username'] == os.getenv('SECRET_KEY') and data['password'] == os.getenv('PASSWORD'):
        return jsonify({'success': True})
    return jsonify({'success': False}), 401

# Dummy QuickBooks API endpoint (replace with actual API calls later)
@salessearcher.route('/items', methods=['GET'])
def get_items():
    items = [
        {'id': 1, 'name': 'Item 1'},
        {'id': 2, 'name': 'Item 2'},
        {'id': 3, 'name': 'Item 3'}
    ]
    return jsonify(items)