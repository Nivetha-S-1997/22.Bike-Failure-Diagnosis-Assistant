#Importing the Libraries:
from helper_func import chat_with_model

from docx import Document as DocxDocument

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

#Document & Embeddings Loading:
doc=DocxDocument('Common bike problems- RAG.docx') #Reading word document

para_data=[] #Document reads plain texts (paragraphs)
table_data=[] #Document reads tables also

for para in doc.paragraphs: #Loops through the texts other than table
    if para.text.strip():
        para_data.append(para.text)

for table in doc.tables: #Loops through each table
    for row in table.rows: #Loops through each row in the table
        row_text=[cell.text.strip() for cell in row.cells] #Loops through each cell in the table & stores the texts of each cell
        table_data.append('|'.join(row_text)) #

documents=[Document(page_content=text) for text in (para_data + table_data)]

retriever = None

def get_retriever():
    global retriever

    if retriever is None:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        db = Chroma.from_documents(documents, embeddings)
        retriever = db.as_retriever()

    return retriever

chat_sessions={}

#Main function:
def process_user_message(user_text, session_id):
    chat_history = chat_sessions.setdefault(session_id, [])
    docs = get_retriever().invoke(user_text)
    context = "\n".join([d.page_content for d in docs])

    history_text = "\n".join(
    [f"User: {item['user']}\nAssistant: {item['bot']}"
     for item in chat_history]
)
    # Create chatbot response:
    System_instruction='''You are a helpful assistant that provides solutions to customers' bike faults, 
    similar to a mechanic.
    Use the retrieved context and previous conversation to understand the user's problem.
    
    Ask a follow-up question if important information is missing.
    Ask a maximum of 2 follow-up questions before providing the final diagnosis and action.
    Do not repeat questions that have already been answered.
    
    Safety instructions:
    - If the user's message requests harmful, violent, sexual, or hateful
    content unrelated to bike troubleshooting, politely refuse.
    - Do not provide dangerous repair instructions involving live electrical
    connections, fuel systems, or other hazardous procedures.
    - Recommend a qualified mechanic when a repair could be unsafe.'''

    message = [
    {
        'role': 'user',
        'parts': [{
            'text': System_instruction +
                    "\n\nPrevious conversation:\n" + history_text +
                    "\n\nCurrent user message:\n" + user_text
        }]
    }
]

    bot_reply=chat_with_model(message, context)

    chat_history.append({
    "user": user_text,
    "bot": bot_reply
})

    return bot_reply