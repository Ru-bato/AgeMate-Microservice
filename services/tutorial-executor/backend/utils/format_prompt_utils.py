# -*- coding: utf-8 -*-
"""
Prompt Formatting Utilities

This module contains utility functions for formatting prompts used in various applications, including AI models.
It provides functionalities such as template filling, string manipulation, and ensuring prompts are well-formed for processing.
"""

from typing import Dict, Any, List, Optional
import json


class PromptFormatter:
    @staticmethod
    def fill_template(template: str, data: Dict[str, Any]) -> str:
        """
        Fills a prompt template with the provided data.

        Args:
            template (str): The template string containing placeholders like {key}.
            data (Dict[str, Any]): A dictionary of key-value pairs to substitute into the template.

        Returns:
            str: A formatted string with all placeholders replaced by corresponding values from the data.
        """
        try:
            return template.format(**data)
        except KeyError as e:
            raise Exception(f"Missing key in data for placeholder: {e}")
        except Exception as e:
            raise Exception(f"Failed to fill template: {e}")

    @staticmethod
    def ensure_single_line(prompt: str) -> str:
        """
        Ensures that the prompt is a single line by replacing newlines and excessive whitespace.

        Args:
            prompt (str): The original prompt string.

        Returns:
            str: A single-line version of the prompt.
        """
        return ' '.join(prompt.split())

    @staticmethod
    def wrap_in_quotes(prompt: str) -> str:
        """
        Wraps the prompt in double quotes.

        Args:
            prompt (str): The original prompt string.

        Returns:
            str: The prompt wrapped in double quotes.
        """
        return f'"{prompt}"'

    @staticmethod
    def escape_special_characters(prompt: str, special_chars: Optional[List[str]] = None) -> str:
        """
        Escapes special characters in the prompt to prevent misinterpretation during processing.

        Args:
            prompt (str): The original prompt string.
            special_chars (Optional[List[str]]): A list of special characters to escape. Defaults to common ones.

        Returns:
            str: The prompt with escaped special characters.
        """
        if special_chars is None:
            special_chars = ['\\', '"', '\n', '\r', '\t']
        for char in special_chars:
            prompt = prompt.replace(char, '\\' + char)
        return prompt

    @staticmethod
    def add_context(prompt: str, context: Dict[str, Any]) -> str:
        """
        Adds a context to the prompt by appending key-value pairs as JSON.

        Args:
            prompt (str): The original prompt string.
            context (Dict[str, Any]): A dictionary of additional context information.

        Returns:
            str: The prompt with added context in JSON format.
        """
        context_str = json.dumps(context, ensure_ascii=False)
        return f"{prompt} [CONTEXT] {context_str}"

    @staticmethod
    def truncate(prompt: str, max_length: int) -> str:
        """
        Truncates the prompt to ensure it does not exceed a specified maximum length.

        Args:
            prompt (str): The original prompt string.
            max_length (int): The maximum allowed length of the prompt.

        Returns:
            str: The truncated prompt.
        """
        if len(prompt) > max_length:
            return prompt[:max_length]
        return prompt

    @staticmethod
    def prepend_system_instruction(prompt: str, instruction: str) -> str:
        """
        Prepends a system instruction to the prompt.

        Args:
            prompt (str): The original prompt string.
            instruction (str): The system instruction to prepend.

        Returns:
            str: The prompt with the prepended system instruction.
        """
        return f"{instruction}\n{prompt}"

    @staticmethod
    def append_user_input(prompt: str, user_input: str) -> str:
        """
        Appends user input to the end of the prompt.

        Args:
            prompt (str): The original prompt string.
            user_input (str): The user input to append.

        Returns:
            str: The prompt with appended user input.
        """
        return f"{prompt}\n{user_input}"

    @staticmethod
    def replace_placeholders(prompt: str, placeholder_values: Dict[str, str]) -> str:
        """
        Replaces placeholders in the prompt with provided values.

        Args:
            prompt (str): The original prompt string containing placeholders like {key}.
            placeholder_values (Dict[str, str]): A dictionary mapping placeholders to their replacement values.

        Returns:
            str: The prompt with all placeholders replaced.
        """
        for placeholder, value in placeholder_values.items():
            prompt = prompt.replace(f"{{{placeholder}}}", str(value))
        return prompt

    @staticmethod
    def validate_format(prompt: str, required_keys: List[str]) -> bool:
        """
        Validates that the prompt contains all required keys.

        Args:
            prompt (str): The prompt string to validate.
            required_keys (List[str]): A list of keys that must be present in the prompt.

        Returns:
            bool: True if all required keys are present, False otherwise.
        """
        missing_keys = [key for key in required_keys if f"{{{key}}}" not in prompt]
        if missing_keys:
            raise Exception(f"Prompt is missing required keys: {missing_keys}")
        return True

    @staticmethod
    def normalize_whitespace(prompt: str) -> str:
        """
        Normalizes whitespace in the prompt, replacing multiple spaces with a single space and trimming.

        Args:
            prompt (str): The original prompt string.

        Returns:
            str: The prompt with normalized whitespace.
        """
        return ' '.join(prompt.split())

    @staticmethod
    def add_bullet_points(prompt: str, items: List[str], bullet: str = '*') -> str:
        """
        Adds bullet points to a list of items and appends them to the prompt.

        Args:
            prompt (str): The original prompt string.
            items (List[str]): A list of strings to be formatted as bullet points.
            bullet (str, optional): The bullet character to use. Defaults to '*'.

        Returns:
            str: The prompt with appended bullet-pointed items.
        """
        bulleted_items = '\n'.join([f"{bullet} {item}" for item in items])
        return f"{prompt}\n\n{bulleted_items}"