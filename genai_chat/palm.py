#!/usr/bin/env python
# encoding: utf-8

# João Antunes <joao8tunes@gmail.com>
# https://github.com/joao8tunes

"""
PaLM GenAI operations.
"""

from vertexai.preview.language_models import ChatModel, TextGenerationModel
from vertexai.language_models._language_models import ChatSession
from vertexai.language_models import _language_models
from vertexai import init

import logging
import json

from genai_chat.settings import get_settings
from genai_chat.core import Bot


class BotPaLM(Bot):
    """
    PaLM GenAI bot.
    """

    _project_id: str
    """Google project ID."""
    _text_llm_name: str
    """LLM text model name."""
    _chat_llm_name: str
    """LLM chat model name."""
    _temperature_llm: float
    """LLM chat model temperature: [0, 1]."""
    _temperature_functions: float
    """LLM text model temperature: [0, 1]."""
    _prompt_functions: str
    """Prompt to identify user-reported search needs and attributes."""
    _text_llm: _language_models._LanguageModel
    """LLM text model object."""
    _chat_llm: _language_models._LanguageModel
    """LLM chat model object."""
    _chat_session: ChatSession
    """LLM chat model session."""

    def __init__(self):
        """
        Instantiates a PaLM GenAI bot object.

        References
        ----------
        .. [1] Migrate to PaLM API from Azure OpenAI: https://cloud.google.com/vertex-ai/docs/generative-ai/migrate-from-azure

        .. [2] Set up Application Default Credentials: https://cloud.google.com/docs/authentication/provide-credentials-adc

        .. [3] Locate the project ID: https://support.google.com/googleapi/answer/7014113?hl=en
        """
        super().__init__()

        palm_settings = get_settings().get('palm')
        self._project_id = palm_settings.get('project_id')
        self._text_llm_name = palm_settings.get('text_llm_name', "text-bison@001")
        self._chat_llm_name = palm_settings.get('chat_llm_name', "chat-bison@001")
        self._temperature_llm = palm_settings.get('temperature_llm', 0.5)
        self._temperature_functions = palm_settings.get('temperature_functions', 0.5)

        # Initializing the PaLM environment:
        init(project=self._project_id)

        # Initializing LLM:
        self._text_llm = TextGenerationModel.from_pretrained(model_name=self._text_llm_name)
        self._chat_llm = ChatModel.from_pretrained(model_name=self._chat_llm_name)
        self._chat_session = self._chat_llm.start_chat(context=self._prompt_behavior)

        # Approach to identify user-reported search needs and attributes:
        self._prompt_functions = """
            You are an excellent music consultant, capable of deeply understanding clients' preferences to provide 
            personalized recommendations. Identify if the user is requesting a music recommendation, and if so, return a 
            JSON containing the following attributes:
            
                - 'title': Music title;
                - 'genre': Music genre;
                - 'authors': Music authors;
                - 'country': Music country;
                - 'year': Music year.
            
            For attributes not identified in the user's message, you should use the value null in the JSON.
            If the user has not requested a music recommendation, do not return anything. 
            Do not invent information not provided by the user.
            """

    def chat(self, user_message: str, **kwargs) -> (str, [dict]):
        """
        Sends a user message and receives a bot response from a LLM.

        Parameters
        ----------
        user_message: str
            User message.
        **kwargs: dict
            Keyword-based arguments.

        Returns
        -------
        bot_message, bot_citations: (str, [dict])
            Bot message and list os citations.
        """
        # TODO: add chat context handling.
        logging.debug("Generating LLM bot response...")

        user_message = user_message.replace('\'', "\"")
        bot_message, bot_citations = "", []

        try:
            # Identifying user-reported search needs and attributes:
            prompt = self._prompt_functions + f"\nUser message: {user_message}"
            response = self._text_llm.predict(prompt=prompt, temperature=self._temperature_functions)
            bot_message = response.text
            bot_message = " ".join(bot_message.replace("\n", " ").split())
            bot_citations = []

            try:
                logging.debug(f"User preferences: {bot_message}")
                search_params = json.loads(bot_message)
                music_recommendations = self.get_music_recommendations(**search_params)
                self._citations_available = music_recommendations if music_recommendations else []
            except Exception as e:
                logging.warning(f"Failed to fetch data via simple search: {e}")
                pass

            if self._citations_available:
                # Workaround to couple LLM with external data without the need to retrain the model:
                logging.debug("Injecting external data into LLM...")
                citations_available_str = ";\n\n".join([json.dumps(citation) for citation in self._citations_available])
                user_message_prompt = f"""
                    User message:
                    '{user_message}'

                    Available options:
                    {citations_available_str}
                    """

                response = self._chat_session.send_message(
                    message=user_message_prompt,
                    temperature=self._temperature_llm
                )

                bot_message = response.text
                bot_citations = self._extract_citations(bot_message=bot_message)
            else:
                response = self._chat_session.send_message(message=user_message, temperature=self._temperature_llm)
                bot_message = response.text
        except Exception as e:
            bot_message = self._error_message_general
            logging.error(e)
            pass

        # Handling with empty citations:
        if self._filter_bot_messages_without_citations and "\"" in bot_message and not bot_citations:
            logging.warning(f"No citation found on bot message: '{bot_message}'. Raising default error message.")
            bot_message = self._error_message_bot_message_without_citations

        bot_message = " ".join(bot_message.replace("\n", " ").split())

        self._add_user_message(user_message=user_message)
        self._add_assistant_message(assistant_message=bot_message, assistant_citations=bot_citations)

        return bot_message, bot_citations
