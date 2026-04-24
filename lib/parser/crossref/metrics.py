def extract_metrics(data):
    return {
        "citation_count": int(data.get("is-referenced-by-count")),
        "reference_count": int(data.get("reference-count")),
        "altmetric_score": None,
        "mendeley_readers": None,
        "tweets_count": None,
        "news_count": None,
        "blog_count": None,
        "policy_count": None,
        "patent_count": None,
        "source": "crossref",
}