import json

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, HttpUrl

from app.prompt_libraries.ShortBlogPostPromptLibrary import ShortBlogPostPromptLibrary
from app.services.liteLLM import litellm_streamed_response
from app.config.settings import redis_client
from app.services.pdf_extractor import extract_pdf_text
from app.prompt_libraries.GenerateQuestionsFromPdfPromptLibrary import (
    GenerateQuestionsFromPdfPromptLibrary,
)
from app.prompt_libraries.DefineChaptersWeightPromptLibrary import (
    DefineChaptersWeightPromptLibrary,
)

router = APIRouter()


class ShortBlogPostController(BaseModel):
    topic: str = Field(..., min_length=3, max_length=200)
    keywords: str = Field(..., min_length=3, max_length=200)


async def store_inputs(short_blog_post_id: str, request: Request):
    if not short_blog_post_id:
        raise HTTPException(status_code=400, detail="Missing 'id' in the request data")

    request_data = await request.json()
    try:
        inputs = ShortBlogPostController(
            topic=request_data["data"]["topic"],
            keywords=request_data["data"]["keywords"],
        )
    except KeyError as e:
        raise HTTPException(status_code=422, detail=f"Missing required field: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid input: {str(e)}")

    json_data = json.dumps(inputs.model_dump())
    redis_client.set(f"short_blog_post_{short_blog_post_id}", json_data)
    return {
        "message": f"Short blog post inputs {short_blog_post_id} stored successfully"
    }


async def show_stream(file_path: str):
    pdf_text = extract_pdf_text(file_path)

    # prompt_library = GenerateQuestionsFromPdfPromptLibrary()
    prompt_library = DefineChaptersWeightPromptLibrary()
    system_prompt = prompt_library.system_prompt()
    user_prompt = prompt_library.user_prompt(pdf_text)

    return StreamingResponse(
        litellm_streamed_response(
            system_prompt,
            user_prompt,
        ),
        media_type="text/event-stream",
    )
