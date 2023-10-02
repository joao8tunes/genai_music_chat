#!/usr/bin/env python
# encoding: utf-8

# João Antunes <joao8tunes@gmail.com>
# https://github.com/joao8tunes

from datetime import datetime
import logging

from genai_chat.openai import BotOpenAI, BotOpenAIFC
from genai_chat.settings import setup_logger
from genai_chat.palm import BotPaLM

setup_logger(__name__)


def main() -> None:
    bots = {
        "OpenAI FC": BotOpenAIFC(),
        "OpenAI": BotOpenAI(),
        "PaLM": BotPaLM()
    }

    logging.info("Chat initialized...")

    while True:
        user_message = input()

        if user_message in ("tks", "thanks", "bye", "obrigado", "tchau", "valeu", "vlw", "flw"):
            break

        results = {}

        for name, bot in bots.items():
            logging.info(name)
            start_time = datetime.now()
            bot_message, bot_citations = bot.chat(user_message=user_message)
            bot_exec_time = datetime.now() - start_time

            results[name] = {
                "bot_message": bot_message,
                "bot_citations": bot_citations,
                "bot_exec_time": bot_exec_time
            }

        results_to_print = []

        for name, data in results.items():
            results_to_print.append(
                f"\n{name}:\n"
                f"\t- Message: {data['bot_message']}\n"
                f"\t- Citations: {len(data['bot_citations'])}, {data['bot_citations']}\n"
                f"\t- Exec Time: {data['bot_exec_time']}\n"
            )

        print("\n----------------------\n".join(results_to_print))


if __name__ == '__main__':
    main()
