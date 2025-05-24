def get_asset_info(asset_id):
    # Simulated asset data
    assets = {
        "1": {"name": "Server A", "type": "Web Server", "location": "Data Center 1"},
        "2": {"name": "Database B", "type": "Database Server", "location": "Data Center 2"},
        "3": {"name": "Workstation C", "type": "User Workstation", "location": "Office 1"},
    }
    
    return assets.get(asset_id, "Asset not found")

def list_all_assets():
    # Simulated asset data
    assets = {
        "1": {"name": "Server A", "type": "Web Server", "location": "Data Center 1"},
        "2": {"name": "Database B", "type": "Database Server", "location": "Data Center 2"},
        "3": {"name": "Workstation C", "type": "User Workstation", "location": "Office 1"},
    }
    
    return assets.values()