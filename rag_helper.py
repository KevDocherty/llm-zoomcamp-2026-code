INSTRUCTIONS = """
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
"""

PROMPT_TEMPLATE = """
QUESTION: 
{question}

CONTEXT:
{context}
""".strip()



class RAGBase:
    '''
    Retrieval-Augmented Generation (RAG) base class for handling
    question answering using a combination of a search index and a
    language model.
    
    The 'index' parameter is anything with a search method, 
    whether minsearch, sqlitesearch, or something else. 
    
    The other four parameters all have defaults. 
    
    You only pass course, instructions, prompt_template, 
    or model when you want to override the default behavior. 
    
    We swap the index later without touching any of the RAG code.
    
    '''

    def __init__(
        self,
        index,
        llm_client,
        instructions=INSTRUCTIONS,
        prompt_template=PROMPT_TEMPLATE,
        course="llm-zoomcamp",
        model="gpt-5.4-mini"
    ):
        
        self.index = index
        self.llm_client = llm_client
        self.instructions = instructions
        self.course = course
        self.prompt_template = prompt_template
        self.model = model
        
    def search(self, query, num_results=5):
        '''
        Search the index for relevant documents based on the query.
        The search is filtered by the course specified in the instance.
        The boost_dict allows for boosting the relevance of certain fields.
        
        The search method delegates to the index.
        '''
        
        boost_dict = {"question": 3.0, "section": 0.5}
        filter_dict = {"course": self.course}

        return self.index.search(
            query,
            num_results=num_results,
            boost_dict=boost_dict,
            filter_dict=filter_dict
        )
        
    def build_context(self, search_results):
        '''
        Build a context string from the search results to be used in the prompt.
        Each document's section, question, and answer are included in the context.
        '''
        
        lines = []

        for doc in search_results:
            lines.append(doc["section"])
            lines.append("Q: " + doc["question"])
            lines.append("A: " + doc["answer"])
            lines.append("")

        return "\n".join(lines).strip()

    def build_prompt(self, query, search_results):
        '''
        Build a prompt string using the query and search results.
        The context is built from the search results and inserted into the prompt template.
        '''
        context = self.build_context(search_results)
        return self.prompt_template.format(
            question=query, context=context
        )
        
    def llm(self, prompt):
        '''
        Generate a response from the language model using the given prompt.
        The prompt is combined with the instructions and sent to the LLM client.
        '''
        
        input_messages = [
            {"role": "developer", "content": self.instructions},
            {"role": "user", "content": prompt}
        ]

        response = self.llm_client.responses.create(
            model=self.model,
            input=input_messages
        )

        return response.output_text
    
    def rag(self, query):
        '''
        Perform a Retrieval-Augmented Generation (RAG) process for the given query.
        The query is used to search the index, build a prompt, and generate a response
        from the language model.
        '''
        search_results = self.search(query)
        prompt = self.build_prompt(query, search_results)
        answer = self.llm(prompt)
        return answer