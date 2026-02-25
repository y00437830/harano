package com.harano.skill;

import java.util.ArrayList;
import java.util.List;

/** Metadata that describes a Skill. */
public class Skill {

    private String id;
    private String name;
    private String version;
    private String description;
    private List<SkillParameter> parameters = new ArrayList<>();
    private List<String> tags = new ArrayList<>();

    public Skill() {}

    public Skill(String id, String name, String version, String description) {
        this.id = id;
        this.name = name;
        this.version = version;
        this.description = description;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getVersion() { return version; }
    public void setVersion(String version) { this.version = version; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public List<SkillParameter> getParameters() { return parameters; }
    public void setParameters(List<SkillParameter> parameters) { this.parameters = parameters; }

    public List<String> getTags() { return tags; }
    public void setTags(List<String> tags) { this.tags = tags; }
}
