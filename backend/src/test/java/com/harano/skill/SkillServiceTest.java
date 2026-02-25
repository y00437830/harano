package com.harano.skill;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.NoSuchElementException;

import static org.junit.jupiter.api.Assertions.*;

class SkillServiceTest {

    private SkillService service;

    @BeforeEach
    void setUp() {
        service = new SkillService();
    }

    private Skill makeSkill(String id, String name) {
        Skill s = new Skill(id, name, "1.0.0", "A test skill");
        s.setTags(List.of("test"));
        return s;
    }

    @Test
    void register_and_findById() {
        Skill skill = makeSkill("greet", "Greet");
        service.register(skill);
        Skill found = service.findById("greet");
        assertEquals("greet", found.getId());
        assertEquals("Greet", found.getName());
    }

    @Test
    void register_duplicate_throws() {
        service.register(makeSkill("greet", "Greet"));
        assertThrows(IllegalArgumentException.class, () -> service.register(makeSkill("greet", "Greet2")));
    }

    @Test
    void findById_unknown_throws() {
        assertThrows(NoSuchElementException.class, () -> service.findById("nonexistent"));
    }

    @Test
    void findAll_sorted() {
        service.register(makeSkill("b", "B"));
        service.register(makeSkill("a", "A"));
        List<Skill> all = service.findAll();
        assertEquals(List.of("a", "b"), all.stream().map(Skill::getId).toList());
    }

    @Test
    void update() {
        service.register(makeSkill("greet", "Greet"));
        Skill updated = makeSkill("greet", "Greet Updated");
        service.update("greet", updated);
        assertEquals("Greet Updated", service.findById("greet").getName());
    }

    @Test
    void update_unknown_throws() {
        assertThrows(NoSuchElementException.class, () -> service.update("x", makeSkill("x", "X")));
    }

    @Test
    void delete() {
        service.register(makeSkill("greet", "Greet"));
        service.delete("greet");
        assertThrows(NoSuchElementException.class, () -> service.findById("greet"));
    }

    @Test
    void delete_unknown_throws() {
        assertThrows(NoSuchElementException.class, () -> service.delete("nonexistent"));
    }

    @Test
    void search_byName() {
        service.register(makeSkill("weather", "Weather Skill"));
        service.register(makeSkill("code", "Code Formatter"));
        List<Skill> results = service.search("weather");
        assertEquals(1, results.size());
        assertEquals("weather", results.get(0).getId());
    }

    @Test
    void search_byTag() {
        Skill s = makeSkill("s1", "S1");
        s.setTags(List.of("nlp", "ai"));
        service.register(s);
        Skill s2 = makeSkill("s2", "S2");
        s2.setTags(List.of("vision"));
        service.register(s2);
        assertEquals(1, service.search("nlp").size());
    }

    @Test
    void search_caseInsensitive() {
        service.register(makeSkill("weather", "Weather Skill"));
        assertEquals(1, service.search("WEATHER").size());
    }
}
