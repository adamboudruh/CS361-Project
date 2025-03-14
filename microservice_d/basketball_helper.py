from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

@app.route('/help', methods=['POST'])
def get_player_data():
    # access question from body of http request
    data = request.get_json()
    question = data.get('question', '')
    print(question)
    
    # make ai helper, give params "you are an enthusiastic basketball ai helper. YOur job is to explain the rules of basketball. If the question does not relate to the sport of basketball, please respond with 'I apologize, I don't know anything about that, but I can help with any basketball related questions you might have!'"
    prompt = (
        "You are an enthusiastic basketball AI helper. Your job is to explain the rules of basketball and answer basketball related questions. "
        "If the question does not relate to the sport of basketball, please respond with 'I apologize, I don't know anything about that, but I can help with any basketball-related questions you might have!' Please keep it under 150 words"
    )
    
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = "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"
    )
    
    completion = client.chat.completions.create(
        model="meta/llama-3.3-70b-instruct",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ],
    )
    print(completion)
    
    answer = completion.choices[0].message.content
    print(answer)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True, port=3003)