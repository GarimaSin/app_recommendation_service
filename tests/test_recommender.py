from online.core.recommender import Recommender
def test_recommender_load():
    r = Recommender()
    assert hasattr(r,'recommend_by_vector')
