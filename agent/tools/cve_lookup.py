class CVELookup:
    def __init__(self, cve_data):
        self.cve_data = cve_data

    def search(self, query):
        results = []
        for cve in self.cve_data:
            if query.lower() in cve['description'].lower():
                results.append(cve)
        return results

    def get_cve_details(self, cve_id):
        for cve in self.cve_data:
            if cve['id'] == cve_id:
                return cve
        return None

def load_cve_data(file_path):
    import json
    with open(file_path, 'r') as file:
        return json.load(file)