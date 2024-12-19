from flask import Flask, request, jsonify
import os
import hashlib
from datetime import datetime

app = Flask(__name__)

@app.route('/notes', methods=['POST'])
def add_note():
    print("hahaha")
    note = request.json.get('note')
    if note:
        note_id = hashlib.sha256(datetime.now().isoformat().encode()).hexdigest()
        with open(f'notes/{note_id}', 'w') as f:
            f.write(note)
        return jsonify({'success': True, 'note_id': note_id})
    return jsonify({'success': False})

@app.route('/notes', methods=['GET'])
def get_notes():
    notes = []
    for note_id in os.listdir('notes'):
        with open(f'notes/{note_id}', 'r') as f:
            notes.append({'note_id': note_id, 'note': f.read()})
    return jsonify(notes)

if __name__ == '__main__':
    app.run()

