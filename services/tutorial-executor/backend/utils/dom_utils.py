# -*- coding: utf-8 -*-
"""
DOM Utilities

This module contains utility functions for manipulating and analyzing the Document Object Model (DOM) of web pages.
It can be used to extract information, modify elements, or interact with web content in various ways.
"""

from typing import List, Dict, Any, Optional
import re
from bs4 import BeautifulSoup
import requests


class DOMUtils:
    @staticmethod
    def fetch_page_content(url: str) -> str:
        """
        Fetches the HTML content of a web page.

        Args:
            url (str): The URL of the web page to fetch.

        Returns:
            str: The HTML content of the web page as a string.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.text
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch page content from {url}: {e}")

    @staticmethod
    def parse_html(html_content: str) -> BeautifulSoup:
        """
        Parses the HTML content into a BeautifulSoup object.

        Args:
            html_content (str): The HTML content as a string.

        Returns:
            BeautifulSoup: A parsed BeautifulSoup object representing the DOM.
        """
        return BeautifulSoup(html_content, 'html.parser')

    @staticmethod
    def find_elements_by_tag(soup: BeautifulSoup, tag_name: str) -> List[BeautifulSoup]:
        """
        Finds all elements in the DOM that match the specified tag name.

        Args:
            soup (BeautifulSoup): The parsed BeautifulSoup object.
            tag_name (str): The tag name to search for.

        Returns:
            List[BeautifulSoup]: A list of matching elements.
        """
        return soup.find_all(tag_name)

    @staticmethod
    def find_element_by_id(soup: BeautifulSoup, element_id: str) -> Optional[BeautifulSoup]:
        """
        Finds an element in the DOM by its ID.

        Args:
            soup (BeautifulSoup): The parsed BeautifulSoup object.
            element_id (str): The ID of the element to find.

        Returns:
            Optional[BeautifulSoup]: The matching element, or None if not found.
        """
        return soup.find(id=element_id)

    @staticmethod
    def find_elements_by_class(soup: BeautifulSoup, class_name: str) -> List[BeautifulSoup]:
        """
        Finds all elements in the DOM that match the specified class name.

        Args:
            soup (BeautifulSoup): The parsed BeautifulSoup object.
            class_name (str): The class name to search for.

        Returns:
            List[BeautifulSoup]: A list of matching elements.
        """
        return soup.find_all(class_=class_name)

    @staticmethod
    def get_element_text(element: BeautifulSoup) -> str:
        """
        Extracts and returns the text content of an element.

        Args:
            element (BeautifulSoup): The element from which to extract text.

        Returns:
            str: The text content of the element.
        """
        if element:
            return element.get_text(strip=True)
        return ""

    @staticmethod
    def get_element_attribute(element: BeautifulSoup, attribute: str) -> Optional[str]:
        """
        Extracts and returns the value of a specified attribute of an element.

        Args:
            element (BeautifulSoup): The element from which to extract the attribute.
            attribute (str): The name of the attribute to extract.

        Returns:
            Optional[str]: The value of the attribute, or None if not found.
        """
        if element and attribute in element.attrs:
            return element[attribute]
        return None

    @staticmethod
    def modify_element_attribute(element: BeautifulSoup, attribute: str, value: Any) -> None:
        """
        Modifies the value of a specified attribute of an element.

        Args:
            element (BeautifulSoup): The element whose attribute is to be modified.
            attribute (str): The name of the attribute to modify.
            value (Any): The new value for the attribute.
        """
        if element:
            element[attribute] = value

    @staticmethod
    def add_class_to_element(element: BeautifulSoup, class_name: str) -> None:
        """
        Adds a class to the specified element.

        Args:
            element (BeautifulSoup): The element to which the class will be added.
            class_name (str): The name of the class to add.
        """
        if element and 'class' in element.attrs:
            classes = element['class']
            if class_name not in classes:
                classes.append(class_name)
        elif element:
            element['class'] = [class_name]

    @staticmethod
    def remove_class_from_element(element: BeautifulSoup, class_name: str) -> None:
        """
        Removes a class from the specified element.

        Args:
            element (BeautifulSoup): The element from which the class will be removed.
            class_name (str): The name of the class to remove.
        """
        if element and 'class' in element.attrs:
            classes = element['class']
            if class_name in classes:
                classes.remove(class_name)
                if not classes:
                    del element['class']

    @staticmethod
    def replace_element_content(element: BeautifulSoup, new_content: str) -> None:
        """
        Replaces the content of an element with new content.

        Args:
            element (BeautifulSoup): The element whose content is to be replaced.
            new_content (str): The new content to insert.
        """
        if element:
            element.clear()
            element.append(BeautifulSoup(new_content, 'html.parser'))

    @staticmethod
    def extract_script_tags(soup: BeautifulSoup) -> List[BeautifulSoup]:
        """
        Extracts all <script> tags from the DOM.

        Args:
            soup (BeautifulSoup): The parsed BeautifulSoup object.

        Returns:
            List[BeautifulSoup]: A list of <script> tags.
        """
        return soup.find_all('script')

    @staticmethod
    def extract_style_tags(soup: BeautifulSoup) -> List[BeautifulSoup]:
        """
        Extracts all <style> tags from the DOM.

        Args:
            soup (BeautifulSoup): The parsed BeautifulSoup object.

        Returns:
            List[BeautifulSoup]: A list of <style> tags.
        """
        return soup.find_all('style')

    @staticmethod
    def remove_elements_by_tag(soup: BeautifulSoup, tag_name: str) -> None:
        """
        Removes all elements from the DOM that match the specified tag name.

        Args:
            soup (BeautifulSoup): The parsed BeautifulSoup object.
            tag_name (str): The tag name of elements to remove.
        """
        for elem in soup.find_all(tag_name):
            elem.decompose()

    @staticmethod
    def remove_elements_by_class(soup: BeautifulSoup, class_name: str) -> None:
        """
        Removes all elements from the DOM that match the specified class name.

        Args:
            soup (BeautifulSoup): The parsed BeautifulSoup object.
            class_name (str): The class name of elements to remove.
        """
        for elem in soup.find_all(class_=class_name):
            elem.decompose()

    @staticmethod
    def remove_elements_by_id(soup: BeautifulSoup, element_id: str) -> None:
        """
        Removes an element from the DOM by its ID.

        Args:
            soup (BeautifulSoup): The parsed BeautifulSoup object.
            element_id (str): The ID of the element to remove.
        """
        elem = soup.find(id=element_id)
        if elem:
            elem.decompose()