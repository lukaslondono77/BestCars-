from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/fetchDealers', methods=['GET'])
def get_dealers():
    conn = get_db_connection()
    dealers = conn.execute('SELECT * FROM djangoapp_dealer').fetchall()
    conn.close()
    return jsonify([dict(dealer) for dealer in dealers])

@app.route('/fetchDealer/<int:dealer_id>', methods=['GET'])
def get_dealer(dealer_id):
    conn = get_db_connection()
    dealer = conn.execute('SELECT * FROM djangoapp_dealer WHERE id = ?', (dealer_id,)).fetchone()
    conn.close()
    return jsonify(dict(dealer)) if dealer else jsonify({})

@app.route('/fetchReviews/dealer/<int:dealer_id>', methods=['GET'])
def get_reviews(dealer_id):
    conn = get_db_connection()
    reviews = conn.execute('SELECT * FROM djangoapp_cardealerreview WHERE dealership_id = ?', (dealer_id,)).fetchall()
    conn.close()
    return jsonify([dict(review) for review in reviews])

@app.route('/insert_review', methods=['POST'])
def add_review():
    data = request.json
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO djangoapp_cardealerreview (name, dealership_id, review, purchase, purchase_date, car_make, car_model, car_year, sentiment)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['name'],
        data['dealership'],
        data['review'],
        data['purchase'],
        data['purchase_date'],
        data['car_make'],
        data['car_model'],
        data['car_year'],
        data.get('sentiment', 'neutral')
    ))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3030) 