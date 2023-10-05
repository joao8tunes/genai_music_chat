#!/usr/bin/env python
# encoding: utf-8

# João Antunes <joao8tunes@gmail.com>
# https://github.com/joao8tunes

"""
OpenAI GenAI operations.
"""

from openai.api_resources.abstract.engine_api_resource import EngineAPIResource
import openai

from typing import Callable, Any
import functools
import logging
import json

from genai_chat.settings import get_settings
from genai_chat.utils import merge_dict
from genai_chat.core import Bot


class FunctionCallingProperty(json.JSONEncoder):
    """Function calling property."""

    name: str
    """Property name."""
    descr_or_enum: Any
    """Description or enumerate property."""
    required: bool
    """Whether it's a required property."""

    def __init__(self, name: str, descr_or_enum: Any, required: bool = False):
        """
        Instantiates a function calling property object.

        Parameters
        ----------
        name: str
            Function calling property name.
        descr_or_enum: Any
            Description or enumerate property.
        required: bool
            Whether it's a required property.

        References
        ----------
        .. [1] Function calling: https://platform.openai.com/docs/guides/gpt/function-calling
        """
        super().__init__()

        self.name = name
        self.descr_or_enum = descr_or_enum
        self.required = required

    def __json__(self) -> dict:
        """
        Handle a JSON object.

        Returns
        -------
        json_output: dict
            Dictionary.
        """
        if isinstance(self.descr_or_enum, list):
            json_output = {
                self.name: {
                    'type': "string",
                    'enum': self.descr_or_enum
                }
            }
        else:
            json_output = {
                self.name: {
                    'type': "string",
                    'description': self.descr_or_enum
                }
            }

        return json_output


class FunctionCalling:
    """Function calling."""

    name: str
    """Function name."""
    description: str
    """Function description."""
    parameters: list
    """Function parameters."""
    function_callable: Callable
    """Function callable."""
    kwargs: dict
    """Keyword-based arguments."""

    def __init__(
            self,
            name: str,
            description: str,
            parameters: list = None,
            function_callable: Callable = None,
            kwargs: dict = None
    ):
        """
        Instantiates a function calling object.

        Parameters
        ----------
        name: str
            Function name.
        description: str
            Function description.
        parameters: list
            Function parameters.
        function_callable: Callable
            Function callable.
        **kwargs: dict
            Keyword-based arguments.

        References
        ----------
        .. [1] Function calling: https://platform.openai.com/docs/guides/gpt/function-calling
        """
        self.name = name
        self.description = description
        self.parameters = parameters if parameters is not None else []
        self.function_callable = function_callable
        self.kwargs = kwargs if kwargs else {}

    def params(self) -> [str]:
        """
        Get keyword-based parameters from `parameters` attribute.

        Returns
        -------
        arg_keys: [str]
            List of keyword-based parameters names.
        """
        arg_keys = [p.name for p in self.parameters]

        return arg_keys

    def __call__(self, **kwargs) -> Callable:
        """
        Call the function callable object using keyword-based parameters.

        Parameters
        ----------
        **kwargs: dict
            Keyword-based arguments to call function calling caller.

        Returns
        -------
        function_call: Callable
            Function call's call.
        """
        function_call = self.function_callable(**kwargs)

        return function_call

    def __json__(self) -> dict:
        """
        Handle a JSON object.

        Returns
        -------
        json_output: dict
            Dictionary.
        """
        json_output = {
            'name': self.name,
            'description': self.description,
            'parameters': {
                'type': "object",
                'properties': functools.reduce(merge_dict, self.parameters),
                'required': [x.name for x in self.parameters if x.required]
            }
        }

        return json_output


class BotOpenAI(Bot):
    """
    OpenAI GenAI bot.
    """

    _api_type: str
    """OpenAI API type: 'azure' or 'open_ai'."""
    _api_key: str
    """OpenAI API key."""
    _api_base: str
    """OpenAI API endpoint."""
    _api_version: str
    """OpenAI API version."""
    _deployment_id: str
    """OpenAI API deployment ID, only required for 'azure' API type."""
    _llm_name: str
    """LLM model name."""
    _temperature_llm: float
    """LLM model temperature: [0, 2]."""
    _temperature_functions: float
    """LLM model temperature: [0, 2]."""
    _prompt_functions: str
    """Prompt to identify user-reported search needs and attributes."""
    _openai_messages: [dict]
    """List of OpenAI messages from chat."""
    _openai_kwargs: dict
    """OpenAI API keyword-based arguments."""
    _openai_functions: [dict]
    """OpenAI keyword-based function calls, only required for 'BotOpenAIFC' class."""

    def __init__(self):
        """
        Instantiates an OpenAI GenAI bot object.

        References
        ----------
        .. [1] OpenAI API Reference: https://platform.openai.com/docs/api-reference

        .. [2] OpenAI Python Library: https://github.com/openai/openai-python
        """
        super().__init__()

        self._genai_name = "OpenAI"
        openai_settings = get_settings().get('openai')
        self._api_type = openai_settings.get('api_type', "open_ai")
        self._api_key = openai_settings.get('api_key')
        self._api_base = openai_settings.get('api_base', "https://api.openai.com/v1/")
        self._api_version = openai_settings.get('api_version', "2023-07-01-preview")
        self._deployment_id = openai_settings.get('deployment_id')
        self._llm_name = openai_settings.get('llm_name', "gpt-35-turbo")
        self._temperature_llm = openai_settings.get('temperature_llm', 0.5)
        self._temperature_functions = openai_settings.get('temperature_functions', 0.5)
        self._openai_functions = []

        # Setting up the OpenAI environment:
        openai.api_type = self._api_type
        openai.api_key = self._api_key
        openai.api_base = self._api_base
        openai.api_version = self._api_version

        self._openai_kwargs = {'deployment_id': self._deployment_id} if openai.api_type == "azure" else {}
        self._openai_messages = [{"role": "system", "content": self._prompt_behavior}]

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

    def _get_llm_response(self, messages: [dict], temperature: float, **kwargs) -> EngineAPIResource:
        """
        Sends a request with a message to the OpenAI API service.

        Parameters
        ----------
        messages: [dict]
            List of messages.
        temperature: float
            LLM temperature.
        **kwargs: dict
            Keyword-based arguments.

        Returns
        -------
        response: EngineAPIResource
            Chat response from OpenAI API service.
        """
        kwargs = merge_dict(kwargs, self._openai_kwargs)
        response = openai.ChatCompletion.create(
            model=self._llm_name,
            temperature=temperature,
            messages=messages,
            **kwargs
        )

        return response

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
        logging.debug(f"[{self._genai_name}] User message: {user_message}")
        logging.debug(f"[{self._genai_name}] Generating LLM bot response...")

        user_message = user_message.replace('\'', "\"")
        bot_message, bot_citations = "", []

        try:
            # Identifying user-reported search needs and attributes:
            prompt = self._prompt_functions + f"\nUser message: {user_message}"
            messages = [{"role": "system", "content": prompt}]
            response = self._get_llm_response(temperature=self._temperature_functions, messages=messages)
            bot_message = response.choices[0].message.content
            bot_message = " ".join(bot_message.replace("\n", " ").split())

            try:
                logging.debug(f"[{self._genai_name}] User preferences: {bot_message}")
                search_params = json.loads(bot_message)
                music_recommendations = self.get_music_recommendations(**search_params)
                self._citations_available = music_recommendations if music_recommendations else []
            except Exception as e:
                logging.warning(f"[{self._genai_name}] Failed to fetch data via simple search: {e}")
                pass

            if self._citations_available:
                # Workaround to couple LLM with external data without the need to retrain the model:
                logging.debug(f"[{self._genai_name}] Injecting external data into LLM...")
                citations_available_str = ";\n\n".join([json.dumps(citation) for citation in self._citations_available])
                user_message_prompt = f"""
                    User message:
                    '{user_message}'

                    Available options:
                    {citations_available_str}
                    """

                self._openai_messages.append({"role": "user", "content": user_message_prompt})
                response = self._get_llm_response(temperature=self._temperature_llm, messages=self._openai_messages)

                bot_message = response.choices[0].message.content
                bot_citations = self._extract_citations(bot_message=bot_message)
            else:
                self._openai_messages.append({"role": "user", "content": user_message})
                response = self._get_llm_response(temperature=self._temperature_llm, messages=self._openai_messages)
                bot_message = response.choices[0].message.content
        except Exception as e:
            bot_message = self._error_message_general
            logging.error(f"[{self._genai_name}] {e}")
            pass

        # Handling with empty citations:
        if self._filter_bot_messages_without_citations and "\"" in bot_message and not bot_citations:
            logging.warning(
                f"[{self._genai_name}] No citation found on bot message: '{bot_message}'. "
                f"Raising default error message."
            )

            bot_message = self._error_message_bot_message_without_citations

        self._openai_messages.append({"role": "assistant", "content": bot_message})
        bot_message = " ".join(bot_message.replace("\n", " ").split())

        self._add_user_message(user_message=user_message)
        self._add_assistant_message(assistant_message=bot_message, assistant_citations=bot_citations)

        logging.debug(f"[{self._genai_name}] Bot message: {bot_message}")
        logging.debug(f"[{self._genai_name}] Bot citations: {bot_citations}")

        return bot_message, bot_citations


class BotOpenAIFC(BotOpenAI):
    """
    OpenAI GenAI bot (using function calling feature).
    """

    _functions: dict
    """Function calls available in OpenAI."""
    _openai_functions: [dict]
    """OpenAI keyword-based function calls."""

    def __init__(self):
        """
        Instantiates an OpenAI GenAI bot object (with function calling feature).

        References
        ----------
        .. [1] OpenAI API Reference: https://platform.openai.com/docs/api-reference

        .. [2] OpenAI Python Library: https://github.com/openai/openai-python

        .. [3] Function calling: https://platform.openai.com/docs/guides/gpt/function-calling

        .. [4] OpenAI models: https://stackoverflow.com/a/75397187/16109419
        """
        super().__init__()

        self._genai_name = "OpenAI FC"
        openai_settings = get_settings().get('openai')
        self._llm_name = openai_settings.get('llm_fc_name', "gpt-35-turbo-16k")
        self._openai_functions = []

        self._functions = {
            "get_music_recommendations": FunctionCalling(
                name="get_music_recommendations",
                description="""
                    Get music recommendations based on the following information provided by the user: 
                    title, genre, authors, country, and/or year.
                """,
                parameters=[
                    FunctionCallingProperty("title", "Music title"),
                    FunctionCallingProperty("genre", "Music genre"),
                    FunctionCallingProperty("authors", "Music authors"),
                    FunctionCallingProperty("country", "Music country"),
                    FunctionCallingProperty("year", "Music year")
                ],
                function_callable=self.get_music_recommendations
            ),
        }

        for key, value in self._functions.items():
            self._openai_functions.append(value.__json__())  # Converting objects to JSON dictionary.

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
        logging.debug(f"[{self._genai_name}] User message: {user_message}")
        logging.debug(f"[{self._genai_name}] Generating LLM bot response...")

        user_message = user_message.replace('\'', "\"")
        self._openai_messages.append({"role": "user", "content": user_message})
        function_call = kwargs.get('function_call', "auto")
        bot_message, bot_citations = "", []

        try:
            # Processing user input message and searching for `function_calling` actions:
            openai_kwargs = {"functions": self._openai_functions}
            response = self._get_llm_response(
                temperature=self._temperature_functions,
                messages=self._openai_messages,
                **openai_kwargs
            )

            response_message = response.choices[0].message
            function_call_obj = response_message.get('function_call')

            # Handling with `function_calling` actions:
            if self._openai_functions is not None and function_call == "auto" and function_call_obj:
                function_name = function_call_obj.get('name')
                function_args = json.loads(function_call_obj.get('arguments'))
                function_caller = self._functions.get(function_name)
                function_kwargs = {k: function_args.get(k) for k in function_caller.params()}

                logging.debug(f"[{self._genai_name}] User preferences: {function_kwargs}")
                function_response = function_caller(**function_kwargs)
                self._citations_available = function_response
                function_content = json.dumps(function_response)

                # Coupling LLM with external data without the need to retrain the model:
                logging.debug(f"[{self._genai_name}] Injecting external data into LLM...")
                self._openai_messages.append({"role": "function", "name": function_name, "content": function_content})

                response = self._get_llm_response(temperature=self._temperature_llm, messages=self._openai_messages)
                bot_message = response.choices[0].message.content
            else:
                # No `function_calling` actions detected:
                response = self._get_llm_response(temperature=self._temperature_llm, messages=self._openai_messages)
                bot_message = response.choices[0].message.content

            bot_citations = self._extract_citations(bot_message=bot_message)
        except Exception as e:
            bot_message = self._error_message_general
            logging.error(f"[{self._genai_name}] {e}")
            pass

        # Handling with empty citations:
        if self._filter_bot_messages_without_citations and "\"" in bot_message and not bot_citations:
            logging.warning(
                f"[{self._genai_name}] No citation found on bot message: '{bot_message}'. "
                f"Raising default error message."
            )

            bot_message = self._error_message_bot_message_without_citations

        self._openai_messages.append({"role": "assistant", "content": bot_message})
        bot_message = " ".join(bot_message.replace("\n", " ").split())

        self._add_user_message(user_message=user_message)
        self._add_assistant_message(assistant_message=bot_message, assistant_citations=bot_citations)

        logging.debug(f"[{self._genai_name}] Bot message: {bot_message}")
        logging.debug(f"[{self._genai_name}] Bot citations: {bot_citations}")

        return bot_message, bot_citations
