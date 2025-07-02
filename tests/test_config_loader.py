import unittest
import os
import configparser
from d4jules.src.core.config_loader import load_config, ConfigError

# Helper to create temporary config files
def create_temp_config_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)

class TestConfigLoader(unittest.TestCase):

    def setUp(self):
        self.test_dir = "tests/temp_config_files"
        os.makedirs(self.test_dir, exist_ok=True)
        self.valid_config_content = """
[GOOGLE_AI]
API_KEY = test_api_key_123

[LLM]
MODEL_NAME = test_model_name

[SCRAPER]
MAX_PAGES = 100
"""
        self.valid_config_path = os.path.join(self.test_dir, "valid_config.ini")
        create_temp_config_file(self.valid_config_path, self.valid_config_content)

    def tearDown(self):
        # Clean up temporary files and directory
        if os.path.exists(self.valid_config_path):
            os.remove(self.valid_config_path)

        for f_name in os.listdir(self.test_dir):
            f_path = os.path.join(self.test_dir, f_name)
            if os.path.isfile(f_path):
                os.remove(f_path)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_load_config_success(self):
        expected_config = {
            'api_key': 'test_api_key_123',
            'model_name': 'test_model_name',
            'scraper_settings': {'max_pages': '100'}
        }
        loaded_config = load_config(self.valid_config_path)
        self.assertEqual(loaded_config, expected_config)

    def test_load_config_file_not_found(self):
        with self.assertRaisesRegex(ConfigError, "Configuration file .*not_found_config.ini.* not found"):
            load_config(os.path.join(self.test_dir, "not_found_config.ini"))

    def test_load_config_missing_google_ai_section(self):
        content = """
[LLM]
MODEL_NAME = test_model
"""
        path = os.path.join(self.test_dir, "missing_ga_section.ini")
        create_temp_config_file(path, content)
        with self.assertRaisesRegex(ConfigError, "Missing \\[GOOGLE_AI\\] section"):
            load_config(path)

    def test_load_config_missing_api_key(self):
        content = """
[GOOGLE_AI]
# API_KEY is missing
[LLM]
MODEL_NAME = test_model
"""
        path = os.path.join(self.test_dir, "missing_api_key.ini")
        create_temp_config_file(path, content)
        with self.assertRaisesRegex(ConfigError, "Missing 'api_key' in \\[GOOGLE_AI\\] section"):
            load_config(path)

    def test_load_config_missing_llm_section(self):
        content = """
[GOOGLE_AI]
API_KEY = test_key
"""
        path = os.path.join(self.test_dir, "missing_llm_section.ini")
        create_temp_config_file(path, content)
        with self.assertRaisesRegex(ConfigError, "Missing \\[LLM\\] section"):
            load_config(path)

    def test_load_config_missing_model_name(self):
        content = """
[GOOGLE_AI]
API_KEY = test_key
[LLM]
# MODEL_NAME is missing
"""
        path = os.path.join(self.test_dir, "missing_model_name.ini")
        create_temp_config_file(path, content)
        with self.assertRaisesRegex(ConfigError, "Missing 'model_name' in \\[LLM\\] section"):
            load_config(path)

    def test_load_config_empty_model_name(self):
        content = """
[GOOGLE_AI]
API_KEY = test_key
[LLM]
MODEL_NAME =
"""
        path = os.path.join(self.test_dir, "empty_model_name.ini")
        create_temp_config_file(path, content)
        with self.assertRaisesRegex(ConfigError, "Missing value for 'model_name' in \\[LLM\\] section"):
            load_config(path)

    def test_load_config_optional_scraper_section_present(self):
        # This is covered by test_load_config_success, which includes SCRAPER section
        pass

    def test_load_config_optional_scraper_section_absent(self):
        content = """
[GOOGLE_AI]
API_KEY = another_key

[LLM]
MODEL_NAME = another_model
"""
        path = os.path.join(self.test_dir, "no_scraper_section.ini")
        create_temp_config_file(path, content)
        expected_config = {
            'api_key': 'another_key',
            'model_name': 'another_model',
            'scraper_settings': {} # Expect empty dict if section is absent
        }
        loaded_config = load_config(path)
        self.assertEqual(loaded_config, expected_config)

if __name__ == '__main__':
    unittest.main()
