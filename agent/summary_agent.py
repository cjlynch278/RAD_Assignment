# main.py

import json

from agent.base_agent import BaseAgent

class SummaryAgent(BaseAgent):
    """
    Summary Agent class for summarizing all given information
    """

    def __init__(self, gemini_api_key):
        """
        Initialize the SummaryAgent with the API key and Gemini API URL.
        """
        super().__init__(gemini_api_key)  # Initialize BaseAgent
        self.name = "OrechestratorAgent"
        self.description = "An agent that calls agents and makes function calls."
        self.gemini_api_key = gemini_api_key
        self.system_prompt = """
            You are a summary agent. You will be given data about an incident and
             relevant cve's that have been ordered for you by relevancy.
            Your job is to generate an analysis. Provide a brief, human-readable explanation of why certain
            CVEs are prioritized, linking them back to the incident details.
            
        """

        # I like having variables that the orchestrator agent can use when calling other agents
        # These variables are also given in the user prompt and either have values or be none.
        # This allows for a dynamic interaction where the results of one agent can be used by another.
        #  without having to pass them explicitly. This can be useful for chaining agent calls.
        
        # This will be cve 

    def f(self, incident_details, ordered_cves,):
        """
        Call the summary agent with the given input.
        This method will be used to call the Vitals agent with the given input.
        
        """

        try:
            user_prompt = f"""
                    Here is the incident {incident_details}"
                    Here are the relavent CVE's found  {relevant_cves}
                """

            response = self.call_gemini( system_prompt=self.system_prompt, user_prompt=user_prompt)
            #handle_response = self.handle_response(response=response)
            return response
        except Exception as e:
            print(f"Error calling Vitals agent: {e}")
            return None


