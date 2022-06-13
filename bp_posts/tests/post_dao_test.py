import pytest

from bp_posts.dao.post import Post
from bp_posts.dao.post_dao import PostDao

def check_fields(post):

    fields = ["poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"]

    for field in fields:
        assert hasattr(post, field), f"Нет поля {field}"


class TestPostsDAO:

    @pytest.fixture
    def post_dao(self):

        post_dao_instance = PostDao("post_mock.json")
        return post_dao_instance

    ### Функция получения всех

    def test_get_all_types(self, post_dao):

        posts = post_dao.get_all()
        assert type(posts) == list, "Incorrect type for result"

        post = post_dao.get_all()[0]
        assert type(post) == Post, "Incorrect type for result single item"

    def test_get_all_fields(self, post_dao):
        posts = post_dao.get_all()
        post = post_dao.get_all()[0]
        check_fields(post)

    def test_get_all_correct_ids(self, post_dao):
        posts = post_dao.get_all()
        correct_pks = {1, 2, 3}
        pks = set([post.pk for post in posts])
        assert pks == correct_pks, "Не совпадают полученные id"


    ### Функция получения для одного пк

    def test_get_by_pk_types(self, post_dao):

        post = post_dao.get_by_pk(1)

        assert type(post) == Post, "Incorrect type for result single item"

    def test_get_by_pk_fields(self, post_dao):
        post = post_dao.get_by_pk(1)
        check_fields(post)

    def test_get_by_pk_none(self, post_dao):
        post = post_dao.get_by_pk(999)
        assert post is None, "Should be None for non existent pk"

    @pytest.mark.parametrize("pk", [1, 2, 3])
    def test_get_by_pk_correct_id(self, post_dao, pk):
        post = post_dao.get_by_pk(pk)
        assert post.pk == pk, f"Incorrect post.pk for requesten post with pk = {pk}"

    ###Фукция получения псстов по вхождению строки

    def test_search_in_content_types(self, post_dao):
        posts = post_dao.search_in_content("ага")
        assert type(posts) == list, "Incorrect type for result"

        post = post_dao.get_all()[0]
        assert type(post) == Post, "Incorrect type for result single item"

    def test_search_in_content_fields(self, post_dao):
        posts = post_dao.search_in_content("ага")
        post = post_dao.get_all()[0]
        check_fields(post)

    def test_search_in_content_not_found(self, post_dao):
        posts = post_dao.search_in_content("999000")
        assert posts == [], "Should be [] for not substring not found"

    @pytest.mark.parametrize("s, expected_pks", [
        ("Ага", {1}),
        ("Вышел", {2}),
        ("на", {1, 2, 3})

    ])
    def test_search_in_content_results(self, post_dao, s, expected_pks):
        posts = post_dao.search_in_content(s)
        pks = set([post.pk for post in posts])
        assert pks == expected_pks, f"Incorrect results searching for {s}"

    ###Фукция получения псстов по имени автора


    def test_get_by_poster_types(self, post_dao):
        posts = post_dao.get_by_poster("leo")
        assert type(posts) == list, "Incorrect type for result"

        post = post_dao.get_all()[0]
        assert type(post) == Post, "Incorrect type for result single item"


    def test_get_by_poster_fields(self, post_dao):
        posts = post_dao.get_by_poster("leo")
        post = post_dao.get_all()[0]
        check_fields(post)

    def test_get_by_poster_none(self, post_dao):
        posts = post_dao.get_by_poster("9999999999999999")
        assert posts == [], "Should be None for non existent poster"

    @pytest.mark.parametrize("s, expected_names", [
        ("leo", {1}),
        ("johnny", {2}),
        ("hank", {3})

    ])
    def test_get_by_poster_results(self, post_dao, s, expected_names):
        posts = post_dao.get_by_poster(s)
        names = set([post.pk for post in posts])
        assert names == expected_names, f"Incorrect results searching for {s}"