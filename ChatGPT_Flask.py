from flask import Flask, render_template, request
import openai


# Initialize the Flask application
app = Flask(__name__)

# Configure OpenAI API key
with open("api_key.txt", "r") as file:
    openai.api_key = file.read().strip()

# Define the home page
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def home_post():
    user_prompt = request.form['user_prompt']
    system_message = request.form['system_message']
    temperature = request.form['temperature']

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt}
    ]

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages,
        temperature = float(temperature),
        max_tokens = 1024)

    assistant_response = response['choices'][0]['message']['content']
    finish_reason = response['choices'][0]['finish_reason']
    # todo: store messages in session
    messages.append({"role": "assistant", "content": assistant_response})

    # Render the response template with the assistant response
    return render_template('home.html',
                           user_prompt=user_prompt,
                           system_message=system_message,
                           assistant_response=assistant_response,
                           finish_reason=finish_reason,
                           temperature=temperature)


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
