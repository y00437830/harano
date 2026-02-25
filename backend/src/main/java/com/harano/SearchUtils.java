package com.harano;

import java.util.Collection;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.stream.Collectors;

/** Shared search utilities for {@link TextSearchable} entities. */
public final class SearchUtils {

    private SearchUtils() {}

    /**
     * Returns all items whose name, description, or any tag contains the given
     * query string (case-insensitive), sorted by {@link TextSearchable#getId()}.
     */
    public static <T extends TextSearchable> List<T> search(Collection<T> items, String query) {
        String q = query.toLowerCase(Locale.ROOT);
        return items.stream()
                .filter(s -> s.getName().toLowerCase(Locale.ROOT).contains(q)
                        || s.getDescription().toLowerCase(Locale.ROOT).contains(q)
                        || s.getTags().stream().anyMatch(t -> t.toLowerCase(Locale.ROOT).contains(q)))
                .sorted(Comparator.comparing(TextSearchable::getId))
                .collect(Collectors.toList());
    }
}
