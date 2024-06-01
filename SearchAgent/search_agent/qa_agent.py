from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
from langchain.agents import Tool
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

class RAGTool:
    def __init__(self, file_path, template):
        self.file_path = file_path
        self.loader = CSVLoader(file_path)
        self.text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)
        self.conversational_memory = ConversationBufferWindowMemory(
            memory_key='chat_history',
            k=5,
            return_messages=True
        )
        self.data = self.loader.load()
        self.texts = self.text_splitter.split_documents(self.data)
        self.docsearch = Chroma.from_documents(self.texts, self.embeddings)

        self.PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])
        self.chain_type_kwargs = {"prompt": self.PROMPT}

        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.docsearch.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs=self.chain_type_kwargs
        )

        self.result = None
        self.ids = []

    def qa_run(self, query):
        self.result = self.qa({'query': query})
        return self.result['result']

class QAAgent:
    def __init__(self, rag_tool, club_rag_tool):
        self.llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)
        self.rag_tool = rag_tool
        self.club_rag_tool = club_rag_tool
        self.tools = [
            Tool(
                name='Lab Recommendation',
                func=self.rag_tool.qa_run,
                description=(
                    'use this tool when recommending appropriate Lab'
                ),
                return_direct=True
            ),
            Tool(
                name='Club Recommendation',
                func=self.club_rag_tool.qa_run,
                description=(
                    'use this tool when recommending appropriate Club'
                ),
                return_direct=True
            )
        ]
        ADDED_PREFIX = "You are a recommendation chatbot that helps college students find proper Labs or Clubs that match their preferences."
        PREFIX = "Answer the following questions as best you can. You have access to the following tools"
        PREFIX = f"{ADDED_PREFIX} {PREFIX}"

        self.agent = initialize_agent(
            agent='chat-conversational-react-description',
            tools=self.tools,
            llm=self.llm,
            verbose=True,
            max_iterations=3,
            early_stopping_method='generate',
            memory=self.rag_tool.conversational_memory,
            agent_kwargs={
                'prefix': PREFIX
            }
        )

    def run(self, query):
        result = self.agent({'input': query, 'chat_history': []})
        return result['output']
