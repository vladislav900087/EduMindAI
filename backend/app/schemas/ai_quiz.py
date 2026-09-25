from typing import Literal

from pydantic import BaseModel, Field, model_validator

class AIQuizOption(BaseModel):
    option_text: str = Field(min_length=1, max_length=500)
    is_correct: bool

class AIQuizQuestion(BaseModel):
    question_text: str = Field(min_length=1, max_length=1000)
    options: list[AIQuizOption] = Field(min_length=4, max_length=4)

    @model_validator(mode='after')
    def validate_correct_option(self):
        correct_count = sum(
            option.is_correct for option in self.options
        )

        if correct_count != 1:
            raise ValueError(
                'Every question must have exactly one correct option'
            )

        return self

class AIQuizGenerationResult(BaseModel):
    questions: list[AIQuizQuestion]


class AIQuizGenerationRequest(BaseModel):
    source_text: str = Field(min_length=20, max_length=12000)
    question_count: int = Field(default=5, ge=1, le=10)
    difficulty: Literal['easy', 'medium', 'hard'] = 'medium'




