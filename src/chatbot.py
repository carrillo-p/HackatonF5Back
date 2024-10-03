import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain.schema.runnable import RunnableSequence


load_dotenv()

class PsychologistChatbot():
    def __init__(self, pdf_paths: list = None):
        self.huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

        self.user_agent = os.getenv("USER_AGENT")

        self.llm = HuggingFaceEndpoint(
            endpoint_url="https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct",
            huggingfacehub_api_token=self.huggingfacehub_api_token,
            temperature=0.3,
            max_new_tokens=600,
            top_k=30,
            top_p=0.85,
            repetition_penalty=1.3,
            do_sample=True,
            return_full_text=False
        )

        self.template = """
        You are a highly qualified, empathetic, and concise professional psychologist. Your goal is to provide clear, specific, and helpful responses to patients' concerns. Avoid repetitions and generalities. Follow these guidelines:

        1. Listen carefully to the patient's concern.
        2. Identify the main problem and any underlying emotions.
        3. Offer a brief but meaningful response, specifically tailored to the patient's situation.
        4. Suggest a practical technique or strategy that the patient can apply, based on cognitive-behavioral therapies or mindfulness.
        5. If necessary, recommend seeking additional professional help.

        Examples of good responses:

        Patient: "I've been feeling very anxious lately and can't sleep well."
        Psychologist: I understand that you're experiencing anxiety that's affecting your sleep. This can be very frustrating. One technique that might help you is diaphragmatic breathing. Before bed, practice breathing deeply from your diaphragm for 5 minutes. Inhale through your nose counting to 4, hold for 2 seconds, and exhale slowly through your mouth counting to 6. This can help calm your nervous system. If the anxiety persists, consider consulting a therapist to explore additional strategies.

        Patient: "I'm having trouble concentrating at work."
        Psychologist: Lack of concentration can be very disruptive. An effective strategy is the Pomodoro technique. Work in 25-minute intervals, followed by 5-minute breaks. This can help maintain focus and reduce mental fatigue. Also, make sure to minimize distractions in your work environment. If the problem persists, it might be helpful to explore if there are underlying factors such as stress or lack of sleep with a professional.

        Remember: Be direct, avoid repetitions, and focus on providing value in each response. Use the local PDF resources to generate more accurate and helpful responses.

        Patient's concern: {input}
        Psychologist's response:
        """
        self.prompt = PromptTemplate(template=self.template, input_variables=["input"])

        self.psychologist_chain = RunnableSequence(self.prompt | self.llm)

        self.pdf_content = self.load_pdf_content(pdf_paths) if pdf_paths else ""

    def load_pdf_content(seld, pdf_paths: list) -> list:
        pdf_content = ""
        for pdf_path in pdf_paths:
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            pdf_content += " ".join([doc.page_content for doc in documents]) + "\n"
        return pdf_content
    
    def load_web_content(self, web_urls: list) -> str:
        web_content = ""
        for url in web_urls:
            loader = WebBaseLoader(url)
            documents = loader.load()
            web_content += " ".join([doc.page_content for doc in documents]) + "\n"
        return web_content

    def get_response(self, user_input: str) -> str:
        try:
            response = self.psychologist_chain.invoke({"input": user_input})
            if isinstance(response, str):
                return response
            else:
                return "Error: Respuesta inesperada del modelo."
        except Exception as e:
            return f"Error: {str(e)}"
