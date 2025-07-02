import configparser
import os

class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass

def load_config(config_path: str = "d4jules/config/config.ini") -> dict:
    """
    Loads configuration from the specified .ini file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: A dictionary containing the configuration values.
              Expected keys: "api_key" and "model_name".

    Raises:
        ConfigError: If the config file is not found, or required sections/keys are missing.
    """
    if not os.path.exists(config_path):
        template_path = config_path + ".template"
        if os.path.exists(template_path):
            raise ConfigError(
                f"Configuration file '{config_path}' not found. "
                f"A template exists at '{template_path}'. Please copy it to '{config_path}' and fill it."
            )
        raise ConfigError(f"Configuration file '{config_path}' not found.")

    config = configparser.ConfigParser()
    read_files = config.read(config_path)

    if not read_files:
        raise ConfigError(f"Could not read configuration file: '{config_path}'")

    loaded_config = {}

    if 'GOOGLE_AI' in config:
        if 'api_key' in config['GOOGLE_AI']:
            loaded_config['api_key'] = config['GOOGLE_AI']['api_key']
            # No validation for placeholder here, will be handled by usage or tests
        else:
            raise ConfigError("Missing 'api_key' in [GOOGLE_AI] section.")
    else:
        raise ConfigError("Missing [GOOGLE_AI] section in configuration file.")

    if 'LLM' in config:
        if 'model_name' in config['LLM']:
            loaded_config['model_name'] = config['LLM']['model_name']
            if not loaded_config['model_name']:
                 raise ConfigError("Missing value for 'model_name' in [LLM] section.")
        else:
            raise ConfigError("Missing 'model_name' in [LLM] section.")
    else:
        raise ConfigError("Missing [LLM] section in configuration file.")

    if 'SCRAPER' in config:
        loaded_config['scraper_settings'] = dict(config.items('SCRAPER'))
    else:
        loaded_config['scraper_settings'] = {}

    return loaded_config
