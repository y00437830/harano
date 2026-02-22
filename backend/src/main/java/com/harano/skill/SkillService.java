package com.harano.skill;

import org.springframework.stereotype.Service;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

/** In-memory registry for {@link Skill} instances. */
@Service
public class SkillService {

    private final Map<String, Skill> skills = new ConcurrentHashMap<>();

    public Skill register(Skill skill) {
        if (skills.containsKey(skill.getId())) {
            throw new IllegalArgumentException("A skill with id '" + skill.getId() + "' is already registered.");
        }
        skills.put(skill.getId(), skill);
        return skill;
    }

    public Skill update(String id, Skill updated) {
        if (!skills.containsKey(id)) {
            throw new NoSuchElementException("Skill not found: " + id);
        }
        updated.setId(id);
        skills.put(id, updated);
        return updated;
    }

    public void delete(String id) {
        if (!skills.containsKey(id)) {
            throw new NoSuchElementException("Skill not found: " + id);
        }
        skills.remove(id);
    }

    public Skill findById(String id) {
        return Optional.ofNullable(skills.get(id))
                .orElseThrow(() -> new NoSuchElementException("Skill not found: " + id));
    }

    public List<Skill> findAll() {
        return skills.values().stream()
                .sorted(Comparator.comparing(Skill::getId))
                .collect(Collectors.toList());
    }

    public List<Skill> search(String query) {
        String q = query.toLowerCase(Locale.ROOT);
        return skills.values().stream()
                .filter(s -> s.getName().toLowerCase(Locale.ROOT).contains(q)
                        || s.getDescription().toLowerCase(Locale.ROOT).contains(q)
                        || s.getTags().stream().anyMatch(t -> t.toLowerCase(Locale.ROOT).contains(q)))
                .sorted(Comparator.comparing(Skill::getId))
                .collect(Collectors.toList());
    }
}
