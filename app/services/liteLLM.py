import json
import uuid

import litellm
from fastapi import HTTPException
from litellm import completion

from app.config.services import get_services
from app.config.settings import get_settings

services = get_services()
settings = get_settings()

litellm.success_callback = ["langfuse"]
litellm.failure_callback = ["langfuse"]


def litellm_response(system_prompt, user_prompt):
    try:
        trace_id = str(uuid.uuid4())
        response = completion(
            model=services.LLM_MODEL,
            api_key=services.LLM_PROVIDER_API_KEY,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)

    data = response.choices[0].message.content
    if data:
        return data


def litellm_streamed_response(system_prompt, user_prompt):
    try:
        trace_id = str(uuid.uuid4())
        response = completion(
            model=services.LLM_MODEL,
            api_key=services.LLM_PROVIDER_API_KEY,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=True,
        )

        yield f"event: trace_id\ndata: {json.dumps({'trace_id': trace_id})}\n\n"
        for chunk in response:
            text = chunk.choices[0].delta.content
            print(text)
            if text:
                yield f"event: message\ndata: {json.dumps({'content': text})}\n\n"
    except GeneratorExit:
        raise
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        yield f"event: error\ndata: {json.dumps({'error': error_message})}\n\n"
    else:
        yield f"event: message\ndata: {json.dumps({'content': '[STOP_STREAMING]'})}\n\n"
