# main.py

import json

from agent.base_agent import BaseAgent

class OrchestratorAgent(BaseAgent):
    """
    ThreatDetectionAgent class for managing threat detection functionalities.
    Inherits from BaseAgent to handle Gemini API calls.
    """

    def __init__(self, gemini_api_key):
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


    def call_orhestrator_agent(self, incident_data):
        """
        Call the Vitals agent with the given input.
        This method will be used to call the Vitals agent with the given input.
        """
        functions = [
            {
                "name": "perform_db_lookup",
                "description": "Perform a database lookup for the given query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query to perform a database lookup for."
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
                "name": "lookup_assets",
                "description": "Lookup assets based on the provided criteria.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "criteria": {
                            "type": "string",
                            "description": "The criteria to lookup assets."
                        }
                    },
                    "required": ["criteria"]
                }
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

            if function_call and function_call.name == "write_vitals":
                # Extract arguments for the write_vitals function
                vitals_data = function_call.args

                # Execute the write_vitals function
                response = self.write_vitals(vitals_data)
                print(f"Vitals data written successfully: {vitals_data}")
                return response
            else:
                print("No valid function call detected in the response.")
                return None
        except Exception as e:
            print(f"Error handling response: {e}")
            return None