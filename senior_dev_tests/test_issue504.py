from imdb import Cinemagoer

def test_same_result():
    ia = Cinemagoer()
    aa=ia.search_movie('Shang-Chi and the Legend of the Ten Rings')
    assert aa[5]['kind'] == ia.get_movie('19829610')['kind']

def test_kind():
    ia = Cinemagoer()
    aa=ia.search_movie('Shang-Chi and the Legend of the Ten Rings')
    assert aa[5]['kind'] == "podcast episode"