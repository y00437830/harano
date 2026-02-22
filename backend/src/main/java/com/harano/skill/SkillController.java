package com.harano.skill;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.NoSuchElementException;

/** REST controller for managing Skills. */
@RestController
@RequestMapping("/api/skills")
@CrossOrigin(origins = "*")
public class SkillController {

    private final SkillService skillService;

    public SkillController(SkillService skillService) {
        this.skillService = skillService;
    }

    @GetMapping
    public List<Skill> listSkills(@RequestParam(required = false) String q) {
        if (q != null && !q.isBlank()) {
            return skillService.search(q);
        }
        return skillService.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Skill> getSkill(@PathVariable String id) {
        try {
            return ResponseEntity.ok(skillService.findById(id));
        } catch (NoSuchElementException e) {
            return ResponseEntity.notFound().build();
        }
    }

    @PostMapping
    public ResponseEntity<Skill> createSkill(@RequestBody Skill skill) {
        try {
            return ResponseEntity.status(HttpStatus.CREATED).body(skillService.register(skill));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.status(HttpStatus.CONFLICT).build();
        }
    }

    @PutMapping("/{id}")
    public ResponseEntity<Skill> updateSkill(@PathVariable String id, @RequestBody Skill skill) {
        try {
            return ResponseEntity.ok(skillService.update(id, skill));
        } catch (NoSuchElementException e) {
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteSkill(@PathVariable String id) {
        try {
            skillService.delete(id);
            return ResponseEntity.noContent().build();
        } catch (NoSuchElementException e) {
            return ResponseEntity.notFound().build();
        }
    }
}
