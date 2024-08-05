"""
server.py

This module provides a Flask web service that analyzes text input to detect emotions.
It exposes an endpoint '/emotionDetector' to receive POST requests containing text and
returns the emotion analysis result as a JSON response.
"""

from flask import Flask, request, jsonify
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def emotion_detector_route():
    """
    Endpoint to analyze the emotion of a given text.

    Returns:
        str: Formatted response message.
    """
    data = request.json
    text_to_analyze = data.get('text', '')
    result = emotion_detector(text_to_analyze)

    # Handle the case where dominant_emotion is None
    if result.get('dominant_emotion') is None:
        formatted_response = "Invalid text! Please try again!"
    else:
        response = {
            'anger': result.get('anger', 0),
            'disgust': result.get('disgust', 0),
            'fear': result.get('fear', 0),
            'joy': result.get('joy', 0),
            'sadness': result.get('sadness', 0),
            'dominant_emotion': result.get('dominant_emotion', '')
        }
        formatted_response = (
            f"For the given statement, the system response is 'anger': {response['anger']}, "
            f"'disgust': {response['disgust']}, 'fear': {response['fear']}, "
            f"'joy': {response['joy']} and 'sadness': {response['sadness']}. "
            f"The dominant emotion is {response['dominant_emotion']}."
        )

    return jsonify(formatted_response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
