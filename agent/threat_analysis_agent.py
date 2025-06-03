# main.py

import json

from agent.base_agent import BaseAgent
from db.chroma_functions import *

class ThreatAnalysisAgent(BaseAgent):
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
        self.system_prompt = """
            "You are a threat detection agent. You will be given data about an incident and
              must understand incident Context: review the affected assets, observed TTPs, and initial findings.\n"

            "You will be given relevant CVE's (known threats), these are simply results from a vector db lookup." \
            "They arent necessarily relavent"
            " Your job is to prioritize CVEs: Assess the risk and impact of relevant CVEs in the context of the specific incident, "
            "going beyond standard scores like CVSS"
            "You will need to return a list back of the cve's in what you think are the most relevant organized from most relavent to least. 
            "You can disregard CVE's that you think are not relavent to the incident, but you must return at least one CVE. Do not include irrelavent cves"
            "Give a summary of the incident and the CVEs you found, and why you think they are relavent."
            "Quick summary what you think the next steps should be for the incident response team. Only provide 2-3 bullet points."
        """

        # I like having variables that the orchestrator agent can use when calling other agents
        # These variables are also given in the user prompt and either have values or be none.
        # This allows for a dynamic interaction where the results of one agent can be used by another.
        #  without having to pass them explicitly. This can be useful for chaining agent calls.
        
        # This will be cve 

    def call_threat_analysis_agent(self, incident_details, relevant_cves):
        """
        Call the Vitals agent with the given input.
        This method will be used to call the Vitals agent with the given input.
        """

        try:
            user_prompt = f"""
                    Here is the incident {incident_details}"
                    Here are the relavent CVE's found  {relevant_cves}
                """

            
            # try calling gemini 3 times. If the check_response fails, retry
            for _ in range(3):
                response = self.call_gemini(system_prompt=self.system_prompt, user_prompt=user_prompt)
                response_text = self.check_response(response)
                if response_text is not None:
                    return response_text
            print("Failed to get a valid response from threat analysis agent after 3 attempts.")
            return None
        except Exception as e:
            print(f"Error calling Threat Analysis Agent: {e}")
            return None


    def check_response(self, response):
        """
        Check the response from the Gemini API call.
        This method will be used to check the response from the Gemini API call.
        Check if the response contains response.candidates[0].content.parts[0].text

        """
        if response and hasattr(response, 'candidates') and len(response.candidates) > 0:
            content = response.candidates[0].content
            if hasattr(content, 'parts') and len(content.parts) > 0:
                text = content.parts[0].text
                # If text doesn't exist, return None
                if text:
                    return text
                else:
                    print("No text found in the response.")
                    return None
                
        else:
            print("No valid response received from Gemini API.")
            return None 