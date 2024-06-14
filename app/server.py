# IMPORTS

from typing import Any, List, Union

from fastapi import FastAPI
from langchain_core.messages import AIMessage, FunctionMessage, HumanMessage
from app.chain_v1 import agent_executor

from langserve import add_routes
from langserve.pydantic_v1 import BaseModel, Field


from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Server Asistentes Bantotal",
    version="1.0",
    description="Servidor que mantiene asistentes de Bantotal",
)

origins = ["http://localhost", "http://localhost:9000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Input(BaseModel):
    input: str
    chat_history: List[Union[HumanMessage, AIMessage, FunctionMessage]] = Field(
        ...,
        extra={"widget": {"type": "chat", "input": "input", "output": "output"}},
    )


class Output(BaseModel):
    output: Any

add_routes(
    app,
    agent_executor.with_types(input_type=Input, output_type=Output).with_config(
        {"run_name": "agent"}
    ),
    path="/API"
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)