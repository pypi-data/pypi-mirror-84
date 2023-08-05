import typer
import uvicorn
from loguru import logger
import click

from imghst.app.app import app
from imghst.__version__ import Version
from imghst.app.configuration.configuration import Configuration
from pathlib import Path

cli_app = typer.Typer()


@cli_app.command()
def run(
    port: int = Configuration.port_number_to_run_on,
    directory_path: str = Configuration.image_hosting_folder,
    api_key: str = Configuration.api_request_key,
    domain_prefix: str = Configuration.current_domain_url,
):

    splash_text = f"""
  _                 _         _   
 (_)_ __ ___   __ _| |__  ___| |_ 
 | | '_ ` _ \ / _` | '_ \/ __| __|
 | | | | | | | (_| | | | \__ \ |_ 
 |_|_| |_| |_|\__, |_| |_|___/\__|
              |___/               
                    v{Version()}
    """

    print(splash_text)
    print("\n")

    current_configuration_object = Configuration()
    current_configuration_object.api_request_key = api_key
    current_configuration_object.port_number_to_run_on = port
    current_configuration_object.image_hosting_folder = Path(directory_path)
    current_configuration_object.current_domain_url = domain_prefix

    app.configuration_object = current_configuration_object

    logger.info(f"Configured API Request Key: {api_key != 'DEFAULTCONFIGURATION'}")
    if api_key == "DEFAULTCONFIGURATION":
        click.secho(
            "Error: Default API key is still set. This may result in unauthorized users uploading data.",
            fg="red",
            blink=True,
            bold=True,
        )

    logger.info(f"Configured Port Number: {port}")
    logger.info(f"Configured Image Hosting Folder: {directory_path}")
    logger.info(f"Configured Current Domain URL: {domain_prefix}xxx.jpg")

    uvicorn.run(app, port=current_configuration_object.port_number_to_run_on)


if __name__ == "__main__":
    cli_app()
