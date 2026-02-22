"""Tests for the Skill system."""

import pytest

from harano.skill.base import Skill
from harano.skill.models import ParameterType, SkillMetadata, SkillParameter
from harano.skill.registry import SkillRegistry


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------


def make_greet_skill_class() -> type[Skill]:
    """Return a fresh GreetSkill class (not yet registered anywhere)."""

    class GreetSkill(Skill):
        metadata = SkillMetadata(
            name="greet",
            description="Returns a greeting message.",
            parameters=[
                SkillParameter(name="name", type=ParameterType.STRING),
            ],
        )

        def execute(self, **kwargs):
            return f"Hello, {kwargs['name']}!"

    return GreetSkill


def make_add_skill_class() -> type[Skill]:
    class AddSkill(Skill):
        metadata = SkillMetadata(
            name="add",
            description="Adds two integers.",
            parameters=[
                SkillParameter(name="a", type=ParameterType.INTEGER),
                SkillParameter(name="b", type=ParameterType.INTEGER),
            ],
        )

        def execute(self, **kwargs):
            return kwargs["a"] + kwargs["b"]

    return AddSkill


# ---------------------------------------------------------------------------
# SkillParameter & SkillMetadata
# ---------------------------------------------------------------------------


class TestSkillParameter:
    def test_required_defaults_to_true(self):
        param = SkillParameter(name="x", type=ParameterType.STRING)
        assert param.required is True

    def test_optional_parameter(self):
        param = SkillParameter(
            name="x", type=ParameterType.STRING, required=False, default="hi"
        )
        assert param.required is False
        assert param.default == "hi"

    def test_all_parameter_types(self):
        for pt in ParameterType:
            param = SkillParameter(name="p", type=pt)
            assert param.type == pt


class TestSkillMetadata:
    def test_defaults(self):
        meta = SkillMetadata(name="my-skill")
        assert meta.version == "0.1.0"
        assert meta.description == ""
        assert meta.parameters == []
        assert meta.tags == []

    def test_with_parameters(self):
        meta = SkillMetadata(
            name="skill",
            parameters=[SkillParameter(name="x", type=ParameterType.INTEGER)],
        )
        assert len(meta.parameters) == 1
        assert meta.parameters[0].name == "x"


# ---------------------------------------------------------------------------
# Skill base class
# ---------------------------------------------------------------------------


class TestSkillBase:
    def test_execute_greet(self):
        GreetSkill = make_greet_skill_class()
        skill = GreetSkill()
        assert skill.execute(name="World") == "Hello, World!"

    def test_execute_add(self):
        AddSkill = make_add_skill_class()
        skill = AddSkill()
        assert skill.execute(a=3, b=4) == 7

    def test_repr(self):
        GreetSkill = make_greet_skill_class()
        skill = GreetSkill()
        assert "greet" in repr(skill)
        assert "0.1.0" in repr(skill)

    def test_cannot_instantiate_abstract_skill(self):
        with pytest.raises(TypeError):
            Skill()  # type: ignore[abstract]


# ---------------------------------------------------------------------------
# SkillRegistry
# ---------------------------------------------------------------------------


class TestSkillRegistry:
    def test_register_and_get(self):
        registry = SkillRegistry()
        GreetSkill = make_greet_skill_class()
        registry.register(GreetSkill)
        assert registry.get("greet") is GreetSkill

    def test_register_as_decorator(self):
        registry = SkillRegistry()
        GreetSkill = make_greet_skill_class()
        result = registry.register(GreetSkill)
        assert result is GreetSkill

    def test_register_duplicate_raises(self):
        registry = SkillRegistry()
        GreetSkill = make_greet_skill_class()
        registry.register(GreetSkill)
        with pytest.raises(ValueError, match="already registered"):
            registry.register(make_greet_skill_class())

    def test_get_unknown_raises(self):
        registry = SkillRegistry()
        with pytest.raises(KeyError):
            registry.get("nonexistent")

    def test_unregister(self):
        registry = SkillRegistry()
        GreetSkill = make_greet_skill_class()
        registry.register(GreetSkill)
        registry.unregister("greet")
        assert "greet" not in registry

    def test_unregister_unknown_raises(self):
        registry = SkillRegistry()
        with pytest.raises(KeyError):
            registry.unregister("nonexistent")

    def test_list_skills(self):
        registry = SkillRegistry()
        registry.register(make_greet_skill_class())
        registry.register(make_add_skill_class())
        assert registry.list_skills() == ["add", "greet"]

    def test_contains(self):
        registry = SkillRegistry()
        registry.register(make_greet_skill_class())
        assert "greet" in registry
        assert "unknown" not in registry

    def test_len(self):
        registry = SkillRegistry()
        assert len(registry) == 0
        registry.register(make_greet_skill_class())
        assert len(registry) == 1

    def test_iter(self):
        registry = SkillRegistry()
        GreetSkill = make_greet_skill_class()
        registry.register(GreetSkill)
        classes = list(registry)
        assert GreetSkill in classes
