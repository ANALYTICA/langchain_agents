from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import ChatPromptTemplate
import pickle

#chat = ChatOpenAI(temperature=0.0, model=llm_model)
def parse_order(model, customer_order):
    name_schema = ResponseSchema(name="name",
                             description="Was is the name of the person making the pizza order?")
    size_schema = ResponseSchema(name="size",
                                      description="What is the size of the pizza? For example, small, medium or large.")
    type_schema = ResponseSchema(name="type",
                                    description="The topping of the pizza. For example supreme, italian, pepperoni.")

    response_schemas = [name_schema, 
                    size_schema,
                    type_schema]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    #print(format_instructions)
    review_template_2 = """\
    For the following text, extract the following information:

    name: Who is ordering? Give the name associated with this order.

    size: What is the size of the pizza ordered?

    type: What are the flavor of toppings? 

    text: {text}

    {format_instructions}
    """

    prompt = ChatPromptTemplate.from_template(template=review_template_2)

    messages = prompt.format_messages(text=customer_order, 
                                format_instructions=format_instructions)

    print(messages[0].content)
    response = model.invoke(messages[0].content)
    print(response)
    output_dict = output_parser.parse(response)
    type(output_dict)
    #output_dict.get('delivery_days')
    #return output_dict.get('delivery_days')
    with open('db.pickle', 'rb') as handle:
        db = pickle.load(handle)
    db[output_dict.get('name')] = [output_dict.get('size'),output_dict.get('type')]

    with open('db.pickle', 'wb') as handle:
        pickle.dump(db, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return "A "+ output_dict.get('size') + " " + output_dict.get('type') + " pizza order has been placed for " + output_dict.get('name') + "."  


#print(messages[0].content)
#response = chat(messages)
#print(response.content)
#output_dict = output_parser.parse(response.content)
#type(output_dict)
#output_dict.get('delivery_days')


customer_review = """\
This leaf blower is pretty amazing.  It has four settings:\
candle blower, gentle breeze, windy city, and tornado. \
It arrived in two days, just in time for my wife's \
anniversary present. \
I think my wife liked it so much she was speechless. \
So far I've been the only one using it, and I've been \
using it every other morning to clear the leaves on our lawn. \
It's slightly more expensive than the other leaf blowers \
out there, but I think it's worth it for the extra features.
"""

#review_template = """\
#For the following text, extract the following information:

#gift: Was the item purchased as a gift for someone else? \
#Answer True if yes, False if not or unknown.

#delivery_days: How many days did it take for the product \
#to arrive? If this information is not found, output -1.

#price_value: Extract any sentences about the value or price,\
#and output them as a comma separated Python list.

#Format the output as JSON with the following keys:
#gift
#delivery_days
#price_value

#text: {text}
#"""
#prompt_template = ChatPromptTemplate.from_template(review_template)
#print(prompt_template)
