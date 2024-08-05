import requests

def emotion_detector(text_to_analyze):
    if not text_to_analyze.strip():  # Check for blank input
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    input_json = {"raw_document": {"text": text_to_analyze}}

    response = requests.post(url, headers=headers, json=input_json)

    if response.status_code == 200:
        response_json = response.json()
        print("Response JSON:", response_json)  # Debugging line

        # Extract emotions from the response
        try:
            emotion_data = response_json['emotionPredictions'][0]['emotion']
        except (KeyError, IndexError):
            emotion_data = {}

        print("Extracted Emotions:", emotion_data)  # Debugging line

        anger = emotion_data.get('anger', 0)
        disgust = emotion_data.get('disgust', 0)
        fear = emotion_data.get('fear', 0)
        joy = emotion_data.get('joy', 0)
        sadness = emotion_data.get('sadness', 0)

        # Find the dominant emotion
        emotion_scores = {
            'anger': anger,
            'disgust': disgust,
            'fear': fear,
            'joy': joy,
            'sadness': sadness
        }
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)

        return {
            'anger': anger,
            'disgust': disgust,
            'fear': fear,
            'joy': joy,
            'sadness': sadness,
            'dominant_emotion': dominant_emotion
        }
    elif response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    else:
        return {
            'error': f"Error: {response.status_code}, {response.text}"
        }
