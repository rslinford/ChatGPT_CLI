import openai
import re

with open("api_key.txt", "r") as file:
    openai.api_key = file.read().strip()

stop_command = "STOP"
clear_command = "CLEAR"
line_wrap_pos = 100
model_id = "gpt-3.5-turbo"
max_tokens = 1000
temperature = 1
messages = [
    # {"role": "system", "content": "You are a helpful assistant."}
    {"role": "system", "content": "You are a nerdy assistant who replies in technical detail."}
    # {"role": "system", "content": "You are a snarky assistant."}
    # {"role": "system", "content": "You are a funny assistant who replies with a sense of humour."}
    # {"role": "system", "content": "You are a poetic assistant who replies in rhyme."}
    # {"role": "system", "content": "You are a poetic assistant who paints with words."}
]


def wrap_print_line(line):
    if len(line) > line_wrap_pos:
        n = 0
        for c in line:
            if n > line_wrap_pos and c == ' ':
                print()
                n = 0
            if c == ' ' and n == 0:
                continue
            print(c, end='')
            n += 1
        print()
    else:
        print(line)


def wrap_print_paragraph(content):
    for line in content.split('\n'):
        wrap_print_line(line)


while True:
    user_input = input(f"{len(messages)}> ").strip()
    if user_input == stop_command:
        break
    if user_input == clear_command:
        while len(messages) > 1:
            messages.pop(-1)
        continue
    if user_input == '':
        continue

    # Matches pattern: param_name = value
    # For example: temperature = 0.7
    result = re.search(r'^(\w+)\s*=\s*(\S+)$', user_input)
    if result:
        name = result.group(1)
        value = result.group(2)
        if name == 'temperature':
            try:
                temperature = float(value)
                print(f'Set <temperature({temperature})>')
            except ValueError:
                print(f'Invalid temperature({value})')
        else:
            print(f'Unknown parameter "{name}"')
        continue

    # Send user's prompt to openai
    messages.append({"role": "user", "content": user_input})
    try:
        response = openai.ChatCompletion.create(
            model=model_id,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens)
        content = response['choices'][0]['message']['content']
        finish_reason = response['choices'][0]['finish_reason']
        messages.append({"role": "assistant", "content": content})
        print(f'<temperature({temperature})>')
        wrap_print_paragraph(content)
        if finish_reason != 'stop':
            print(f'<{finish_reason}({max_tokens})>')
    except openai.error.InvalidRequestError as e:
        print(f'Error({model_id}): {e}')
