import re
import logging

from markdown import markdown
from bs4 import BeautifulSoup
from src.domain.pydantic_models.input_models import InputDocument


logger = logging.getLogger(__name__)

class ObsidianMarkdownProcessor:

    @staticmethod
    def _get_bibliographic_references_from_html(soup):
        references_section = soup.find("h1", string="References")
        references = []

        if not references_section:
            return references
        
        references_content = references_section.find_next_sibling()
        if not references_content:
            return references
        
        references_lines = references_content.text.splitlines()
        for line in references_lines:
            line = line.strip()

            if line.startswith("[[") and line.endswith("]]"):
                references.append(line[2:-2])
            elif line:
                references.append(line)

        return references
    
    @staticmethod
    def _get_tags_from_html(soup):
        tags_section = soup.find("h1", string="Tags")
        tags = []
        if not tags_section:
            return tags

        tags_content = tags_section.find_next_sibling()
        if tags_content:
            tags = [word.replace("#", "", 1) for word in tags_content.text.split() if word.startswith("#")]
        return tags

    @staticmethod
    def _get_inline_references_from_html(soup, excluded_references):
        """
        Extracts inline references that are not in the References sections.

        Args:
            soup (BeautifulSoup): Parsed HTML content.
            excluded_references (list): References to exclude (e.g., from Tags and References sections).

        Returns:
            list: Inline references that are not excluded.
        """
        # Combine all text content from the soup
        full_text = soup.get_text(separator="\n")

        # Use regex to find all [[...]] patterns
        all_references = set(re.findall(r"\[\[(.+?)\]\]", full_text))

        # Remove excluded references
        return list(all_references - set(excluded_references))

    @staticmethod
    def _get_content_excluding_sections(soup):
        """
        Extracts the main content of the Markdown, excluding Tags and References sections.

        Args:
            soup (BeautifulSoup): Parsed HTML content.

        Returns:
            str: Remaining content as plain text, excluding Tags and References sections.
        """
        content_soup = soup.__copy__()

        sections_to_exclude = ["Tags", "References"]

        for section_title in sections_to_exclude:
            section = content_soup.find("h1", string=section_title)
            if section:
                next_sibling = section.find_next_sibling()
                while next_sibling:
                    if next_sibling.name and next_sibling.name.startswith("h"):
                        break
                    sibling_to_remove = next_sibling
                    next_sibling = next_sibling.find_next_sibling()
                    sibling_to_remove.extract()
                section.extract()

        return content_soup.get_text(separator="\n").strip()

    def _preprocess_markdown(md_content):
        """
        Preprocesses Markdown content to avoid interpreting hashtags as headings.

        Args:
            md_content (str): The raw Markdown content.

        Returns:
            str: Preprocessed Markdown content.
        """
        return re.sub(r"#(\w+)", r"\\#\1", md_content)

    @staticmethod
    def process(md_metadata: dict) -> InputDocument:
        """
        Processes a Markdown content and creates a InputDocument object.

        Args:
            file_path (str): The path to the Markdown file.

        Returns:
            InputDocument: An instance of the InputDocument model.
        """
        logger.info("Processing the Markdown...")
        logger.debug(f"Markdown Content: {md_metadata}")
        raw_content = md_metadata["raw_content"]
        folders = md_metadata["folders"]
        title = md_metadata["title"]
        logger.info(f"Markdown Title: {title}")

        raw_content = ObsidianMarkdownProcessor._preprocess_markdown(raw_content)
        html_content = markdown(raw_content)
        soup = BeautifulSoup(html_content, "html.parser")
        logger.info("Markdown converted into html")
        
        subtitles = [h2.text.strip() for h2 in soup.find_all("h2")]
        logger.info("Subtitles extracted")

        if not subtitles:
            logger.warning("There are not subtitles in the markdown")
        logger.info(f"Markdown First Subtitle: {subtitles[0:1]} and last: {subtitles[-2:-1]}")
        logger.debug(f"Markdown Subtitles: {subtitles}")
        

        content = ObsidianMarkdownProcessor._get_content_excluding_sections(soup)
        logger.info("Content extracted")
        logger.debug(f"Markdown Content: {content}")

        tags = ObsidianMarkdownProcessor._get_tags_from_html(soup)
        logger.info(f"Tags extracted. First one: {tags[0:1]}, Last one: {tags[-2:-1]}")
        logger.debug(f"Markdown Tags: {tags}")

        bibliographic_references = ObsidianMarkdownProcessor._get_bibliographic_references_from_html(soup)
        logger.info(f"References extracted. First one: {bibliographic_references[0:1]}, "
                    "Last one: {bibliographic_references[-2:-1]}")
        logger.debug(f"Markdown References: {bibliographic_references}")

        obsidian_references = ObsidianMarkdownProcessor._get_inline_references_from_html(soup, bibliographic_references)

        return InputDocument(
            title=title,
            subtitles=subtitles,
            content=content,
            raw_content=raw_content,
            folders=folders,
            tags=tags,
            bibliographic_references=bibliographic_references,
            obsidian_references=obsidian_references
        )
