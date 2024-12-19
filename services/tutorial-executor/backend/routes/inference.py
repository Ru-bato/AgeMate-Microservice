# -*- coding: utf-8 -*-
"""
Inference

This module handles the inference logic for interacting with large language models (LLMs) or other machine learning models.
It includes loading models, processing input data, generating responses, and handling asynchronous operations.
"""

import asyncio
from typing import Any, Dict, List, Optional
import logging
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
import torch
# from transformers import AutoModelForCausalLM, AutoTokenizer

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

class ModelConfig(BaseModel):
    """
    Pydantic model for model configuration.
    """
    model_name: str = "distilgpt2"  # Default model name
    max_length: int = 50
    temperature: float = 1.0
    top_k: int = 50
    top_p: float = 0.95

# Load the model and tokenizer asynchronously
model_config = ModelConfig()
model: Optional[Any] = None
tokenizer: Optional[Any] = None

async def load_model():
    """
    Asynchronously loads the model and tokenizer based on the provided configuration.
    """
    global model, tokenizer
    logging.info("Loading model and tokenizer...")
    # model = AutoModelForCausalLM.from_pretrained(model_config.model_name)
    # tokenizer = AutoTokenizer.from_pretrained(model_config.model_name)
    # model.eval()  # Set to evaluation mode
    logging.info("Model and tokenizer loaded.")

@router.on_event("startup")
async def startup_event():
    """
    FastAPI startup event to load the model when the application starts.
    """
    await load_model()

@router.on_event("shutdown")
async def shutdown_event():
    """
    FastAPI shutdown event to clean up resources when the application shuts down.
    """
    if model is not None:
        del model
    if tokenizer is not None:
        del tokenizer
    logging.info("Resources cleaned up.")

class InferenceRequest(BaseModel):
    """
    Pydantic model for inference requests.
    """
    prompt: str
    max_length: Optional[int] = None
    temperature: Optional[float] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None

class InferenceResponse(BaseModel):
    """
    Pydantic model for inference responses.
    """
    generated_text: str

@router.post("/infer/", response_model=InferenceResponse)
async def infer(request: InferenceRequest, background_tasks: BackgroundTasks):
    """
    Endpoint to perform inference using the loaded model.

    Args:
        request (InferenceRequest): The inference request data.
        background_tasks (BackgroundTasks): FastAPI's BackgroundTasks object for running tasks asynchronously.

    Returns:
        InferenceResponse: The generated text from the model.
    """
    validate_model_loaded()

    gen_kwargs = {
        "max_length": request.max_length if request.max_length else model_config.max_length,
        "temperature": request.temperature if request.temperature else model_config.temperature,
        "top_k": request.top_k if request.top_k else model_config.top_k,
        "top_p": request.top_p if request.top_p else model_config.top_p
    }

    inputs = tokenizer(request.prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs, **gen_kwargs)

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Simulate a long-running task in the background
    background_tasks.add_task(logging.info, f"Inference completed for prompt: {request.prompt}")

    return {"generated_text": generated_text}

# Additional endpoints and utility functions

@router.post("/configure/", response_model=ModelConfig)
async def configure_model(config: ModelConfig):
    """
    Endpoint to configure the model parameters.

    Args:
        config (ModelConfig): The new configuration for the model.

    Returns:
        ModelConfig: The updated configuration.
    """
    global model_config, model, tokenizer
    if model is not None or tokenizer is not None:
        logging.warning("Reloading model with new configuration...")
        await load_model()  # Reload model with new configuration
    model_config = config
    return model_config

def validate_model_loaded():
    """
    Utility function to check if the model is loaded.

    Raises:
        HTTPException: If the model is not loaded.
    """
    if model is None or tokenizer is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

@router.get("/config/", response_model=ModelConfig)
async def get_current_config():
    """
    Endpoint to get the current model configuration.

    Returns:
        ModelConfig: The current configuration of the model.
    """
    return model_config

@router.post("/infer/batch/", response_model=List[InferenceResponse])
async def batch_infer(requests: List[InferenceRequest], background_tasks: BackgroundTasks):
    """
    Endpoint to perform batch inference using the loaded model.

    Args:
        requests (List[InferenceRequest]): A list of inference request data.
        background_tasks (BackgroundTasks): FastAPI's BackgroundTasks object for running tasks asynchronously.

    Returns:
        List[InferenceResponse]: A list of generated texts from the model.
    """
    validate_model_loaded()

    responses = []
    for req in requests:
        gen_kwargs = {
            "max_length": req.max_length if req.max_length else model_config.max_length,
            "temperature": req.temperature if req.temperature else model_config.temperature,
            "top_k": req.top_k if req.top_k else model_config.top_k,
            "top_p": req.top_p if req.top_p else model_config.top_p
        }

        inputs = tokenizer(req.prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = model.generate(**inputs, **gen_kwargs)

        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        responses.append({"generated_text": generated_text})

        # Simulate a long-running task in the background
        background_tasks.add_task(logging.info, f"Inference completed for prompt: {req.prompt}")

    return responses

# Health check endpoint
@router.get("/health")
async def health_check():
    """
    Endpoint to check the health status of the service.

    Returns:
        dict: A message indicating the service is healthy.
    """
    validate_model_loaded()
    return {"message": "Service is healthy"}

# # Error handling middleware can be added here as needed
# @router.exception_handler(HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException):
#     """
#     Custom exception handler for HTTP exceptions.

#     Args:
#         request (Request): The incoming request.
#         exc (HTTPException): The raised HTTP exception.

#     Returns:
#         JSONResponse: A JSON response containing error details.
#     """
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"message": exc.detail},
#     )

# Background task example
def process_inference_background(prompt: str, generated_text: str):
    """
    Background task to process inference results after generation.

    Args:
        prompt (str): The original prompt used for inference.
        generated_text (str): The generated text from the model.
    """
    logging.info(f"Processing inference results for prompt: {prompt}")
    # Simulate processing
    import time
    time.sleep(2)  # Simulating long-running task
    logging.info(f"Finished processing inference results for prompt: {prompt}")

@router.post("/infer/process/")
async def infer_and_process(request: InferenceRequest, background_tasks: BackgroundTasks):
    """
    Endpoint to perform inference and process the results in the background.

    Args:
        request (InferenceRequest): The inference request data.
        background_tasks (BackgroundTasks): FastAPI's BackgroundTasks object for running tasks asynchronously.

    Returns:
        InferenceResponse: The generated text from the model.
    """
    validate_model_loaded()

    gen_kwargs = {
        "max_length": request.max_length if request.max_length else model_config.max_length,
        "temperature": request.temperature if request.temperature else model_config.temperature,
        "top_k": request.top_k if request.top_k else model_config.top_k,
        "top_p": request.top_p if request.top_p else model_config.top_p
    }

    inputs = tokenizer(request.prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs, **gen_kwargs)

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Add background task to process the inference results
    background_tasks.add_task(process_inference_background, request.prompt, generated_text)

    return {"generated_text": generated_text}