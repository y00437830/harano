package com.harano;

import java.util.List;

/**
 * Common interface for entities that support full-text search by name,
 * description, and tags.
 */
public interface TextSearchable {
    String getId();
    String getName();
    String getDescription();
    List<String> getTags();
}
