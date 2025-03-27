# summary_formatter.py

from abc import ABC, abstractmethod
from typing import Any

class SummaryFormatter(ABC):
    @abstractmethod
    def format(self, summary: Any) -> str:
        pass

    @abstractmethod
    def get_extension(self) -> str:
        pass


class MarkdownFormatter(SummaryFormatter):
    def format(self, summary: str) -> str:
        return summary

    def get_extension(self) -> str:
        return "md"


class JSONFormatter(SummaryFormatter):
    def format(self, summary: str) -> str:
        return summary

    def get_extension(self) -> str:
        return "json"


class HTMLFormatter(SummaryFormatter):
    def format(self, summary: str) -> str:
        return summary

    def get_extension(self) -> str:
        return "html"


class TextFormatter(SummaryFormatter):
    def format(self, summary: str) -> str:
        return summary

    def get_extension(self) -> str:
        return "txt"


class FormatterFactory:
    @staticmethod
    def get_formatter(fmt: str) -> SummaryFormatter:
        fmt = fmt.lower()
        if fmt == "markdown":
            return MarkdownFormatter()
        elif fmt == "json":
            return JSONFormatter()
        elif fmt == "html":
            return HTMLFormatter()
        elif fmt == "text":
            return TextFormatter()
        else:
            raise ValueError(f"Unsupported format: {fmt}. Available formats: markdown, json, html, text")