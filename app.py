from flask import Flask, request, jsonify, send_from_directory
import json, os, time, random, string
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'trips.json')

# ── helpers ──────────────────────────────────────────────────────────────────

def read_data():
    if not os.path.exists(DATA_FILE):
        initial = {"places": [], "expenses": [], "notes": []}
        write_data(initial)
        return initial
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def uid():
    return str(int(time.time() * 1000)) + ''.join(random.choices(string.ascii_lowercase, k=4))

# ── PLACES ───────────────────────────────────────────────────────────────────

@app.route('/api/places', methods=['GET'])
def get_places():
    category = request.args.get('category')
    data = read_data()
    places = data['places']
    if category:
        places = [p for p in places if p['category'] == category]
    return jsonify(places)

@app.route('/api/places', methods=['POST'])
def add_place():
    body = request.get_json()
    if not body.get('name') or not body.get('category'):
        return jsonify({'error': 'name and category required'}), 400
    data = read_data()
    place = {
        'id':        uid(),
        'name':      body['name'],
        'category':  body['category'],   # restaurant | museum | party | transport | must | other
        'address':   body.get('address', ''),
        'date':      body.get('date', ''),
        'time':      body.get('time', ''),
        'notes':     body.get('notes', ''),
        'link':      body.get('link', ''),
        'priority':  body.get('priority', 'normal'),  # must | high | normal
        'done':      False,
        'createdAt': datetime.now().isoformat()
    }
    data['places'].append(place)
    write_data(data)
    return jsonify(place), 201

@app.route('/api/places/<place_id>', methods=['PATCH'])
def update_place(place_id):
    data = read_data()
    place = next((p for p in data['places'] if p['id'] == place_id), None)
    if not place:
        return jsonify({'error': 'not found'}), 404
    updates = request.get_json()
    place.update(updates)
    write_data(data)
    return jsonify(place)

@app.route('/api/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    data = read_data()
    data['places'] = [p for p in data['places'] if p['id'] != place_id]
    write_data(data)
    return jsonify({'ok': True})

# ── EXPENSES ─────────────────────────────────────────────────────────────────

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    return jsonify(read_data()['expenses'])

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    body = request.get_json()
    if not body.get('description') or body.get('amount') is None:
        return jsonify({'error': 'description and amount required'}), 400
    data = read_data()
    expense = {
        'id':          uid(),
        'description': body['description'],
        'amount':      float(body['amount']),
        'currency':    body.get('currency', 'GBP'),
        'category':    body.get('category', 'other'),  # food | transport | attraction | shopping | other
        'date':        body.get('date', datetime.now().strftime('%Y-%m-%d')),
        'createdAt':   datetime.now().isoformat()
    }
    data['expenses'].append(expense)
    write_data(data)
    return jsonify(expense), 201

@app.route('/api/expenses/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    data = read_data()
    data['expenses'] = [e for e in data['expenses'] if e['id'] != expense_id]
    write_data(data)
    return jsonify({'ok': True})

# ── NOTES ────────────────────────────────────────────────────────────────────

@app.route('/api/notes', methods=['GET'])
def get_notes():
    return jsonify(read_data()['notes'])

@app.route('/api/notes', methods=['POST'])
def add_note():
    body = request.get_json()
    if not body.get('text'):
        return jsonify({'error': 'text required'}), 400
    data = read_data()
    note = {
        'id':        uid(),
        'text':      body['text'],
        'createdAt': datetime.now().isoformat()
    }
    data['notes'].append(note)
    write_data(data)
    return jsonify(note), 201

@app.route('/api/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    data = read_data()
    data['notes'] = [n for n in data['notes'] if n['id'] != note_id]
    write_data(data)
    return jsonify({'ok': True})

# ── STATS ────────────────────────────────────────────────────────────────────

@app.route('/api/stats', methods=['GET'])
def get_stats():
    data = read_data()
    places   = data['places']
    expenses = data['expenses']

    total_gbp = sum(e['amount'] for e in expenses if e['currency'] == 'GBP')
    total_ils = sum(e['amount'] for e in expenses if e['currency'] == 'ILS')

    by_category = {}
    for p in places:
        by_category[p['category']] = by_category.get(p['category'], 0) + 1

    return jsonify({
        'totalPlaces':   len(places),
        'donePlaces':    sum(1 for p in places if p['done']),
        'mustSee':       sum(1 for p in places if p['priority'] == 'must'),
        'totalSpentGBP': round(total_gbp, 2),
        'totalSpentILS': round(total_ils, 2),
        'byCategory':    by_category
    })

# ── SERVE FRONTEND ───────────────────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
