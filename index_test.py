import index


def test_ngram():
    assert list(index.ngram("carotte", 3)) == ["car", "aro", "rot", "ott", "tte"]


def test_parse_ua():
    ngrams = index.parse_ua(r"(OperationsDashboard)-(?:Windows)-(\d+)\.(\d+)\.(\d+)")
    assert ngrams == set(
        list(index.ngram("OperationsDashboard", 3)) + list(index.ngram("Windows", 3))
    )
