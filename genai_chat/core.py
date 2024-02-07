#!/usr/bin/env python
# encoding: utf-8

# João Antunes <joao8tunes@gmail.com>
# https://github.com/joao8tunes

"""
Core GenAI operations.
"""

import logging
import json
import re
import os

from genai_chat.utils import compare_strings
from genai_chat.settings import get_settings


class Bot:
    """
    Abstract GenAI bot.
    """

    _genai_name: str
    """Generative AI technology name."""
    _prompt_behavior: str
    """Bot behavior: initial prompt."""
    _prompt_function_music_recommendations: str
    """Prompt to identify user-reported search needs and attributes for music recommendations."""
    _citation_regex: str
    """Regex used to fetch citations from bot message."""
    _citation_threshold: float
    """Threshold for fuzzy citation search, between 0 and 1."""
    _citation_field: str
    """Field used to index citations."""
    _citations_available: [dict]
    """List of external data."""
    _database_filepath: str
    """Database filepath with external data."""
    _filter_bot_messages_without_citations: bool
    """Whether to filter bot messages with no citations."""
    _error_message_bot_message_without_citations: str
    """Default message shown when bot messages has no citations."""
    _error_message_general: str
    """Default error message."""
    _chat_history: [dict]
    """Chat history."""

    def __init__(self):
        """
        Instantiates an abstract GenAI bot object.
        """
        genai_settings = get_settings().get('genai_chat')

        self._prompt_behavior = genai_settings.get('prompt_behavior', "")
        self._prompt_function_music_recommendations = genai_settings.get('prompt_function_music_recommendations', "")
        self._citation_regex = genai_settings.get('citation_regex', r'"([^"]*)"')
        self._citation_threshold = genai_settings.get('citation_threshold', 0.75)
        self._citation_field = genai_settings.get('citation_field', "title")
        self._citations_available = []
        self._chat_history = []

        database_filepath_rel = genai_settings.get('database_filepath', "assets/database.json")
        this_dir_path = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir))
        self._database_filepath = os.path.join(*[this_dir_path, "..", database_filepath_rel])

        self._filter_bot_messages_without_citations = \
            genai_settings.get('filter_bot_messages_without_citations', True)
        self._error_message_bot_message_without_citations = \
            genai_settings.get('error_message_bot_message_without_citations', "")
        self._error_message_general = genai_settings.get('error_message_general', "")

    @property
    def genai_name(self) -> str:
        """
        Get the Generative AI technology name.

        Returns
        -------
        _genai_name: str
            Generative AI technology name.
        """
        return self._genai_name

    def _load_database(self) -> [dict]:
        """
        Load a database from a JSON file.

        Returns
        -------
        data: [dict]
            Database.
        """
        with open(self._database_filepath, mode="rt", encoding="utf-8") as file:
            data = json.load(file)

        return data

    def _extract_citations(self, bot_message: str) -> [dict]:
        """
        Extracts the citations contained in the LLM bot message using fuzzy string match.

        Parameters
        ----------
        bot_message: str
            Message from LLM bot.

        Returns
        -------
        citations_list: [dict]
            List of citations.
        """
        logging.debug("Extracting citations from message...")
        selected_citations = {}
        citations = self._citations_available.copy()

        if citations:
            # Extracting citations using regex and fuzzy string matching:
            names_list = re.findall(pattern=self._citation_regex, string=bot_message)

            if names_list:
                for name in names_list:
                    max_similarity = 0.0
                    ref, ref_index = None, None

                    for data_index, data in enumerate(citations, start=0):
                        similarity = compare_strings(name, data[self._citation_field], case_sensitive=False)

                        if similarity > max_similarity:
                            max_similarity = similarity
                            ref, ref_index = data, data_index

                    if max_similarity >= self._citation_threshold:
                        selected_citations[ref_index] = ref

            # Extracting citations using only fuzzy string matching:
            for data_index, data in enumerate(citations, start=0):
                if data_index not in selected_citations:
                    similarity = compare_strings(
                        data[self._citation_field],
                        bot_message,
                        fuzzy_method="partial_ratio",
                        case_sensitive=False
                    )

                    if similarity >= self._citation_threshold:
                        selected_citations[data_index] = data.copy()

        if selected_citations:
            citations, citations_ids = list(selected_citations.values()), list(selected_citations.keys())
            logging.debug(f"Selected citations: {citations_ids}")
        else:
            logging.warning("No citations found.")
            citations = []

        return citations

    def chat(self, user_message: str, **kwargs) -> (str, [dict]):
        """
        Abstract chat method: sends a user message and receives a bot response from a LLM.

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
        raise NotImplementedError()

    def _add_user_message(self, user_message: str) -> None:
        """
        Add user message to chat history.

        Parameters
        ----------
        user_message: str
            User message.
        """
        self._chat_history.append(
            {
                "author": "user",
                "message": user_message
            }
        )

    def _add_assistant_message(self, assistant_message: str, assistant_citations: [dict]) -> None:
        """
        Add assistant message to chat history.

        Parameters
        ----------
        assistant_message: str
            Assistant message.
        assistant_citations: [dict]
            Assistant citations.
        """
        self._chat_history.append(
            {
                "author": "assistant",
                "message": assistant_message,
                "citations": assistant_citations
            }
        )

    @property
    def chat_history(self) -> [dict]:
        """
        Get chat history.

        Returns
        -------
        _chat_history: [dict]
            Chat history.
        """
        return self._chat_history

    def get_music_recommendations(
            self,
            title: str = None,
            genre: str = None,
            authors: str = None,
            country: str = None,
            year: int = None
    ) -> [dict]:
        """
        Get music recommendations from database.

        Parameters
        ----------
        title: str
            Music title.
        genre: str
            Music genre.
        authors: str
            Music authors.
        country: str
            Music country.
        year: int
            Music year.

        Returns
        -------
        data: [dict]
            List of music recommendations.

        Notes
        -----
        This method allows for the incorporation of external data into the LLM without requiring model retraining. This
        integration is useful in refining the information considered by the LLM, leading to more personalized responses.
        Given that GenAI charges for LLM usage per token/word, it's prudent to limit the amount of external data
        injected into the LLM per request.

        It's recommended to adopt an approach that provides the user with the top N options based on identified
        parameters, rather than loading the entire database into the LLM. Additionally, you have the option to employ a
        custom recommendation engine or utilize a semantic search service like Azure Cognitive Search or GCP Cloud
        Search (also known as GCP Enterprise Search).
        """
        data = []

        try:
            logging.debug("Fetching data using simple search...")
            search_params = {"title": title, "genre": genre, "authors": authors, "country": country, "year": year}
            logging.debug(f"Search parameters: {search_params}")
            data = self._load_database()
            logging.debug(f"Fetched {len(data)} results.")
        except Exception as e:
            logging.warning(f"Failed to fetch data: {e}")
            pass

        return data
