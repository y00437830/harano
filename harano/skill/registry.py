"""Registry for managing Skill instances."""

from __future__ import annotations

from typing import Iterator, Type

from harano.skill.base import Skill


class SkillRegistry:
    """A simple in-memory registry for :class:`~harano.skill.base.Skill` classes.

    Skills are stored by their metadata name and can be retrieved, listed,
    and unregistered at runtime.
    """

    def __init__(self) -> None:
        self._skills: dict[str, Type[Skill]] = {}

    def register(self, skill_class: Type[Skill]) -> Type[Skill]:
        """Register a Skill class.

        Can be used as a decorator::

            registry = SkillRegistry()

            @registry.register
            class MySkill(Skill):
                ...

        Args:
            skill_class: A concrete :class:`Skill` subclass to register.

        Returns:
            The same *skill_class* (enabling decorator usage).

        Raises:
            ValueError: If a skill with the same name is already registered.
        """
        name = skill_class.metadata.name
        if name in self._skills:
            raise ValueError(f"A skill named {name!r} is already registered.")
        self._skills[name] = skill_class
        return skill_class

    def unregister(self, name: str) -> None:
        """Remove a skill from the registry by name.

        Args:
            name: The skill name to remove.

        Raises:
            KeyError: If no skill with *name* is registered.
        """
        if name not in self._skills:
            raise KeyError(f"No skill named {name!r} is registered.")
        del self._skills[name]

    def get(self, name: str) -> Type[Skill]:
        """Return the Skill class registered under *name*.

        Args:
            name: The skill name to look up.

        Raises:
            KeyError: If no skill with *name* is registered.
        """
        if name not in self._skills:
            raise KeyError(f"No skill named {name!r} is registered.")
        return self._skills[name]

    def list_skills(self) -> list[str]:
        """Return a sorted list of registered skill names."""
        return sorted(self._skills.keys())

    def __iter__(self) -> Iterator[Type[Skill]]:
        return iter(self._skills.values())

    def __len__(self) -> int:
        return len(self._skills)

    def __contains__(self, name: str) -> bool:
        return name in self._skills
