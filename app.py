import yaml
from smolagents import CodeAgent, HfApiModel
from smolagents.tools import Tool
from tools.resumescraper import ResumeScraperTool

class FinalAnswerTool(Tool):
    name = "final_answer"
    description = "Use this tool to provide your final roast"
    inputs = {
        "answer": {
            "type": "string",
            "description": "The final roast for the resume"
        }
    }
    output_type = "string"

    def forward(self, answer: str) -> str:
        return answer

def create_agent():
    final_answer = FinalAnswerTool()
    resume_scraper = ResumeScraperTool()
    
    # Use Qwen/Qwen2.5-Coder-32B-Instruct for roasting
    model = HfApiModel(
        max_tokens=2096,
        temperature=0.5,
        model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
        custom_role_conversions=None,
    )

    with open("prompts.yaml", 'r') as stream:
        prompt_templates = yaml.safe_load(stream)
        
    agent = CodeAgent(
        model=model,
        tools=[resume_scraper, final_answer],
        max_steps=6,
        verbosity_level=1,
        prompt_templates=prompt_templates
    )
    
    return agent
