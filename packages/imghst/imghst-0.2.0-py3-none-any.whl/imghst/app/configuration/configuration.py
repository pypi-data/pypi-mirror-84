
from imghst.app.configuration.unique_generators.uuid_based import generate_unique_id
from pathlib import Path

class Configuration:
    """ Do Not Touch Anything Here. Configure with arguments. """
    
    api_request_key = "DEFAULTCONFIGURATION"
    image_unique_file_name = generate_unique_id
    image_hosting_folder = Path(".")
    
    port_number_to_run_on = 5000
