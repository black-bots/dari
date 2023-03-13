# -*- coding:utf-8 -*-

title = """<h1 align="center">▪◾◼⬛BlackBots ChatGPT⬛◼◾▪"""
description = """<div align=center>

Developed by © Cloud Bots™ BlackBots [Supreme100](https://instagram.com/erikrai.art)

Visit Black Botss [Webstore](https://black-bots.github.io) to download other useful tools.

This app uses `gpt-3.5-turbo` large language model
</div>
"""
customCSS = """
code {
     display: inline;
     white-space: break-spaces;
     border-radius: 6px;
     margin: 0 2px 0 2px;
     padding: .2em .4em .1em .4em;
     background-color: rgba(0.7,0.8,0.5,0.2);
}
pre code {
     display: block;
     white-space: pre;
     background-color: hsla(0, 0%, 0%, 72%);
     border: solid 5px var(--color-border-primary) !important;
     border-radius: 10px;
     padding: 0 1.2rem 1.2rem;
     margin-top: 1em !important;
     color: rgba(0.7,0.8,0.5,0.2);
     box-shadow: inset 0px 8px 16px hsla(0, 0%, 0%, .2)
}
"""

standard_error_msg = "☹️An error occurred:" # Standard prefix for error messages
error_retrieve_prompt = "The connection timed out, unable to retrieve the conversation. Please check the network connection, or whether the API-Key is valid." # An error occurred while retrieving the conversation
summarize_prompt = "Please summarize the above conversation, no more than 100 words." # The prompt when summarizing the conversation
max_token_streaming = 3500 # Maximum number of tokens for streaming conversations
timeout_streaming = 5 # Timeout for streaming conversations
max_token_all = 3500 # Maximum number of tokens for non-streaming conversations
timeout_all = 200 # Timeout for non-streaming conversations
enable_streaming_option = True # Whether to enable the check box to choose whether to display the answer in real time
HIDE_MY_KEY = False # Set this value to True if you want to hide your API key in UI