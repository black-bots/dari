#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gradio as gr
import os
import sys
import argparse
from utils import *
from presets import *
import webbrowser

#
my_api_key = "" # enter your API key here

#if we are running in Docker
if os.environ.get('dockerrun') == 'yes':
     dockerflag=True
else:
     dockerflag = False

authflag = False

if dockerflag:
     my_api_key = os.environ.get('my_api_key')
     if my_api_key == "empty":
         print("Please give an api key!")
         sys. exit(1)
     #auth
     username = os.environ.get('USERNAME')
     password = os.environ.get('PASSWORD')
     if not (isinstance(username, type(None)) or isinstance(password, type(None))):
         authflag = True
else:
     if not my_api_key and os.path.exists("api_key.txt") and os.path.getsize("api_key.txt"):
         with open("api_key.txt", "r") as f:
             my_api_key = f.read().strip()
     if os.path.exists("auth.json"):
         with open("auth.json", "r") as f:
             auth = json. load(f)
             username = auth["username"]
             password = auth["password"]
             if username != "" and password != "":
                 authflag = True

gr.Chatbot.postprocess = postprocess

with gr.Blocks(css=customCSS) as demo:
    gr.HTML(title)
    with gr.Row():
        with gr.Column(scale=4):
            keyTxt = gr.Textbox(show_label=False, placeholder=f"Enter your OpenAI API-key here...",value=my_api_key, type="password", visible=not HIDE_MY_KEY).style(container=True)
        with gr.Column(scale=1):
            use_streaming_checkbox = gr.Checkbox(label="Real-time streaming answer", value=True, visible=enable_streaming_option)
    chatbot = gr.Chatbot() # .style(color_map=("#1D51EE", "#585A5B"))
    history = gr.State([])
    token_count = gr.State([])
    promptTemplates = gr.State(load_template(get_template_names(plain=True)[0], mode=2))
    TRUECOMSTANT = gr.State(True)
    FALSECONSTANT = gr.State(False)
    topic = gr.State("Untitled conversation history")

    with gr.Row():
        with gr.Column(scale=12):
            user_input = gr.Textbox(show_label=False, placeholder="enter here").style(
                container=False)
        with gr.Column(min_width=50, scale=1):
            submitBtn = gr.Button("🚀", variant="primary")
    with gr.Row():
        emptyBtn = gr.Button("🧹 new conversation")
        retryBtn = gr.Button("🔄 Regenerate")
        delLastBtn = gr.Button("🗑️ Delete the last conversation")
        reduceTokenBtn = gr.Button("♻️ Summarize the conversation")
    status_display = gr.Markdown("status: ready")
    systemPromptTxt = gr.Textbox(show_label=True, placeholder=f"Enter System Prompt here...",
                                label="System prompt", value=initial_prompt). style(container=True)
    with gr.Accordion(label="Load Prompt Template", open=False):
        with gr.Column():
            with gr.Row():
                with gr.Column(scale=6):
                    templateFileSelectDropdown = gr.Dropdown(label="Select Prompt template collection file", choices=get_template_names(plain=True), multiselect=False, value=get_template_names(plain=True)[0])
                with gr.Column(scale=1):
                    templateRefreshBtn = gr.Button("🔄 Refresh")
                    templaeFileReadBtn = gr.Button("📂 read template")
            with gr.Row():
                with gr.Column(scale=6):
                    templateSelectDropdown = gr.Dropdown(label="load from Prompt template", choices=load_template(get_template_names(plain=True)[0], mode=1), multiselect=False, value=load_template(get_template_names(plain=True)[ 0], mode=1)[0])
                with gr.Column(scale=1):
                    templateApplyBtn = gr.Button("⬇️ Apply")
    with gr.Accordion(label="Save/Load conversation history", open=False):
        with gr.Column():
            with gr.Row():
                with gr.Column(scale=6):
                    saveFileName = gr.Textbox(
                        show_label=True, placeholder=f"Enter the saved file name here...", label="Set the saved file name", value="Conversation History").style(container=True)
                with gr.Column(scale=1):
                    saveHistoryBtn = gr.Button("💾 Save conversation")
            with gr.Row():
                with gr.Column(scale=6):
                    historyFileSelectDropdown = gr.Dropdown(label="Load conversation from list", choices=get_history_names(plain=True), multiselect=False, value=get_history_names(plain=True)[0])
                with gr.Column(scale=1):
                    historyRefreshBtn = gr.Button("🔄 Refresh")
                    historyReadBtn = gr.Button("📂 Read conversation")
    #inputs, top_p, temperature, top_k, repetition_penalty
    with gr.Accordion("parameter", open=False):
        top_p = gr.Slider(minimum=-0, maximum=1.0, value=1.0, step=0.05,
                        interactive=True, label="Top-p (nucleus sampling)",)
        temperature = gr.Slider(minimum=-0, maximum=5.0, value=1.0,
                                step=0.1, interactive=True, label="Temperature",)
        #top_k = gr.Slider( minimum=1, maximum=50, value=4, step=1, interactive=True, label="Top-k",)
        #repetition_penalty = gr.Slider( minimum=0.1, maximum=3.0, value=1.03, step=0.01, interactive=True, label="Repetition Penalty", )
    gr.Markdown(description)


    user_input.submit(predict, [keyTxt, systemPromptTxt, history, user_input, chatbot, token_count, top_p, temperature, use_streaming_checkbox], [chatbot, history, status_display, token_count], show_progress=True)
    user_input. submit(reset_textbox, [], [user_input])

    submitBtn.click(predict, [keyTxt, systemPromptTxt, history, user_input, chatbot, token_count, top_p, temperature, use_streaming_checkbox], [chatbot, history, status_display, token_count], show_progress=True)
    submitBtn. click(reset_textbox, [], [user_input])

    emptyBtn.click(reset_state, outputs=[chatbot, history, token_count, status_display], show_progress=True)

    retryBtn.click(retry, [keyTxt, systemPromptTxt, history, chatbot, token_count, top_p, temperature, use_streaming_checkbox], [chatbot, history, status_display, token_count], show_progress=True)

    delLastBtn.click(delete_last_conversation, [chatbot, history, token_count, use_streaming_checkbox], [
                    chatbot, history, token_count, status_display], show_progress=True)

    reduceTokenBtn.click(reduce_token_size, [keyTxt, systemPromptTxt, history, chatbot, token_count, top_p, temperature, use_streaming_checkbox], [chatbot, history, status_display, token_count], show_progress=True)

    saveHistoryBtn. click(save_chat_history, [
                saveFileName, systemPromptTxt, history, chatbot], None, show_progress=True)

    saveHistoryBtn.click(get_history_names, None, [historyFileSelectDropdown])

    historyRefreshBtn.click(get_history_names, None, [historyFileSelectDropdown])

    historyReadBtn.click(load_chat_history, [historyFileSelectDropdown, systemPromptTxt, history, chatbot], [saveFileName, systemPromptTxt, history, chatbot], show_progress=True)

    templateRefreshBtn.click(get_template_names, None, [templateFileSelectDropdown])

    templaeFileReadBtn.click(load_template, [templateFileSelectDropdown], [promptTemplates, templateSelectDropdown], show_progress=True)

    templateApplyBtn.click(get_template_content, [promptTemplates, templateSelectDropdown, systemPromptTxt], [systemPromptTxt], show_progress=True)

print(colorama.Back.GREEN + "\Black Bots's warm reminder: visit http://localhost:7860 to view the interface" + colorama.Style.RESET_ALL)
# The local server is enabled by default, it can be accessed directly from the IP by default, and the public sharing link is not created by default
demo.title = "BlackBots ChatGPT 🚀"

if __name__ == "__main__":
     webbrowser.open('http://localhost:7860', new = 2)
     if dockerflag:
         if authflag:
             demo.queue().launch(server_name="0.0.0.0", server_port=7860,auth=(username, password))
         else:
             demo.queue().launch(server_name="0.0.0.0", server_port=7860, share=False)
     #if not running in Docker
     else:
         if authflag:
             demo.queue().launch(share=False, auth=(username, password))
         else:
             demo.queue().launch(share=False) # Change to share=True to create a public sharing link
         #demo.queue().launch(server_name="0.0.0.0", server_port=7860, share=False) # Customizable port
         #demo.queue().launch(server_name="0.0.0.0", server_port=7860,auth=("fill in the username here", "fill in the password here")) # Username and password can be set
         #demo.queue().launch(auth=("Fill in the username here", "Fill in the password here")) # Suitable for Nginx reverse proxy

