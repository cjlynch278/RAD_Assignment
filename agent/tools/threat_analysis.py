def analyze_threat_level(incident_data, cve_data):
    """
    Analyzes the threat level of incidents based on provided CVE data.

    Parameters:
    - incident_data: A dictionary containing incident details.
    - cve_data: A list of CVE entries relevant to the incidents.

    Returns:
    - A dictionary with incident IDs as keys and their corresponding threat levels.
    """
    threat_levels = {}

    for incident in incident_data:
        incident_id = incident.get("id")
        severity_score = 0

        for cve in cve_data:
            if cve.get("id") in incident.get("related_cves", []):
                severity_score += cve.get("severity_score", 0)

        if severity_score > 7:
            threat_levels[incident_id] = "High"
        elif severity_score > 4:
            threat_levels[incident_id] = "Medium"
        else:
            threat_levels[incident_id] = "Low"

    return threat_levels

# Example usage:
# incident_data = [{"id": "incident_1", "related_cves": ["CVE-2021-1234"]}]
# cve_data = [{"id": "CVE-2021-1234", "severity_score": 8}]
# print(analyze_threat_level(incident_data, cve_data))