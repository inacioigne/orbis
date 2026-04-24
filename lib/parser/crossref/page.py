def parse_page_range(page):
    if not page:
        return (None, None)
    page = str(page).strip()
    if "-" in page:
        a, b = page.split("-", 1)
        return a.strip() or None, b.strip() or None
    return page, None