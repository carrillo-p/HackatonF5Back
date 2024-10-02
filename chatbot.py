import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema.runnable import RunnableSequence
from langchain.memory import ConversationBufferMemory

load_dotenv()

# Configurar el token de Hugging Face (asegúrate de tener esto configurado)
huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Verificar si el token se cargó correctamente
if not huggingfacehub_api_token:
    raise ValueError("No se encontró el token HUGGINGFACEHUB_API_TOKEN. Asegúrate de que esté configurado en tu archivo .env")

user_agent = os.getenv("USER_AGENT")

# Configurar el modelo de lenguaje (LLM)
llm = HuggingFaceEndpoint(
    endpoint_url="https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct",
    huggingfacehub_api_token=huggingfacehub_api_token,
    temperature=0.7,
    max_new_tokens=300,
    top_k=50,
    top_p=0.95,
    repetition_penalty=1.2,
    do_sample=True,
    return_full_text=False
)
# Plantilla de prompt para el psicólogo AI
template = """
Eres un psicólogo profesional altamente cualificado, empático y conciso. Tu objetivo es proporcionar respuestas claras, específicas y útiles a las preocupaciones de los pacientes. Evita repeticiones y generalidades. Sigue estas pautas:

1. Escucha atentamente la preocupación del paciente.
2. Identifica el problema principal y cualquier emoción subyacente.
3. Ofrece una respuesta breve pero significativa, adaptada específicamente a la situación del paciente.
4. Sugiere una técnica o estrategia práctica que el paciente pueda aplicar.
5. Si es necesario, recomienda buscar ayuda profesional adicional.

Recuerda: Sé directo, evita repeticiones y céntrate en proporcionar valor en cada respuesta.

Preocupación del paciente: {input}

Respuesta del psicólogo:
"""

prompt = PromptTemplate(template=template, input_variables=["input"])

psychologist_chain = RunnableSequence(prompt | llm)

def chat_with_psychologist():
    print("Bienvenido a tu sesión con el psicólogo AI. Escribe 'salir' cuando quieras terminar la conversación.")
    
    while True:
        user_input = input("\nTú: ")
        
        if user_input.lower() == 'salir':
            print("Psicólogo AI: Gracias por tu tiempo. Recuerda que estoy aquí si necesitas hablar. Cuídate mucho.")
            break
        
        response = psychologist_chain.invoke(input=user_input)
        print(f"Psicólogo AI: {response}")
        
if __name__ == "__main__":
    chat_with_psychologist()