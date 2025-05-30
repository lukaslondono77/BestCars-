from flask import Flask, jsonify
from textblob import TextBlob


app = Flask(__name__)


@app.route('/analyze/<text>', methods=['GET'])
def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text using TextBlob
    Returns a sentiment score between -1 (negative) and 1 (positive)
    """
    try:
        # Create a TextBlob object
        blob = TextBlob(text)

        # Get the sentiment polarity (-1 to 1)
        sentiment = blob.sentiment.polarity

        # Determine the sentiment label
        if sentiment > 0:
            label = "positive"
        elif sentiment < 0:
            label = "negative"
        else:
            label = "neutral"

        return jsonify({
            "sentiment": sentiment,
            "label": label
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
