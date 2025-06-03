# main.py

import json

from agent.base_agent import BaseAgent
from agent.threat_analysis_agent import ThreatAnalysisAgent
from agent.summary_agent import SummaryAgent

from db.chroma_functions import *

class OrchestratorAgent(BaseAgent):
    """
    ThreatDetectionAgent class for managing threat detection functionalities.
    Inherits from BaseAgent to handle Gemini API calls.
    """

    def __init__(self, gemini_api_key, chroma_client, chroma_collection_name="cves"):
        """
        Initialize the ThreatDetectionAgent with the API key and Gemini API URL.
        """
        super().__init__(gemini_api_key)  # Initialize BaseAgent
        self.name = "OrechestratorAgent"
        self.description = "An agent that calls agents and makes function calls."
        self.gemini_api_key = gemini_api_key
        self.system_prompt =  """ 
            You are an orchestration agent. You will be given data about an incident and must:
            Your job will be to orchestrate the other agents to perform a task.
            
            You will need to call *ALL* of the following functions to perform your tasks:
            1. perform_db_lookup(query): Perform a database lookup for the given query.
            2. analyze_threats(data): Analyze threats based on the provided data.
            3. summarize(data): Summarize the provided data.

            Your job is to simply call the other agents and make function calls, do not return a text response.
            You are a function-calling agent. Only respond with a function call when appropriate.
            Do not include any explanatory text or natural language unless explicitly requested.
            Please call each of the functions in the order they are listed above.  
            You will return 3 different function calls, one for each of the functions.
            """
        

        # I like having variables that the orchestrator agent can use when calling other agents
        # These variables are also given in the user prompt and either have values or be none.
        # This allows for a dynamic interaction where the results of one agent can be used by another.
        #  without having to pass them explicitly. This can be useful for chaining agent calls.
        
        # This will be cve 

        self.threat_analysis_agent = ThreatAnalysisAgent(self.gemini_api_key)
        self.summary_agent = SummaryAgent(self.gemini_api_key)
        self.cve_results = None  # Placeholder for the results of the CVE lookup

        self.chroma_client = chroma_client
        self.chroma_collection_name = chroma_collection_name
        self.chroma_collection = get_collection(self.chroma_client, self.chroma_collection_name)

    def call_orchestrator_agent(self, incident_data):
        """
        Call the Vitals agent with the given input.
        This method will be used to call the Vitals agent with the given input.
        """
        functions = [
            {
                "name": "perform_vector_db_lookup",
                "description": """
                    Perform a vector db lookup to get relavent cve data. Look up relavent terms. 
                    These terms can be used to find CVEs that are relevant to the incident.   
                    These cve's are known threats. You should try to figure out if there are any relevant
                    cves that are related to what the incident is      
                    """,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Keywords or phrases to search for in the vector database."
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "analyze_threats",
                "description": "Analyze threats based on the provided data.",
            },

       
    ]


        try:
            
            user_prompt = "Perform an analysis. Here is the incident data: " + json.dumps(incident_data, indent=2)
            

            i = 0
            while i < 3:
                response = self.call_gemini(system_prompt=self.system_prompt, user_prompt=user_prompt, functions=functions)
                if not self.gaurd_rail_check(response):
                    print("Guard rail check failed, retrying...")
                    i += 1
                    continue
                else:
                    break
            
            handle_response = self.handle_response(response=response, incident_data=incident_data)
            return handle_response
        except Exception as e:
            print(f"Error calling Orchestrator agent: {e}")
            return None



    def gaurd_rail_check(self, response):
        # Check that there are 2 parts in the response return true if there are 3 parts, false otherwise
        if len(response.candidates[0].content.parts) == 2:
            return True
        else:
            return False


    def call_agent(self, part, incident_data):
        """
        Call the appropriate agent based on the part of the response.
        This method will be used to call the appropriate agent based on the part of the response.
        """
        if part.function_call.name == "perform_vector_db_lookup":
            keywords = part.function_call.args.get("query", "")
            self.cve_results = query_collection(query_text=keywords, collection=self.chroma_collection)
            return self.cve_results if self.cve_results else None
        elif part.function_call.name == "analyze_threats":
            self.threat_analysis = self.threat_analysis_agent.call_threat_analysis_agent(incident_details=incident_data, relevant_cves=self.cve_results)
            return self.threat_analysis
       
        else:
            print(f"Unknown function call: {part.function_call.name}")
            return None
        
    
    def handle_response(self,response, incident_data):
        """
        Handle the response from the Gemini API and execute the appropriate function.
        """

        for part in response.candidates[0].content.parts:
            if part.function_call:
                result = self.call_agent(part,incident_data=incident_data)
            else:
                print(f"No function call in part: {part.text}")


    
