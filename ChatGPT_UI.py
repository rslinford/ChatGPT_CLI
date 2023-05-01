import tkinter as tk
import openai

openai.api_key = "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"
openai_model = "text-davinci-002"


class MyGUI:
    def __init__(self, master):
        self.master = master
        master.title("ChatGPT")

        # create the input and output text fields
        self.input_text = tk.Entry(master)
        self.input_text.bind("<Return>", self.on_enter)
        self.output_text = tk.Text(master, height=10, state='disabled')

        # create the submit button
        self.submit_button = tk.Button(master, text='Submit', command=self.on_submit)

        # create the vertical grid layout to arrange the widgets
        self.grid_layout = tk.Grid()

        # add the widgets to the grid layout
        self.input_label = tk.Label(master, text='Input:')
        self.input_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.input_text.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.output_label = tk.Label(master, text='Output:')
        self.output_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.output_text.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

        self.submit_button.grid(row=2, column=1, padx=5, pady=5, sticky='e')

    def on_enter(self, event):
        if event.widget == self.input_text:
            self.on_submit()

    def on_submit(self):
        input_text = self.input_text.get()
        response = openai.Completion.create(
            engine=openai_model,
            prompt=input_text,
            max_tokens=1024 * 4 - 1,
            n=1,
            stop=None,
            temperature=0.5,
        )

        output_text = response.choices[0].text

        # update the output text field
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', 'end')
        self.output_text.insert('1.0', output_text)
        self.output_text.config(state='disabled')


if __name__ == '__main__':
    root = tk.Tk()
    my_gui = MyGUI(root)
    root.mainloop()
