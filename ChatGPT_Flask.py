from flask import Flask, render_template, request
import openai
import os

# Initialize the Flask application
app = Flask(__name__)

# Configure OpenAI API key
with open("api_key.txt", "r") as file:
    openai.api_key = file.read().strip()

# Define the home page
@app.route('/')
def home():
    return render_template('home.html')

# Define the response page
@app.route('/response', methods=['POST'])
def response():
    # Get the user prompt from the form
    user_prompt = request.form['user_prompt']

    # Get the system message from the form
    system_message = request.form['system_message']

    # Get the temperature from the form
    temperature = request.form['temperature']

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt}
    ]

    # Generate the assistant response using OpenAI API
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages,
        temperature = float(temperature),
        max_tokens = 1024)

    # Get the assistant response from the OpenAI API response
    assistant_response = response['choices'][0]['message']['content']
    finish_reason = response['choices'][0]['finish_reason']
    # todo: store messages in session
    messages.append({"role": "assistant", "content": assistant_response})

    # Render the response template with the assistant response
    return render_template('response.html',
                           user_prompt=user_prompt,
                           system_message=system_message,
                           assistant_response=assistant_response,
                           finish_reason=finish_reason,
                           temperature=temperature)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
