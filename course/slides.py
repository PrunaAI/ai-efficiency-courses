from pathlib import Path
from typing import List, Optional, Union

import fitz  # PyMuPDF
import gradio as gr
from gradio_pdf import PDF
from pydantic import BaseModel, ConfigDict, Field, field_validator


class PDFSlideQuery(BaseModel):
    """
    Pydantic model for querying slides from a PDF.
    Note: We avoid using 'range' in the schema due to Pydantic limitations.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    pdf_path: Union[str, Path] = Field(..., description="Path to the PDF file.")
    slide_index: Optional[int] = Field(
        None, description="Index of the slide to display (0-based)."
    )
    slide_indices: Optional[List[int]] = Field(
        None, description="List of slide indices to display (0-based)."
    )
    phrases: Optional[Union[str, List[str]]] = Field(
        None, description="Phrase or list of phrases to search for in the slides."
    )

    @field_validator("pdf_path")
    @classmethod
    def validate_pdf_path(cls, v):
        """
        Validate and resolve the PDF path using robust resource resolution logic.

        Args:
            v (str | Path): The PDF filename or path.

        Returns:
            Path: The resolved absolute path to the PDF file.

        Raises:
            ValueError: If the file cannot be resolved or does not exist.
        """
        import importlib.resources
        from pathlib import Path

        path = Path(v)
        if path.is_absolute():
            if not path.exists() or not path.is_file():
                raise ValueError(f"PDF file does not exist at absolute path: {path}")
            resolved_path = path
        else:
            # Try to resolve as a resource in the 'slides' package
            try:
                slides_pkg = "slides"
                resource = importlib.resources.files(slides_pkg) / path.name
                if not resource.is_file():
                    raise FileNotFoundError(
                        f"Resource '{path.name}' not found in package '{slides_pkg}'"
                    )
                with importlib.resources.as_file(resource) as resource_path:
                    resolved_path = Path(resource_path)
                    if not resolved_path.exists() or not resolved_path.is_file():
                        raise FileNotFoundError(
                            f"Resolved resource path does not exist: {resolved_path}"
                        )
            except (
                ModuleNotFoundError,
                FileNotFoundError,
                AttributeError,
                NotADirectoryError,
            ) as e:
                raise ValueError(
                    f"Could not resolve PDF path '{v}' in installed slides directory: {e}"
                ) from e

        if resolved_path.suffix.lower() != ".pdf":
            raise ValueError(f"File is not a PDF: {resolved_path}")
        return resolved_path

    @field_validator("slide_index")
    @classmethod
    def validate_slide_index(cls, v):
        if v is not None and v < 0:
            raise ValueError("slide_index must be non-negative")
        return v

    @field_validator("slide_indices")
    @classmethod
    def validate_slide_indices(cls, v):
        if v is not None:
            if not isinstance(v, list):
                raise ValueError("slide_indices must be a list of ints")
            if not all(isinstance(i, int) and i >= 0 for i in v):
                raise ValueError("All slide_indices must be non-negative integers")
        return v

    @field_validator("phrases")
    @classmethod
    def validate_phrases(cls, v):
        if v is not None and not isinstance(v, (str, list)):
            raise ValueError("phrases must be a string or a list of strings")
        return v


class PDFSlideViewer:
    """
    Class to load a PDF and display a specific slide, a set of slides, or slides by searching for phrases.
    Designed for use in browser via Gradio.
    """

    def __init__(self, pdf_path: Union[str, Path]):
        # Use the robust PDF path validator to resolve the path, ensuring consistent resource resolution.
        self.pdf_path = PDFSlideQuery.validate_pdf_path(pdf_path)
        if not self.pdf_path.exists() or not self.pdf_path.is_file():
            raise FileNotFoundError(f"PDF file not found at: {self.pdf_path}")
        self.doc = fitz.open(str(self.pdf_path))
        self.num_pages = self.doc.page_count

    def show_slide(
        self,
        slide_index: Optional[int] = None,
        slide_indices: Optional[Union[List[int], range]] = None,
        phrases: Optional[Union[str, List[str]]] = None,
        highlight: bool = False,
    ) -> None:
        """
        Display a slide by index, a set of slides by indices, or by searching for phrases.

        Args:
            slide_index (Optional[int]): 0-based index of the slide to display.
            slide_indices (Optional[Union[List[int], range]]): List or range of slide indices to display.
            phrases (Optional[Union[str, List[str]]]): Phrase or list of phrases to search for.
            highlight (bool): If True, highlight found phrases on the slide(s).

        Returns:
            None. Launches a Gradio app to display the slide(s) in the browser.
        """
        try:
            # Show a single slide by index
            if slide_index is not None:
                if not (0 <= slide_index < self.num_pages):
                    raise IndexError(
                        f"slide_index {slide_index} out of range (0 to {self.num_pages - 1})"
                    )
                # Extract the single page as a new PDF
                pdf_bytes = self._extract_pages_as_pdf([slide_index])
                self._display_pdf_in_browser(pdf_bytes, title=f"Slide {slide_index}")
                return

            # Show a set of slides by indices
            if slide_indices is not None:
                # Accept both list and range for backward compatibility, but always convert to list
                if isinstance(slide_indices, range):
                    indices = list(slide_indices)
                else:
                    indices = slide_indices
                if not indices:
                    raise ValueError("slide_indices is empty")
                for idx in indices:
                    if not (0 <= idx < self.num_pages):
                        raise IndexError(
                            f"slide_indices contains out-of-range index {idx} (0 to {self.num_pages - 1})"
                        )
                pdf_bytes = self._extract_pages_as_pdf(indices)
                self._display_pdf_in_browser(pdf_bytes, title=f"Slides {indices}")
                return

            # Show slide(s) by searching for phrases
            if phrases is not None:
                if isinstance(phrases, str):
                    phrases = [phrases]
                found_indices = []
                for i in range(self.num_pages):
                    page = self.doc.load_page(i)
                    text = page.get_text()
                    if any(phrase.lower() in text.lower() for phrase in phrases):
                        found_indices.append(i)
                if not found_indices:
                    raise ValueError(
                        f"No slide found containing all phrases: {phrases}"
                    )
                # Optionally highlight phrases (not supported in gradio-pdf, so we skip)
                pdf_bytes = self._extract_pages_as_pdf(found_indices)
                self._display_pdf_in_browser(
                    pdf_bytes, title=f"Slides with phrases: {phrases}"
                )
                return

            raise ValueError(
                "Either slide_index, slide_indices, or phrases must be provided."
            )

        except Exception as e:
            raise RuntimeError(
                f"Failed to display slide(s) from PDF {self.pdf_path} with slide_index={slide_index}, slide_indices={slide_indices}, phrases={phrases}"
            ) from e

    def _extract_pages_as_pdf(self, indices: List[int]) -> bytes:
        """
        Extracts the specified pages from the PDF and returns them as a new PDF in bytes.

        Args:
            indices (List[int]): List of page indices to extract.

        Returns:
            bytes: The PDF bytes containing the selected pages.
        """
        try:
            new_doc = fitz.open()
            for idx in indices:
                new_doc.insert_pdf(self.doc, from_page=idx, to_page=idx)
            pdf_bytes = new_doc.write()
            new_doc.close()
            return pdf_bytes
        except Exception as e:
            raise RuntimeError(
                f"Failed to extract pages {indices} from PDF {self.pdf_path}"
            ) from e

    def _display_pdf_in_browser(
        self, pdf_bytes: bytes, title: str = "PDF Slides"
    ) -> None:
        """
        Launches a Gradio app to display the given PDF bytes in the browser.

        Args:
            pdf_bytes (bytes): The PDF file as bytes.
            title (str): Title for the Gradio app.

        Returns:
            None
        """
        try:
            import os
            import tempfile

            # Create a temporary file to store the PDF bytes
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                temp_file.write(pdf_bytes)
                temp_file_path = temp_file.name

            try:
                with gr.Blocks() as demo:
                    gr.Markdown(f"### {title}")
                    PDF(value=temp_file_path, label="PDF Slides", interactive=True)
                demo.launch(quiet=True)
            finally:
                # Clean up the temporary file
                try:
                    os.unlink(temp_file_path)
                except OSError:
                    pass  # File might already be deleted
        except Exception as e:
            raise RuntimeError(f"Failed to launch Gradio PDF viewer for {title}") from e


def show_slides(
    pdf_path: Union[str, Path],
    phrases: Optional[Union[str, List[str]]] = None,
    slide_indices: Optional[Union[List[int], range]] = None,
    slide_index: Optional[int] = None,
):
    """
    Utility function to display slides from a PDF using phrases or indices.

    Args:
        pdf_path (Union[str, Path]): Path to the PDF file.
        phrases (Optional[Union[str, List[str]]]): Phrase or list of phrases to search for.
        slide_indices (Optional[Union[List[int], range]]): List or range of slide indices to display.
        slide_index (Optional[int]): Index of the slide to display.

    Returns:
        None. Launches a Gradio app to display the slide(s) in the browser.
    """
    viewer = PDFSlideViewer(pdf_path)
    viewer.show_slide(
        slide_index=slide_index, slide_indices=slide_indices, phrases=phrases
    )


# Example usage:
# viewer = PDFSlideViewer("path/to/slides.pdf")
# viewer.show_slide(slide_index=2)
# viewer.show_slide(slide_indices=[2, 3, 4])
# viewer.show_slide(slide_indices=range(5, 8))
# viewer.show_slide(phrases="Transformer")
# viewer.show_slide(phrases=["Transformer", "Attention"])
