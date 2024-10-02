import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain.schema.runnable import RunnableSequence

load_dotenv()

class PsychologistChatbot():
    def __init__(self):
        self.huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

        self.user_agent = os.getenv("USER_AGENT")

        self.llm = HuggingFaceEndpoint(
            endpoint_url="https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct",
            huggingfacehub_api_token=self.huggingfacehub_api_token,
            temperature=0.7,
            max_new_tokens=300,
            top_k=50,
            top_p=0.95,
            repetition_penalty=1.2,
            do_sample=True,
            return_full_text=False
        )

        self.template = """
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
        self.prompt = PromptTemplate(template=self.template, input_variables=["input"])

        self.psychologist_chain = RunnableSequence(self.prompt | self.llm)

        def get_response(self, user_input: str) -> str:
            response = self.psychologist_chain.invoke({"input": user_input})
            return response['output']
