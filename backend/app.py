from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp_utils import analyze_email

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'ok',
        'message': 'Smart Email Summarizer Backend is running'
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json(silent=True)
        if not data or 'email_text' not in data:
            return jsonify({'error': 'email_text is required'}), 400

        email_text = str(data.get('email_text', '')).strip()
        if not email_text:
            return jsonify({'error': 'Email text cannot be empty'}), 400

        result = analyze_email(email_text)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            'error': 'Email analysis failed',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
