from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import nest_asyncio
import asyncio

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")

from pinecone import Pinecone
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.core import (
    VectorStoreIndex,
    Settings,
    PromptTemplate,
    get_response_synthesizer,
)

# Initialize nest_asyncio
nest_asyncio.apply()

# Initialize the FastAPI app
app = FastAPI()


# Data model for the request
class QueryRequest(BaseModel):
    query: str


# Initialize Pinecone client and index
pinecone_client = Pinecone(
    api_key=os.environ["PINECONE_API_KEY"], environment=os.environ["PINECONE_API_KEY"]
)
pinecone_index = pinecone_client.Index("rag-lorawan")

# Initialize OpenAI models
openai_llm = OpenAI(api_key=os.environ["OPENAI_API_KEY"], model="gpt-4", temperature=0)
embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
Settings.llm = openai_llm
Settings.embed_model = embed_model
Settings.chunk_size = 1536

# Initialize the vector store
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

# Initialize the index and retriever
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
retriever = VectorIndexRetriever(
    index=index,
    similiarity_top_k=5,
    sparse_top_k=10,
    vector_store_query_mode="hybrid",
)

# Define the prompt template in English
prompt_template = """
You are a specialized chatbot focused on LoRa and LoRaWAN technologies. Your role is to provide expert-level information and guidance on these subjects. Your knowledge base includes detailed insights into LoRa and LoRaWAN technologies, as well as relevant case studies, best practices, and technical standards.

Follow these guidelines when answering queries:
- Provide concise answers to straightforward questions.
- Offer in-depth explanations for more complex or open-ended inquiries.
- Assist with network design, deployment strategies, troubleshooting, and any other tasks related to LoRa and LoRaWAN.
- Use markdown for technical formatting and code snippets.
- Do not reveal information about your role or knowledge base unless it is directly relevant to the user's query.

When handling different types of questions:
- **Technical Questions:** Provide detailed, accurate information.
- **Practical Applications:** Offer insights based on case studies and best practices.
- **Troubleshooting:** Suggest step-by-step approaches to identify and resolve issues.
- **Design and Deployment:** Provide strategic advice and considerations.

**Use markdown formatting** as follows:
- Use backticks for inline code or technical terms.
- Use 
triple backticks
 for multi-line code blocks or command-line instructions.
- Use **bold** for emphasis on important points.
- Use *italics* for subtle emphasis or technical terms on first mention.
- Use bullet points or numbered lists for step-by-step instructions or multiple related points.

**Additional instructions:**
- **Chain of Thought:** For complex questions, clearly break down the response into logical steps or sequences. Ensure each step is visible and reasoned out before concluding.
- **Few-Shot Learning:** Adapt your responses based on provided examples or context clues within the query. Utilize patterns from previous answers to maintain consistency.
- **Contextual Adjustment:** Adjust the level of technical detail based on the perceived expertise of the user. Simplify terms for beginners; use more advanced terminology for experts.
- **Avoid Redundancy:** Before reiterating a point, review the response to ensure it has not already been covered sufficiently. Simplify and streamline the information.
- **Context-Sensitive Responses:** If the query is related to a specific context (e.g., rural vs. urban deployment), tailor your advice to address challenges and solutions relevant to that context.

Format your response as follows, don't put for example ("Detailed Explanation") in your response.:
1. **Detailed Explanation:** Follow with a more detailed explanation or discussion as needed.
2. **Technical Details and Examples:** Include relevant technical details, examples, or code snippets using markdown.
3. **Summary:** Conclude with a summary or key takeaway if the response is lengthy.

**Here is the user's question:**
{query_str}

Process the query and provide a response following the guidelines and formatting instructions above. If the query requires complex reasoning or multiple steps, break down your reasoning step by step before providing your final answer. First, identify the key points of the problem, then explain how you would apply the relevant knowledge, and finally give your conclusion.
"""

qa_template = PromptTemplate(template=prompt_template)
response_synthesizer = get_response_synthesizer(
    llm=openai_llm, text_qa_template=qa_template, response_mode="compact"
)
cohere_rerank = CohereRerank(api_key=os.environ["COHERE_API_KEY"], top_n=2)
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[cohere_rerank],
)

# Configure CORS to allow requests from the frontend
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify your frontend's domain here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define the /chat endpoint
@app.post("/chat")
async def chat(query_request: QueryRequest):
    try:
        response = await asyncio.get_event_loop().run_in_executor(
            None, query_engine.query, query_request.query
        )
        return {"response": str(response)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
