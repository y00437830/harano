"""Base class for Harano Skills."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from harano.skill.models import SkillMetadata


class Skill(ABC):
    """Abstract base class that every concrete Skill must implement.

    Subclasses must:
    1. Provide a :attr:`metadata` class attribute that describes the skill.
    2. Implement the :meth:`execute` method that carries out the skill logic.

    Example::

        class GreetSkill(Skill):
            metadata = SkillMetadata(
                name="greet",
                description="Returns a greeting message.",
                parameters=[
                    SkillParameter(name="name", type=ParameterType.STRING),
                ],
            )

            def execute(self, **kwargs: Any) -> Any:
                return f"Hello, {kwargs['name']}!"
    """

    metadata: SkillMetadata

    @abstractmethod
    def execute(self, **kwargs: Any) -> Any:
        """Execute the skill with the given keyword arguments.

        Args:
            **kwargs: Input values matching the skill's declared parameters.

        Returns:
            The result produced by the skill.
        """

    def __repr__(self) -> str:
        return f"<Skill name={self.metadata.name!r} version={self.metadata.version!r}>"
