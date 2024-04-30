from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.python import PythonREPL
from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain_experimental.tools.python.tool import PythonREPLTool
import langchain 
from langchain.agents import tool
from datetime import date
import pickle
langchain.debug = True
langchain.verbose = True

#model_url = "http://localhost:5000"
#llm = TextGen(model_url=model_url,max_new_tokens=2048, ban_eos_token=True)
@tool
def time(text: str) -> str:
    """Returns todays date, use this for any \
    questions related to knowing todays date. \
    The input should always be an empty string, \
    and this function will always return todays \
    date - any date mathmatics should occur \
    outside this function."""
    return str(date.today())

@tool
def FtoC(f: int) -> str:
    """Returns farenheit converted to celsius, use this for any \
    questions converting farenheit to celsius. \
    The input should always be a temperature in farenheit as an integer, \
    and this function will always return that integer converted to degrees celsius"""
    answer = (float(f) - 32)*(5/9)
    return str(answer)



@tool
def get_order(name: str) -> str:
    """Looks up the pizza ordered for a given name including size and toppings. Use for questions about pizza orders. \
    Always inputs a person's name and returns a string. It is acceptable if no order is found."""
    with open('db.pickle', 'rb') as handle:
        db = pickle.load(handle)

    try:
        item = db[name]
        response = name + " ordered " + " a " + item[0] + " " + item[1] + " pizza."
        return response
    except:
        return "No order found."

#tools = load_tools(
    #["human", "llm-math"],
#    ["human", "llm-math"], 
#    llm=math_llm,
#)
#tools = tools + [gender_guesser]

def python_agent(llm):
    agent = create_python_agent(llm, tool=PythonREPLTool(), verbose=True)
    return agent


def agent_initialize(agent_model, tools_list = ["llm-math"], custom_tools = [time, FtoC, get_order]): 
    tools = load_tools(tools_list, llm=agent_model)
    tools = tools + custom_tools
    agent= initialize_agent(
        tools, 
        agent_model, 
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        verbose = True)
    return agent

def question_agent(question, agent):
    return agent(question)

#@tool
#def log_name(name: str) -> str:
#    """Records name of person you are talking to \
#    the input should always be a proper name."""

#    with open('current.pickle', 'wb') as handle:
#        pickle.dump(name, handle, protocol=pickle.HIGHEST_PROTOCOL)

#    response = "Hello " + name
#    return response

#@tool
#def log_order(item: str) -> str:
#    """Places an order for an item, \
#    the input should always be an order item as a string"""
#    with open('db.pickle', 'rb') as handle:
#        db = pickle.load(handle)
#    with open('current.pickle', 'rb') as handle:
#        name = pickle.load(handle)

#    db[name] = item

#    with open('db.pickle', 'wb') as handle:
#        pickle.dump(db, handle, protocol=pickle.HIGHEST_PROTOCOL)

#    response = "Order for " + name + " of " + item + " made."
#    return response