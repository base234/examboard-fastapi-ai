from fastapi import FastAPI, UploadFile, File, APIRouter, Request, Query, HTTPException
from tempfile import NamedTemporaryFile
from app.controllers import (
   ShortBlogPostController,
   GenerateQuestionsFromPdfController,
)

router = APIRouter()

# for live text data streaming
@router.post("/ai/short-blog-post/{id}/inputs")
async def generate_short_blog_post(id: str, request: Request):
    return await ShortBlogPostController.store_inputs(id, request)

@router.get("/ai/short-blog-post/{id}/stream")
async def show_short_blog_post_stream(id: str):
    return await ShortBlogPostController.show_stream(id)

# show text data after generation completes
@router.post("/ai/blog-post/generate")
async def generate_blog_post(request: Request):
     request_data = await request.json()
     topic = request_data["data"]["topic"]

     try:
      post_content = await BlogPost.generate_post(topic)
      return {"topic": topic, "content": post_content}
     except Exception as e:
      raise HTTPException(status_code=500, detail=f"Error generating blog: {e}")


@router.post("/pdf/upload")
async def upload_file(file: UploadFile = File(...)):
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

        return await GenerateQuestionsFromPdfController.show_stream(temp_file_path)
