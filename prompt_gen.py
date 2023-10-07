from dataclasses import dataclass

# Constants
ROOT_BFS = (
    "I want you act as a Prompt Creator.\n"
    "Your goal is to draw inspiration from the #Given Prompt# to create a brand new prompt.\n"
    "This new prompt should belong to the same domain as the #Given Prompt# but be even more rare.\n"
    "The LENGTH and complexity of the #Created Prompt# should be similar to that of the #Given Prompt#.\n"
    "The #Created Prompt# must be reasonable and must be understood and responded by humans.\n"
    "'#Given Prompt#', '#Created Prompt#', 'given prompt' and 'created prompt' are not allowed to appear in #Created Prompt#\n"
)

ROOT_DFS = (
    "I want you act as a Prompt Rewriter.\n"
    "Your objective is to rewrite a given prompt into a more complex version to make those famous AI systems (e.g., chatgpt and GPT4) a bit harder to handle.\n"
    "But the rewritten prompt must be reasonable and must be understood and responded by humans.\n"
    "Your rewriting cannot omit the non-text parts such as the table and code in #The Given Prompt#:.\n"
    "Also, please do not omit the input in #The Given Prompt#.\n"
    "You SHOULD complicate the given prompt using the following method:\n"
    "{method}\n"
    "You should try your best not to make the #Rewritten Prompt# become verbose, #Rewritten Prompt# can only add 10 to 20 words into #The Given Prompt#.\n"
    "'#The Given Prompt#', '#Rewritten Prompt#', 'given prompt' and 'rewritten prompt' are not allowed to appear in #Rewritten Prompt#\n"
)

@dataclass
class PromptCreator:
    root_bfs: str = ROOT_BFS
    root_dfs: str = ROOT_DFS

    def create_breadth_prompt(self, instruction: str) -> str:
        assert isinstance(instruction, str), "Expected 'instruction' to be a string"
        return f"{self.root_bfs}#Given Prompt#:\n{instruction}\n#Created Prompt#:\n"

    def create_constraints_prompt(self, instruction: str) -> str:
        return self._dfs_method("Please add one more constraints/requirements into #The Given Prompt#'", instruction)

    def create_deepen_prompt(self, instruction: str) -> str:
        return self._dfs_method("If #The Given Prompt# contains inquiries about certain issues, the depth and breadth of the inquiry can be increased.", instruction)

    def create_concretizing_prompt(self, instruction: str) -> str:
        return self._dfs_method("Please replace general concepts with more specific concepts.", instruction)

    def create_reasoning_prompt(self, instruction: str) -> str:
        return self._dfs_method("If #The Given Prompt# can be solved with just a few simple thinking processes, you can rewrite it to explicitly request multiple-step reasoning.", instruction)

    def _dfs_method(self, method: str, instruction: str) -> str:
        assert isinstance(method, str), "Expected 'method' to be a string"
        assert isinstance(instruction, str), "Expected 'instruction' to be a string"
        return f"{self.root_dfs.format(method=method)}#The Given Prompt#:\n{instruction}\n#Rewritten Prompt#:\n"
