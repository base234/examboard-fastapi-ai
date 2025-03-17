import json

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, HttpUrl

from app.prompt_libraries.ShortBlogPostPromptLibrary import ShortBlogPostPromptLibrary
from app.services.liteLLM import litellm_streamed_response
from app.config.settings import redis_client

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


async def show_stream(short_blog_post_id: str):
    if not short_blog_post_id:
        raise HTTPException(
            status_code=400, detail="Missing 'id' in the request parameters"
        )

    inputs = redis_client.get(f"short_blog_post_{short_blog_post_id}")

    if not inputs:
        raise HTTPException(
            status_code=404, detail=f"No data found for brief {short_blog_post_id}"
        )

    inputs = json.loads(inputs)
    inputs = ShortBlogPostController(**inputs)

    short_blog_post_prompt_library = ShortBlogPostPromptLibrary()

    system_prompt = short_blog_post_prompt_library.system_prompt()
    user_prompt = short_blog_post_prompt_library.user_prompt(inputs.topic, inputs.keywords)

    redis_client.delete(f"short_blog_post_{short_blog_post_id}")

    return StreamingResponse(
        litellm_streamed_response(
            system_prompt,
            user_prompt,
        ),
        media_type="text/event-stream",
    )
