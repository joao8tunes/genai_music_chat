URLS=[
"genai_chat/index.html",
"genai_chat/core.html",
"genai_chat/openai.html",
"genai_chat/palm.html",
"genai_chat/settings.html",
"genai_chat/utils.html"
];
INDEX=[
{
"ref":"genai_chat",
"url":0,
"doc":""
},
{
"ref":"genai_chat.core",
"url":1,
"doc":"Core GenAI operations."
},
{
"ref":"genai_chat.core.Bot",
"url":1,
"doc":"Abstract GenAI bot. Instantiates an abstract GenAI bot object."
},
{
"ref":"genai_chat.core.Bot.get_genai_name",
"url":1,
"doc":"Get the Generative AI technology name. Returns    - _genai_name: str Generative AI technology name.",
"func":1
},
{
"ref":"genai_chat.core.Bot.chat",
"url":1,
"doc":"Abstract chat method: sends a user message and receives a bot response from a LLM. Parameters      user_message: str User message.  kwargs: dict Keyword-based arguments. Returns    - bot_message, bot_citations: (str, [dict]) Bot message and list os citations.",
"func":1
},
{
"ref":"genai_chat.core.Bot.get_chat_history",
"url":1,
"doc":"Get chat history. Returns    - _chat_history: [dict] Chat history.",
"func":1
},
{
"ref":"genai_chat.core.Bot.get_music_recommendations",
"url":1,
"doc":"Get music recommendations from database. Parameters      title: str Music title. genre: str Music genre. authors: str Music authors. country: str Music country. year: int Music year. Returns    - data: [dict] List of music recommendations. Notes   - This method allows for the incorporation of external data into the LLM without requiring model retraining. This integration is useful in refining the information considered by the LLM, leading to more personalized responses. Given that GenAI charges for LLM usage per token/word, it's prudent to limit the amount of external data injected into the LLM per request. It's recommended to adopt an approach that provides the user with the top N options based on identified parameters, rather than loading the entire database into the LLM. Additionally, you have the option to employ a custom recommendation engine or utilize a semantic search service like Azure Cognitive Search or GCP Cloud Search (also known as GCP Enterprise Search).",
"func":1
},
{
"ref":"genai_chat.openai",
"url":2,
"doc":"OpenAI GenAI operations."
},
{
"ref":"genai_chat.openai.FunctionCallingProperty",
"url":2,
"doc":"Function calling property. Instantiates a function calling property object. Parameters      name: str Function calling property name. descr_or_enum: Any Description or enumerate property. required: bool Whether it's a required property. References       [1] Function calling: https: platform.openai.com/docs/guides/gpt/function-calling"
},
{
"ref":"genai_chat.openai.FunctionCallingProperty.name",
"url":2,
"doc":"Property name."
},
{
"ref":"genai_chat.openai.FunctionCallingProperty.descr_or_enum",
"url":2,
"doc":"Description or enumerate property."
},
{
"ref":"genai_chat.openai.FunctionCallingProperty.required",
"url":2,
"doc":"Whether it's a required property."
},
{
"ref":"genai_chat.openai.FunctionCalling",
"url":2,
"doc":"Function calling. Instantiates a function calling object. Parameters      name: str Function name. description: str Function description. parameters: list Function parameters. function_callable: Callable Function callable.  kwargs: dict Keyword-based arguments. References       [1] Function calling: https: platform.openai.com/docs/guides/gpt/function-calling"
},
{
"ref":"genai_chat.openai.FunctionCalling.name",
"url":2,
"doc":"Function name."
},
{
"ref":"genai_chat.openai.FunctionCalling.description",
"url":2,
"doc":"Function description."
},
{
"ref":"genai_chat.openai.FunctionCalling.parameters",
"url":2,
"doc":"Function parameters."
},
{
"ref":"genai_chat.openai.FunctionCalling.function_callable",
"url":2,
"doc":"Function callable."
},
{
"ref":"genai_chat.openai.FunctionCalling.kwargs",
"url":2,
"doc":"Keyword-based arguments."
},
{
"ref":"genai_chat.openai.FunctionCalling.params",
"url":2,
"doc":"Get keyword-based parameters from  parameters attribute. Returns    - arg_keys: [str] List of keyword-based parameters names.",
"func":1
},
{
"ref":"genai_chat.openai.BotOpenAI",
"url":2,
"doc":"OpenAI GenAI bot. Instantiates an OpenAI GenAI bot object. References       [1] OpenAI API Reference: https: platform.openai.com/docs/api-reference  [2] OpenAI Python Library: https: github.com/openai/openai-python"
},
{
"ref":"genai_chat.openai.BotOpenAI.chat",
"url":2,
"doc":"Sends a user message and receives a bot response from a LLM. Parameters      user_message: str User message.  kwargs: dict Keyword-based arguments. Returns    - bot_message, bot_citations: (str, [dict]) Bot message and list os citations.",
"func":1
},
{
"ref":"genai_chat.openai.BotOpenAI.get_genai_name",
"url":1,
"doc":"Get the Generative AI technology name. Returns    - _genai_name: str Generative AI technology name.",
"func":1
},
{
"ref":"genai_chat.openai.BotOpenAI.get_chat_history",
"url":1,
"doc":"Get chat history. Returns    - _chat_history: [dict] Chat history.",
"func":1
},
{
"ref":"genai_chat.openai.BotOpenAI.get_music_recommendations",
"url":1,
"doc":"Get music recommendations from database. Parameters      title: str Music title. genre: str Music genre. authors: str Music authors. country: str Music country. year: int Music year. Returns    - data: [dict] List of music recommendations. Notes   - This method allows for the incorporation of external data into the LLM without requiring model retraining. This integration is useful in refining the information considered by the LLM, leading to more personalized responses. Given that GenAI charges for LLM usage per token/word, it's prudent to limit the amount of external data injected into the LLM per request. It's recommended to adopt an approach that provides the user with the top N options based on identified parameters, rather than loading the entire database into the LLM. Additionally, you have the option to employ a custom recommendation engine or utilize a semantic search service like Azure Cognitive Search or GCP Cloud Search (also known as GCP Enterprise Search).",
"func":1
},
{
"ref":"genai_chat.openai.BotOpenAIFC",
"url":2,
"doc":"OpenAI GenAI bot (using function calling feature). Instantiates an OpenAI GenAI bot object (with function calling feature). References       [1] OpenAI API Reference: https: platform.openai.com/docs/api-reference  [2] OpenAI Python Library: https: github.com/openai/openai-python  [3] Function calling: https: platform.openai.com/docs/guides/gpt/function-calling  [4] OpenAI models: https: stackoverflow.com/a/75397187/16109419"
},
{
"ref":"genai_chat.openai.BotOpenAIFC.chat",
"url":2,
"doc":"Sends a user message and receives a bot response from a LLM. Parameters      user_message: str User message.  kwargs: dict Keyword-based arguments. Returns    - bot_message, bot_citations: (str, [dict]) Bot message and list os citations.",
"func":1
},
{
"ref":"genai_chat.openai.BotOpenAIFC.get_genai_name",
"url":1,
"doc":"Get the Generative AI technology name. Returns    - _genai_name: str Generative AI technology name.",
"func":1
},
{
"ref":"genai_chat.openai.BotOpenAIFC.get_chat_history",
"url":1,
"doc":"Get chat history. Returns    - _chat_history: [dict] Chat history.",
"func":1
},
{
"ref":"genai_chat.openai.BotOpenAIFC.get_music_recommendations",
"url":1,
"doc":"Get music recommendations from database. Parameters      title: str Music title. genre: str Music genre. authors: str Music authors. country: str Music country. year: int Music year. Returns    - data: [dict] List of music recommendations. Notes   - This method allows for the incorporation of external data into the LLM without requiring model retraining. This integration is useful in refining the information considered by the LLM, leading to more personalized responses. Given that GenAI charges for LLM usage per token/word, it's prudent to limit the amount of external data injected into the LLM per request. It's recommended to adopt an approach that provides the user with the top N options based on identified parameters, rather than loading the entire database into the LLM. Additionally, you have the option to employ a custom recommendation engine or utilize a semantic search service like Azure Cognitive Search or GCP Cloud Search (also known as GCP Enterprise Search).",
"func":1
},
{
"ref":"genai_chat.palm",
"url":3,
"doc":"PaLM GenAI operations."
},
{
"ref":"genai_chat.palm.BotPaLM",
"url":3,
"doc":"PaLM GenAI bot. Instantiates a PaLM GenAI bot object. References       [1] Migrate to PaLM API from Azure OpenAI: https: cloud.google.com/vertex-ai/docs/generative-ai/migrate-from-azure  [2] Set up Application Default Credentials: https: cloud.google.com/docs/authentication/provide-credentials-adc  [3] Locate the project ID: https: support.google.com/googleapi/answer/7014113?hl=en"
},
{
"ref":"genai_chat.palm.BotPaLM.chat",
"url":3,
"doc":"Sends a user message and receives a bot response from a LLM. Parameters      user_message: str User message.  kwargs: dict Keyword-based arguments. Returns    - bot_message, bot_citations: (str, [dict]) Bot message and list os citations.",
"func":1
},
{
"ref":"genai_chat.palm.BotPaLM.get_genai_name",
"url":1,
"doc":"Get the Generative AI technology name. Returns    - _genai_name: str Generative AI technology name.",
"func":1
},
{
"ref":"genai_chat.palm.BotPaLM.get_chat_history",
"url":1,
"doc":"Get chat history. Returns    - _chat_history: [dict] Chat history.",
"func":1
},
{
"ref":"genai_chat.palm.BotPaLM.get_music_recommendations",
"url":1,
"doc":"Get music recommendations from database. Parameters      title: str Music title. genre: str Music genre. authors: str Music authors. country: str Music country. year: int Music year. Returns    - data: [dict] List of music recommendations. Notes   - This method allows for the incorporation of external data into the LLM without requiring model retraining. This integration is useful in refining the information considered by the LLM, leading to more personalized responses. Given that GenAI charges for LLM usage per token/word, it's prudent to limit the amount of external data injected into the LLM per request. It's recommended to adopt an approach that provides the user with the top N options based on identified parameters, rather than loading the entire database into the LLM. Additionally, you have the option to employ a custom recommendation engine or utilize a semantic search service like Azure Cognitive Search or GCP Cloud Search (also known as GCP Enterprise Search).",
"func":1
},
{
"ref":"genai_chat.settings",
"url":4,
"doc":"Setup operations."
},
{
"ref":"genai_chat.settings.setup_logger",
"url":4,
"doc":"Define default logger. Parameters      name: str Module name. log_filepath: str Log filepath. mode: str Log file open mode. primary_level: str Primary log level. secondary_level: str Secondary log level. secondary_modules: [str] Secondary modules to filter. Returns    - logger: logging.Logger Logger.",
"func":1
},
{
"ref":"genai_chat.settings.get_settings",
"url":4,
"doc":"Import application settings from YAML-based file. Returns    - settings: dict Application settings.",
"func":1
},
{
"ref":"genai_chat.settings.read_yaml",
"url":4,
"doc":"Read YAML-based file content. Parameters      filepath: str YAML-based filepath. Returns    - content: dict Content from YAML-based file.",
"func":1
},
{
"ref":"genai_chat.utils",
"url":5,
"doc":"General utilities."
},
{
"ref":"genai_chat.utils.compare_strings",
"url":5,
"doc":"Compare strings based on fuzzy logic methods. Parameters      s1: str String. s2: str String. fuzzy_method: str Fuzzy method to compare strings. case_sensitive: bool Whether is case sensitive. Returns    - similarity: float Similarity between strings  s1 and  s2 in range [0,1]. References       [1] Fuzzy String Matching in Python Tutorial: https: www.datacamp.com/community/tutorials/fuzzy-string-python  [2] TheFuzz: https: github.com/seatgeek/thefuzz",
"func":1
},
{
"ref":"genai_chat.utils.merge_dict",
"url":5,
"doc":"Merges two simple and non-hierarchical dictionaries. Parameters      a: dict Dictionary. b: dict Dictionary. Returns    - x: dict Merged dictionary. References       [1] Using  Dict class to merge complex/hierarchical dictionaries: https: stackoverflow.com/a/70908985/16109419",
"func":1
},
{
"ref":"genai_chat.utils.md5_hash",
"url":5,
"doc":"Hash a string using the MD5 algorithm. Parameters      string: str String to convert to MD5 hash. Returns    - string_hash: str MD5 hash.",
"func":1
}
]