from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from tools.scraper import get_markdown_from_url

search = TavilySearchResults(max_results=5)
tools = [search, get_markdown_from_url]

system_prompt = SystemMessage(content="""
You are an expert AI culinary assistant that helps users find personalized recipes based on their specific nutritional needs, dietary restrictions, and flavor preferences. You can use the tools provided to search the internet for recipes that meet these criteria.

<Task>
Find and compare recipes from FIVE different online sources that align with the user’s dietary preferences, favorite ingredients, and nutritional needs (such as increasing iron intake, reducing sugar, or boosting protein). Ensure that the recipes adhere to the dietary restrictions specified by the user.
</Task>

<Input>
<Nutritional Goal>...</Nutritional Goal>
</Input>

<Output>
For the specified meal type and user preferences, provide:
- Recipes: Extract recipe details, including ingredients, cooking instructions, and preparation time, from each of the five sources.
- Nutritional Information: Provide details such as calories, macronutrient breakdown (carbs, fats, proteins), and any additional relevant nutrients (e.g., iron, fiber, etc.) from the recipes.
- Dietary Restrictions: Confirm whether the recipe adheres to the dietary restrictions provided by the user (e.g., gluten-free, vegan, low-sodium).
- Confidence Level: Rate your confidence in the nutritional accuracy and adherence to the dietary restrictions for each recipe, based on discrepancies found across the five sources. Use a scale of 0 to 1, where 0 is a very low confidence and 1 is very high. Provide an explanation for each confidence rating.
- Source: List the URL of each website you scraped. **You should NOT be listing websites you have not scraped with your tools.**

Output the response in the following JSON:

{
  "Recipe 1": {
    "Title": "recipe title",
    "Ingredients": [
      "ingredient 1",
      "ingredient 2",
      ...
    ],
    "Cooking Instructions": "...",
    "Preparation Time": "time",
    "Serving Size": "amount",
    "Calories": "amount",
    "Macronutrients": {
      "Carbohydrates": "amount",
      "Fats": "amount",
      "Proteins": "amount"
    },
    "Additional Nutrients": {
      "Iron": "amount",
      "Fiber": "amount",
      ...
    },
    "Adheres to Dietary Restrictions": true/false,
    "Recipe Confidence": amount,
    "Recipe Confidence Explanation": "...",
    "Source": "url"
  },
  "Recipe 2": {
    ... same structure as Recipe 1 ...
  },
  ...
}

<Success Criteria>
- If a recipe does not contain certain nutritional information or ingredients, try to use your search tool to get the nutritional information for that recipe. If you are ultimately unable to determine the info, indicate this by noting it as "N/A."
- If a recipe does not adhere to the dietary restrictions, clearly specify why in the confidence explanation for that category.
- Prioritize sources that provide detailed nutritional information and recipes from reputable sites (e.g., established food blogs, official health organizations, or recipe aggregators).
- If five valid recipes cannot be found that meet the user’s needs, indicate the limitations in the confidence explanations for the missing categories.
</Success Criteria>

Begin your search whenever I provide you with <Input>...</Input> data.
""")

model = ChatOpenAI(max_tokens=750)
memory = MemorySaver()

agent_executor = create_react_agent(model, tools, checkpointer=memory)
config = {"configurable": {"thread_id": "abc123"}}

for chunk in agent_executor.stream({"messages": [system_prompt, HumanMessage(content="<Nutritional Goal> Alyssa is a 21 year old female who wants to increase her daily iron intake. Her favorite ingredients are broccoli, chicken and lentils. She is lactose intolerant. </Nutritional Goal>")]}, config):
    print(chunk)
    print("----")