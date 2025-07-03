import unittest
import os
import configparser
from src.core.config_loader import load_config, ConfigError

class TestConfigLoader(unittest.TestCase):

    def setUp(self):
        self.test_dir = "temp_test_config_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.config_path = os.path.join(self.test_dir, "test_config.ini")
        self.template_path = self.config_path + ".template"

        # Clean up any pre-existing files from previous failed tests
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        if os.path.exists(self.template_path):
            os.remove(self.template_path)

    def tearDown(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        if os.path.exists(self.template_path):
            os.remove(self.template_path)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def _create_config_file(self, content):
        with open(self.config_path, "w") as f:
            f.write(content)

    def _create_template_file(self, content):
        with open(self.template_path, "w") as f:
            f.write(content)

    def test_load_config_success(self):
        config_content = """
[GOOGLE_AI]
API_KEY = test_api_key_123
[LLM]
MODEL_NAME = test_model_name
[SCRAPER]
MAX_PAGES = 10
DEFAULT_OUTPUT_DIR = test_output/
[CUSTOM_SECTION]
custom_key = custom_value
int_key = 123
float_key = 45.67
"""
        self._create_config_file(config_content)
        config = load_config(self.config_path)
        self.assertEqual(config['api_key'], "test_api_key_123")
        self.assertEqual(config['model_name'], "test_model_name")
        self.assertIn('scraper_settings', config)
        self.assertEqual(config['scraper_settings']['max_pages'], '10') # configparser reads all as strings initially
        self.assertEqual(config['scraper_settings']['default_output_dir'], 'test_output/')
        self.assertIn('custom_section', config)
        self.assertEqual(config['custom_section']['custom_key'], 'custom_value')
        self.assertEqual(config['custom_section']['int_key'], 123) # Check auto-conversion
        self.assertEqual(config['custom_section']['float_key'], 45.67) # Check auto-conversion


    def test_load_config_file_not_found_with_template(self):
        self._create_template_file("[GOOGLE_AI]\nAPI_KEY = template_key")
        with self.assertRaisesRegex(ConfigError, f"Configuration file '{self.config_path}' not found. A template exists at '{self.template_path}'. Please copy it to '{self.config_path}' and fill it."):
            load_config(self.config_path)

    def test_load_config_file_not_found_no_template(self):
        with self.assertRaisesRegex(ConfigError, f"Configuration file '{self.config_path}' not found."):
            load_config(self.config_path)

    def test_load_config_missing_google_ai_section(self):
        config_content = """
[LLM]
MODEL_NAME = test_model_name
"""
        self._create_config_file(config_content)
        with self.assertRaisesRegex(ConfigError, "Missing \\[GOOGLE_AI\\] section in configuration file."):
            load_config(self.config_path)

    def test_load_config_missing_api_key(self):
        config_content = """
[GOOGLE_AI]
WRONG_KEY = some_value
[LLM]
MODEL_NAME = test_model_name
"""
        self._create_config_file(config_content)
        with self.assertRaisesRegex(ConfigError, "Missing 'api_key' in \\[GOOGLE_AI\\] section."):
            load_config(self.config_path)

    def test_load_config_missing_llm_section(self):
        config_content = """
[GOOGLE_AI]
API_KEY = test_api_key_123
"""
        self._create_config_file(config_content)
        with self.assertRaisesRegex(ConfigError, "Missing \\[LLM\\] section in configuration file."):
            load_config(self.config_path)

    def test_load_config_missing_model_name(self):
        config_content = """
[GOOGLE_AI]
API_KEY = test_api_key_123
[LLM]
WRONG_KEY = some_value
"""
        self._create_config_file(config_content)
        with self.assertRaisesRegex(ConfigError, "Missing 'model_name' in \\[LLM\\] section."):
            load_config(self.config_path)

    def test_load_config_empty_model_name(self):
        config_content = """
[GOOGLE_AI]
API_KEY = test_api_key_123
[LLM]
MODEL_NAME =
"""
        self._create_config_file(config_content)
        with self.assertRaisesRegex(ConfigError, "Missing value for 'model_name' in \\[LLM\\] section."):
            load_config(self.config_path)

    def test_load_config_optional_scraper_section_present(self):
        config_content = """
[GOOGLE_AI]
API_KEY = test_api_key
[LLM]
MODEL_NAME = test_model
[SCRAPER]
MAX_DEPTH = 5
TIMEOUT = 30
"""
        self._create_config_file(config_content)
        config = load_config(self.config_path)
        self.assertIn('scraper_settings', config)
        self.assertEqual(config['scraper_settings']['max_depth'], '5')
        self.assertEqual(config['scraper_settings']['timeout'], '30')

    def test_load_config_optional_scraper_section_absent(self):
        config_content = """
[GOOGLE_AI]
API_KEY = test_api_key
[LLM]
MODEL_NAME = test_model
"""
        self._create_config_file(config_content)
        config = load_config(self.config_path)
        self.assertIn('scraper_settings', config)
        self.assertEqual(config['scraper_settings'], {})

    def test_load_config_other_sections_conversion(self):
        config_content = """
[GOOGLE_AI]
API_KEY = test_api_key
[LLM]
MODEL_NAME = test_model
[SECTION_A]
key_str = value_str
key_int = 100
key_float = 23.45
key_bool_str_true = true
[SECTION_B]
another_key = another_value
"""
        self._create_config_file(config_content)
        config = load_config(self.config_path)

        self.assertIn('section_a', config)
        self.assertEqual(config['section_a']['key_str'], 'value_str')
        self.assertEqual(config['section_a']['key_int'], 100)
        self.assertEqual(config['section_a']['key_float'], 23.45)
        self.assertEqual(config['section_a']['key_bool_str_true'], 'true') # Stays string as per current logic

        self.assertIn('section_b', config)
        self.assertEqual(config['section_b']['another_key'], 'another_value')

if __name__ == '__main__':
    unittest.main()
