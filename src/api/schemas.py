from pydantic import BaseModel
from typing import List, Optional


class ExplainRequest(BaseModel):
    path: str
    model: Optional[str] = "mistral"
    use_cache: Optional[bool] = True


class FunctionInfo(BaseModel):
    name: str
    line_start: int
    line_end: int
    args: List[str]


class ClassInfo(BaseModel):
    name: str
    line_start: int
    line_end: int
    methods: List[str]


class AnalysisResult(BaseModel):
    file_name: str
    language: str
    total_lines: int
    functions: Optional[List[FunctionInfo]] = []
    classes: Optional[List[ClassInfo]] = []
    imports: Optional[List[str]] = []


class ExplainResponse(BaseModel):
    analysis: AnalysisResult
    explanation: str
    cached: bool
