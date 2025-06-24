from app.main import compute_pews

def test_pews_score_low():
    score = compute_pews(130, 99.0, 36.8)
    assert score == 0

def test_pews_score_medium():
    score = compute_pews(170, 93.0, 38.2)
    assert score >= 2

def test_pews_score_high():
    score = compute_pews(190, 85.0, 39.6)
    assert score >= 4
