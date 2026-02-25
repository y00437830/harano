package com.harano.skill;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

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
    public Skill getSkill(@PathVariable String id) {
        return skillService.findById(id);
    }

    @PostMapping
    public ResponseEntity<Skill> createSkill(@RequestBody Skill skill) {
        return ResponseEntity.status(HttpStatus.CREATED).body(skillService.register(skill));
    }

    @PutMapping("/{id}")
    public Skill updateSkill(@PathVariable String id, @RequestBody Skill skill) {
        return skillService.update(id, skill);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteSkill(@PathVariable String id) {
        skillService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
