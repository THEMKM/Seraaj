from app.db import init_db
from app.matching import compute_match_scores


def test_matching_empty_db():
    init_db()
    assert compute_match_scores() == 0
