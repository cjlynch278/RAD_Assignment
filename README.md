
## Running
Open the demo.ipynb file and run through each cell

# RAD Assignment: Security Incident Analysis Agent

## Overview
This project implements a **Gen AI-powered agent** designed to assist in analyzing security incidents. The agent leverages a **Gemini's LLM** and integrates with tools like **ChromaDB** for contextual data retrieval. It simulates real-world security workflows, including CVE lookups, threat analysis, and incident summarization, to provide actionable insights for security analysts.

---

## Features
- **Incident Analysis**: Processes incident data to identify and prioritize threats.
- **CVE Lookup**: Retrieves relevant CVEs using a vector-based search in ChromaDB.
- **Threat Intelligence**: Simulates threat analysis to assess the impact of incidents.
- **Explainable Outputs**: Generates clear, traceable reasoning for its conclusions.
- **Extensible Design**: Modular architecture allows integration with additional tools or data sources.

---

## Project Structure
```
RAD_Assignment
├── agent
│   ├── orchestrator_agent.py       # Core agent for orchestrating tasks
│   ├── threat_analysis_agent.py    # Handles threat analysis
├── db
│   ├── chroma_functions.py         # Functions for interacting with ChromaDB
├── data
├── demo.ipynb                      # Jupyter notebook for experimentation
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

---

## Setup Instructions

### Prerequisites
- Python 3.8 or higher (3.13 not recommended)
- A valid API key for the LLM (if using a live LLM service)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd RAD_Assignment
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the project root and add your LLM API key:
     ```
     GEMINI_API_KEY=<your-api-key>
     ```

---

## Usage

### Experimentation
Use the Jupyter notebook for testing and experimentation:
```bash
jupyter notebook demo.ipynb
```

---

