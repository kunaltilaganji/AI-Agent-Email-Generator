import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("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"), model_name="llama-3.3-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
        You are Kunal, a machine learning engineer.  
        I’m a machine learning engineer with a strong background in data science and research,
        eager to contribute to in the industry's innovative work in machine learning.
        I’m excited about the possibility of bringing my skills to your team.
        With hands-on experience in designing and deploying machine learning models,
        My expertise spans tools like TensorFlow, PyTorch, and scikit-learn, alongside advanced techniques in 
        natural language processing, computer vision, and predictive analytics. 
        Using the above information, write a cold email to the client regarding the job mentioned above.
        Also add the most relevant ones from the following links to showcase my portfolio: {link_list} 
        Do not provide a preamble.
        ### EMAIL (NO PREAMBLE):

            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
