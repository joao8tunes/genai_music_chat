#!/usr/bin/env python
# encoding: utf-8

# João Antunes <joao8tunes@gmail.com>
# https://github.com/joao8tunes

from streamlit.runtime.uploaded_file_manager import UploadedFile
from datetime import datetime
from typing import Union
import streamlit as st
import pandas as pd
import logging
import json

from genai_chat.openai import BotOpenAI, BotOpenAIFC
from genai_chat.palm import BotPaLM
from genai_chat.settings import setup_logger
from genai_chat.utils import md5_hash

setup_logger(__name__)


def show_chat_sessions() -> None:
    """
    Show chat sessions on screen.
    """
    if "chats" in st.session_state:
        for chat in st.session_state['chats']:
            st.markdown(f"#### {chat['genai']} Chat #{chat['id']}")

            for message in chat['bot'].get_chat_history():
                avatar = "ℹ️" if message['author'] == "info" else None

                with st.chat_message(message['author'], avatar=avatar):
                    st.markdown(message['message'])

                    if "citations" in message:
                        for citation in message['citations']:
                            st.json(citation)


def simulate_chat_sessions() -> None:
    """
    Simulate chat sessions.
    """
    st.session_state['chats'] = []

    if "input_file" in st.session_state:
        df = load_chat_simulations_csv(st.session_state['input_file'])

        if df is None:
            del st.session_state['input_file']
            st.rerun()

            return

        for chat, data in df.groupby('user_id'):
            start_chat(restart_sessions=False)

            for user_text in data['user_message'].to_list():
                send_user_message(user_text)

            # Closing current chat:
            st.session_state['chats'][-1]['active'] = False


def send_user_message(user_message: str) -> None:
    """
    Send user message to the current chat.

    Parameters
    ----------
    user_message: str
        User message.
    """
    if user_message:
        st.session_state['chats'][-1]['bot'].chat(user_message=user_message)


def start_chat(restart_sessions: bool = True) -> None:
    """
    Start GenAI-based chat session.

    Parameters
    ----------
    restart_sessions: bool
        Whether to restart chat sessions.
    """
    genai_approach = st.session_state['genai_approach'] if "genai_approach" in st.session_state else ""

    if (restart_sessions and genai_approach) or "chats" not in st.session_state:
        logging.info("Restarting chats...")
        st.session_state['chats'] = []
    else:
        logging.info("Starting chat...")

    if genai_approach == "OpenAI FC":
        bot = BotOpenAIFC()
    elif genai_approach == "OpenAI":
        bot = BotOpenAI()
    elif genai_approach == "PaLM":
        bot = BotPaLM()
    else:
        bot = None

    if bot is not None:
        start_time = datetime.now()
        bot_id = md5_hash(start_time.strftime("%Y-%m-%d %H:%M:%S.%f"))
        chat = {"id": bot_id, "genai": genai_approach, "bot": bot, "active": True}
        st.session_state['chats'].append(chat)


def load_chat_simulations_csv(file: Union[str, UploadedFile], **kwargs) -> pd.DataFrame:
    """
    Load chat simulations from CSV file.

    Parameters
    ----------
    file: Union[str, UploadedFile]
        CSV file.
    **kwargs: dict
        Keyword-based arguments.

    Returns
    -------
    df: pd.DataFrame
        Pandas dataframe.
    """
    sep, encoding = kwargs.get('sep', ";"), kwargs.get('encoding', "UTF-8")
    df = None

    # Reading files from 'streamlit' UI:
    try:
        df = pd.read_csv(filepath_or_buffer=file, sep=sep, encoding=encoding, **kwargs).dropna()
    except Exception as e:
        logging.error(f"Failed to read CSV file: {e}")
        pass

    return df


def prepare_chat_sessions_to_download() -> [dict]:
    """
    Prepare chat sessions to download.

    Returns
    -------
    json_data: str
        JSON data.
    """
    data = []

    for chat in st.session_state['chats']:
        data.append({
            "id": chat['id'],
            "genai": chat['genai'],
            "messages": chat['bot'].get_chat_history(),
            "active": chat['active']
        })

    json_data = json.dumps(data)

    return json_data


def main():
    st.set_page_config(page_title="GenAI Music Chat")

    st.sidebar.write('**GENERATIVE AI**')

    st.sidebar.radio(
        label="Choose the GenAI approach used by chat",
        options=["OpenAI FC", "OpenAI", "PaLM"],
        captions=["Azure/OpenAI (function calling)", "Azure/OpenAI", "GCP Vertex AI PaLM"],
        key="genai_approach"
    )

    st.sidebar.markdown("""---""")

    st.sidebar.write('**CHAT**')

    chat_mode = st.sidebar.radio(
        label="Choose between normal chat or chat simulation",
        options=["Chat conversation", "Chat simulation"],
        captions=["Normal chat mode", "Load user messages from file"]
    )

    st.title("Chat History")

    if chat_mode == "Chat conversation":
        st.sidebar.button("Re-Start", help="Re-Start chat", type="primary", on_click=start_chat)

        if "chats" in st.session_state and st.session_state['chats'] and st.session_state["chats"][-1]['active']:
            user_message = st.chat_input("Send a message", key="enabled_chat_input")

            if user_message:
                send_user_message(user_message)
        else:
            st.chat_input("Send a message", key="disabled_chat_input", disabled=True)
    elif chat_mode == "Chat simulation":
        st.sidebar.file_uploader(
            "Chat simulation file",
            accept_multiple_files=False,
            type=("csv",),
            help="CSV file with user messages",
            on_change=simulate_chat_sessions,
            key="input_file"
        )

        st.sidebar.markdown("_Below is an example of a chat simulation file:_")
        st.sidebar.code(
            """
            user_id;user_message
            1;hello
            1;I would like some happy music
            1;nice, very good
            2; hi, how are you?
            2; do you like samba?
            2; recommend me a samba from Brazil
            """
        )

    show_chat_sessions()

    if "chats" in st.session_state:
        st.sidebar.download_button(
            label="Download",
            help="Download chat sessions",
            data=prepare_chat_sessions_to_download(),
            file_name="chat_sessions.json",
            mime="application/json",
        )


if __name__ == "__main__":
    main()
