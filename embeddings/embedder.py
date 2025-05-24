import numpy as np

def embed_cve(cve_data):
    """
    Convert CVE data into a vector representation.
    
    Args:
        cve_data (dict): A dictionary containing CVE information.
        
    Returns:
        np.ndarray: A vector representation of the CVE.
    """
    # Example embedding logic (to be replaced with actual implementation)
    vector = np.array([hash(cve_data['id']), len(cve_data['description']), cve_data['severity']])
    return vector / np.linalg.norm(vector)

def embed_incident(incident_data):
    """
    Convert incident data into a vector representation.
    
    Args:
        incident_data (dict): A dictionary containing incident information.
        
    Returns:
        np.ndarray: A vector representation of the incident.
    """
    # Example embedding logic (to be replaced with actual implementation)
    vector = np.array([hash(incident_data['id']), len(incident_data['details']), incident_data['impact']])
    return vector / np.linalg.norm(vector)