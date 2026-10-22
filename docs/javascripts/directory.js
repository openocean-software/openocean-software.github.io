// Filter chips and search for the member project directory (projects/).
//
// Cards carry data-filter (one of the chip keys) and data-search (lowercase
// name, category, summary and tags) from overrides/partials/project-card.html.
// Without JS every card stays visible, so the page still works as a list.
// A ?q= query string (the home page search form) pre-fills the search box.

function setupDirectory() {
  const root = document.querySelector("[data-oo-directory]");
  if (!root) return;

  const search = root.querySelector("[data-oo-search]");
  const filters = Array.from(root.querySelectorAll("[data-oo-filter]"));
  const cards = Array.from(root.querySelectorAll(".oo-card"));
  const count = root.querySelector("[data-oo-count]");
  const empty = root.querySelector("[data-oo-empty]");
  let active = "all";

  function apply() {
    const query = search.value.trim().toLowerCase();
    let shown = 0;
    for (const card of cards) {
      const matchesFilter = active === "all" || card.dataset.filter === active;
      const matchesQuery = !query || card.dataset.search.includes(query);
      card.hidden = !(matchesFilter && matchesQuery);
      if (!card.hidden) shown += 1;
    }
    count.textContent = `Showing ${shown} of ${cards.length}`;
    empty.hidden = shown !== 0;
  }

  for (const button of filters) {
    button.addEventListener("click", () => {
      active = button.dataset.ooFilter;
      for (const b of filters) b.setAttribute("aria-pressed", String(b === button));
      apply();
    });
  }
  search.addEventListener("input", apply);

  const q = new URLSearchParams(window.location.search).get("q");
  if (q) {
    search.value = q;
    apply();
  }
}

// Material's instant navigation swaps pages without a reload and announces
// each one on document$; fall back to DOMContentLoaded when it is off.
if (typeof document$ !== "undefined") {
  document$.subscribe(setupDirectory);
} else {
  document.addEventListener("DOMContentLoaded", setupDirectory);
}
