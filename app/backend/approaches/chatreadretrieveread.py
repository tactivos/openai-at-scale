import openai
from approaches.approach import Approach

class ChatReadRetrieveReadApproach(Approach):


    # def __init__(self, chatgpt_deployment: str, gpt_deployment: str, sourcepage_field: str, content_field: str):
    def __init__(self, chatgpt_deployment: str, gpt_deployment: str):
        self.chatgpt_deployment = chatgpt_deployment
        self.gpt_deployment = gpt_deployment

    def run(self, history: list[dict], overrides: dict) -> any:
        print("history:", history)
        print("override:", overrides)
        top_p = overrides.get("top") or 0.95
        temperature = overrides.get("temperature") or 0.7
        max_tokens = overrides.get("maxResponse") or 800
        promptSystemTemplate = overrides.get("prompt_system_template") or "You are an AI assistant that helps people find information."

        # Step
        system_prompt_template = {}
        system_prompt_template["role"] = "system"
        system_prompt_template["content"] = promptSystemTemplate
        print("prompt:",[system_prompt_template]+self.get_chat_history_as_text(history))

        completion = openai.ChatCompletion.create(
            engine=self.chatgpt_deployment,
            messages = [system_prompt_template]+self.get_chat_history_as_text(history),
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None)
        print("completion: ", completion)
        return {"answer": completion.choices[0].message["content"]}
    
    def get_chat_history_as_text(self, history, include_last_turn=True, approx_max_tokens=1000) -> list:
        history_text = []
        for h in history:
            user_text = {}
            user_text["role"] = "user"
            user_text["content"] = h["user"]

            if h.get("bot") is None:
                history_text = history_text + [user_text]
            else:
                bot_text = {}
                bot_text["role"] = "assistant"
                bot_text["content"] = h.get("bot")
                history_text = history_text + [user_text, bot_text]
            # if len(history_text) > approx_max_tokens*4:
            #     break
        
        return history_text
