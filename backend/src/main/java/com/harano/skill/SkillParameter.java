package com.harano.skill;

import java.util.ArrayList;
import java.util.List;

/** Describes a single input parameter accepted by a {@link Skill}. */
public class SkillParameter {

    private String name;
    private String type;
    private String description;
    private boolean required;
    private Object defaultValue;

    public SkillParameter() {}

    public SkillParameter(String name, String type, String description, boolean required) {
        this.name = name;
        this.type = type;
        this.description = description;
        this.required = required;
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getType() { return type; }
    public void setType(String type) { this.type = type; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public boolean isRequired() { return required; }
    public void setRequired(boolean required) { this.required = required; }

    public Object getDefaultValue() { return defaultValue; }
    public void setDefaultValue(Object defaultValue) { this.defaultValue = defaultValue; }
}
