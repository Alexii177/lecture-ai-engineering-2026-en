from app import retrieval


def test_neighbors_stay_in_document_and_are_unique(monkeypatch):
    pages = [
        {
            "page_id": f"{doc}-p{number:03d}",
            "document_id": doc,
            "page": number,
            "content": f"{doc} page {number}",
            "citation": f"{doc}, page {number}",
        }
        for doc in ("doc-a", "doc-b")
        for number in (1, 2, 3, 4)
    ]
    hits = [dict(pages[1], distance=0.1), dict(pages[2], distance=0.2)]
    monkeypatch.setattr(retrieval, "search", lambda query: hits)
    monkeypatch.setattr(retrieval, "load_pages", lambda: pages)

    results = retrieval.search_with_neighbors("example")
    ids = [page["page_id"] for page in results]

    assert results[:2] == hits
    assert len(ids) == len(set(ids)) == 4
    assert set(ids) == {f"doc-a-p{n:03d}" for n in (1, 2, 3, 4)}
    assert all(page["content"] and page["citation"] for page in results)


def test_no_hits_returns_no_pages(monkeypatch):
    monkeypatch.setattr(retrieval, "search", lambda query: [])
    monkeypatch.setattr(retrieval, "load_pages", lambda: [])
    assert retrieval.search_with_neighbors("missing") == []
