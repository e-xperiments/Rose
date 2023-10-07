import os
import dotenv
import json
import random
from llm_backend import OpenAILLM
from prompt_gen import PromptCreator

dotenv.load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def main():
    promgen = PromptCreator()
    fr = open('alpaca_data.json','r')
    llm = OpenAILLM(OPENAI_API_KEY)

    all_objs = json.load(fr)

    evol_objs = []


    for cur_obj in all_objs:
        
        instruction = cur_obj['instruction'].strip() + '\r\n'+ cur_obj['input'].strip()

        evol_prompts = []
        evol_prompts.append(promgen.create_constraints_prompt(instruction))
        evol_prompts.append(promgen.create_deepen_prompt(instruction))
        evol_prompts.append(promgen.create_concretizing_prompt(instruction))
        evol_prompts.append(promgen.create_reasoning_prompt(instruction))
        evol_prompts.append(promgen.create_breadth_prompt(instruction))

        selected_evol_prompt = random.choice(evol_prompts)


        evol_instruction = llm.get_completion(selected_evol_prompt)
        answer = llm.get_completion(evol_instruction)

        evol_objs.append({"instruction":evol_instruction,"output":answer})



    with open('alpaca_data_evol.json', 'w') as f:	
        json.dump(evol_objs, f, indent=4)



if __name__=="__main__":
    main()
