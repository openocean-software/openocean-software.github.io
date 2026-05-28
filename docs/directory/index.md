---
render_macros: true
---

# Project Directory

The OpenOcean.Software Project Directory is a curated catalog of open-source
software for marine robotics. Browse projects below, or
[submit your own](../directory-submit/index.md).

!!! tip "Can't find what you need?"
    If you're looking for something that isn't listed here, check our
    [community forum](https://forum.oceansoft.org) or
    [open an issue](https://github.com/openocean-software/openocean-software.github.io/issues)
    to let us know what's missing.

<!-- FUTURE HOOK: client-side filtering -->
<!-- When ready to add JS filtering, add filter controls here and tag each -->
<!-- card with data-* attributes matching the YAML fields. See plan Section 9. -->

{% for project in projects %}

---

<div class="project-card" markdown>

### {{ project.name }} {% if project.status == "active" %} :material-check-circle:{ .status-active title="Active" } {% elif project.status == "maintained" %} :material-shield-check:{ .status-maintained title="Maintained" } {% elif project.status == "archived" %} :material-archive:{ .status-archived title="Archived" } {% elif project.status == "experimental" %} :material-flask:{ .status-experimental title="Experimental" } {% endif %}

{{ project.description }}

**Category:** {{ project.category | replace("-", " ") | title }}
{% if project.middleware %} · **Middleware:** {{ project.middleware | join(", ") }}{% endif %}
{% if project.languages %} · **Languages:** {{ project.languages | join(", ") }}{% endif %}
 · **License:** `{{ project.license }}`
{% if project.maintainer_org %} · **Maintainer:** {{ project.maintainer_org }}{% endif %}

{% if project.tags %}
{% for tag in project.tags %}<span class="project-tag">{{ tag }}</span> {% endfor %}
{% endif %}

[:material-source-repository: Repository]({{ project.repo_url }}){ .md-button }
{% if project.website_url %}[:material-web: Website]({{ project.website_url }}){ .md-button }{% endif %}
{% if project.docs_url %}[:material-book-open-variant: Docs]({{ project.docs_url }}){ .md-button }{% endif %}
{% if project.openssf_scorecard %}[:material-shield-search: OpenSSF Scorecard]({{ project.openssf_scorecard }}){ .md-button }{% endif %}

</div>

{% endfor %}

---

*Know a project that should be listed here?
[Submit it →](../directory-submit/index.md)*
