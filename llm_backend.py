import time
import logging
from typing import Tuple, Optional, Any

logging.basicConfig(level=logging.INFO)

class LanguageModel:
    def get_completion(self, prompt: str) -> Tuple[Optional[str], Optional[str]]:
        raise NotImplementedError("This method should be overridden by subclass")

class OpenAILLM(LanguageModel):
    
    def __init__(self, api_key: str,model=None):
        self.api_key = api_key
        self.moddel = model or "gpt-3.5-turbo"
    
    def get_completion(self, prompt: str) -> Tuple[Optional[str], Optional[str]]:
        try:
            import openai  # Importing here to avoid unnecessary dependencies for other language models
            openai.api_key = self.api_key
            response = openai.ChatCompletion.create(
                model=self.moddel,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ]
            )
            return response["choices"][0]["message"]["content"], None
        except Exception as e:
            return None, str(e)

class LLMClient:
    def __init__(self, lm: LanguageModel, max_retries: int = 15, retry_delay: int = 5):
        self.lm = lm
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    def call(self, prompt: str) -> Tuple[Optional[str], Optional[str]]:
        retries = self.max_retries
        while retries > 0:
            completion, err = self.lm.get_completion(prompt)
            if completion:
                return completion, None
            logging.warning(f"Retry for sample '{prompt}', Error: {err}")
            time.sleep(self.retry_delay)
            retries -= 1
        return None, f"Max retries reached for sample '{prompt}'"
    

# Usage
if __name__ == "__main__":
    openai_lm = OpenAI(api_key='your_api_key')
    lm_client = LLMClient(lm=openai_lm, max_retries=5, retry_delay=2)
    response, error = lm_client.call("Tell me a joke.")
    
    if response:
        logging.info(f"Response: {response}")
    else:
        logging.error(f"Error: {error}")
