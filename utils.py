import base64
from io import BytesIO
import pdfplumber
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage


def get_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file.

    Args:
        pdf (bytes): The PDF file as bytes.

    Returns:
        str: The extracted text from the PDF.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as plumber_pdf:
            for page in plumber_pdf.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text


def convert_to_base64(pil_image: "PIL.Image") -> str:
    """
    Convert PIL images to Base64 encoded strings

    :param pil_image: PIL image
    :return: Re-sized Base64 string
    """

    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")  # You can change the format if needed
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


def convert_base64(file_data: bytes) -> str:
    """
    Convert binary file data to a base64-encoded string.
    """
    return base64.b64encode(file_data).decode("utf-8")

# def prompt_func(data):
#     text = data["text"]
#     image = data["image"]

#     image_part = {
#         "type": "image_url",
#         "image_url": f"data:image/jpeg;base64,{image}",
#     }

#     content_parts = []
#     text_part = {"type": "text", "text": text}

#     content_parts.append(image_part)
#     content_parts.append(text_part)

#     return [HumanMessage(content=content_parts)]

def prompt_func(data):
    text = data.get("text", "") 
    image = data.get("image")    # Safely get the image part (may be None)

    content_parts = []

    # Add the text part if provided
    if text:
        text_part = {"type": "text", "text": text}
        content_parts.append(text_part)

    # Add the image part if provided
    if image:
        image_part = {
            "type": "image_url",
            "image_url": f"data:image/jpeg;base64,{image}",
        }
        content_parts.append(image_part)

    # Return the formatted message for LangChain
    return [HumanMessage(content=content_parts)]

class MyOutputParser(BaseModel):
    question: str = Field(default_factory=str, description="Input question")
    answer: str = Field(default_factory=str, description="Answer to the question")