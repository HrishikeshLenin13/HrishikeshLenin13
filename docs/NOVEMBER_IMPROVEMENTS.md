# Link validation

HTML anchor href attributes now receive the existing repository-bound path and Markdown/SVG fragment validation. This complements inline Markdown links, reference links and image sources. No network requests are added.

HTML attributes are parsed with the standard HTML parser, so entities and unquoted URLs work and data-href attributes are not mistaken for links.
