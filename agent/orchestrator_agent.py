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

    def __init__(self, gemini_api_key, collection_name="cves"):
        """
        Initialize the ThreatDetectionAgent with the API key and Gemini API URL.
        """
        super().__init__(gemini_api_key)  # Initialize BaseAgent
        self.name = "OrechestratorAgent"
        self.description = "An agent that calls agents and makes function calls."
        self.gemini_api_key = gemini_api_key
        self.system_prompt = (
            "You are a threat detection agent. You will be given data about an incident and must:\n"
            "1. Understand Incident Context: Reason about the affected assets, observed TTPs, and initial findings.\n"
            "2. Identify Relevant CVEs: Determine which CVEs are potentially relevant based on the incident context and affected software/hardware, using LLM reasoning and potentially querying data sources.\n"
            "3. Prioritize CVEs: Assess the risk and impact of relevant CVEs in the context of the specific incident, going beyond standard scores like CVSS.\n"
            "4. Generate Analysis: Provide a brief, human-readable explanation of why certain CVEs are prioritized, linking them back to the incident details.\n"
            "You will need to call the following functions to perform your tasks:\n"
            "1. perform_db_lookup(query): Perform a database lookup for the given query.\n"
            "2. analyze_threats(data): Analyze threats based on the provided data.\n"
            "3. lookup_assets(criteria): Lookup assets based on the provided criteria.\n"
        )

        # I like having variables that the orchestrator agent can use when calling other agents
        # These variables are also given in the user prompt and either have values or be none.
        # This allows for a dynamic interaction where the results of one agent can be used by another.
        #  without having to pass them explicitly. This can be useful for chaining agent calls.
        
        # This will be cve 
        self.cve_data = None  # Placeholder for CVE data

        self.threat_analysis_agent = ThreatAnalysisAgent(self.gemini_api_key)
        self.summary_agent = SummaryAgent(self.gemini_api_key)

    def call_orhestrator_agent(self, incident_data):
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
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "string",
                            "description": "The data to analyze for threats."
                        }
                    },
                    "required": ["data"]
                }
            },
            {
                "name": "summarize",
                "description": "Get a summary of the entire incident.",

            }
       
    ]


        try:
            user_prompt = "Perform an analysis. Here is the incident data: " + json.dumps(incident_data, indent=2)

            response = self.call_gemini( system_prompt=self.system_prompt, user_prompt=user_prompt, functions=functions)
            #handle_response = self.handle_response(response=response)
            return response
        except Exception as e:
            print(f"Error calling Vitals agent: {e}")
            return None



    def handle_response(self, response):
        """
        Handle the response from the Gemini API and execute the appropriate function.
        """
        try:
            # Extract the function call from the response
            function_call = response.candidates[0].content.parts[0].function_call

            if function_call and function_call.name == "perform_vector_db_lookup":
                # Extract arguments for the write_vitals function
                keywords = function_call.args
                # Returns all data on 
                self.cve_data = query_collection(keywords, self.collection_name, n_results=3)
                print(f"Vector DB Result: {vector_db_result}")

            ####
            #### Should this agent be called if there are not relavent cve's found?
            #### Really the goal of this agent may simply be to prioritize given CVE's.
            #### I'm going to make a decision to say that it must.
            ####
            if function_call and function_call.name == "analyze_threats" and self.cve_data:
                # Extract arguments for the analyze threates function
                threat_agent_resposne = self.threat_analysis_agent.call_threat_analysis_agent()
               

                # Execute the write_vitals function
                response = self.write_vitals(vitals_data)
                print(f"Vitals data written successfully: {vitals_data}")

                return response
            
            if function_call and function_call.name == "analyze_threats" and self.cve_data is None:
                
                return "No relevant CVE Data"
            
            if function_call and function_call.name == "summarize" and self.cve_data:
                # Extract arguments for the analyze threates function
                summary_agent_response = self.summary_agent.cal
               

                # Execute the write_vitals function
                response = self.write_vitals(vitals_data)
                print(f"Vitals data written successfully: {vitals_data}")

                return response
            
            if function_call and function_call.name == "analyze_threats" and self.cve_data is None:
                
                return "No relevant CVE Data"

        except Exception as e:
            print(f"Error handling response: {e}")
            return None