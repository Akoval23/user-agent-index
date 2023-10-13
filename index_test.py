import index


def test_ngram():
    assert list(index.ngram("carotte", 3)) == ["car", "aro", "rot", "ott", "tte"]


def test_parse_ua():
    ngrams = index.extract_term(r"(OperationsDashboard)-(?:Windows)-(\d+)\.(\d+)\.(\d+)")
    assert ngrams == [
        "OperationsDashboard",
        "Windows",
    ]
