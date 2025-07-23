from flask import Flask, render_template, request, jsonify
import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig, SafetySetting, HarmCategory, HarmBlockThreshold

# Initialize Vertex AI
PROJECT_ID = "sesac-ericyum9196"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Load the model
        # Cloud Run 배포 리전에서 사용 가능한 모델로 설정
        # gemini-1.5-flash-001 또는 gemini-1.0-pro 등 사용 가능한 모델로 변경 필요
        model = GenerativeModel("gemini-2.5-flash") 

        user_message = request.form['message']

        # GenerationConfig 설정 (이전 코드의 generate_content_config 대체)
        generation_config = GenerationConfig(
            temperature=1.0,
            top_p=1.0,
            max_output_tokens=8192, # Cloud Run 환경에 맞게 조정
        )

        # SafetySetting 설정 (이전 코드의 safety_settings 대체)
        safety_settings = [
            SafetySetting(category=HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=HarmBlockThreshold.BLOCK_NONE),
            SafetySetting(category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=HarmBlockThreshold.BLOCK_NONE),
            SafetySetting(category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=HarmBlockThreshold.BLOCK_NONE),
            SafetySetting(category=HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=HarmBlockThreshold.BLOCK_NONE),
        ]

        # Generate content
        response = model.generate_content(
            [Part.from_text(user_message)],
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

        return response.text

    except Exception as e:
        print(f"An error occurred: {e}")
        return str(e)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))