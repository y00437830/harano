"""Data models for the Skill system."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ParameterType(str, Enum):
    """Supported parameter types for a Skill."""

    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    OBJECT = "object"
    ARRAY = "array"


class SkillParameter(BaseModel):
    """Describes a single input parameter of a Skill."""

    name: str = Field(..., description="Parameter name.")
    type: ParameterType = Field(..., description="Expected type of the parameter.")
    description: str = Field(default="", description="Human-readable description.")
    required: bool = Field(default=True, description="Whether the parameter is required.")
    default: Any = Field(default=None, description="Default value when not required.")


class SkillMetadata(BaseModel):
    """Metadata that describes a Skill."""

    name: str = Field(..., description="Unique skill identifier.")
    version: str = Field(default="0.1.0", description="Semantic version of the skill.")
    description: str = Field(default="", description="Human-readable description.")
    parameters: list[SkillParameter] = Field(
        default_factory=list,
        description="List of input parameters accepted by the skill.",
    )
    tags: list[str] = Field(default_factory=list, description="Categorisation tags.")
