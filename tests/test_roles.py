class FakeUser:

    def __init__(self, role):

        self.role = role


def test_admin_role():

    user = FakeUser("admin")

    assert user.role == "admin"


def test_moderator_role():

    user = FakeUser("moderator")

    assert user.role == "moderator"


def test_user_role():

    user = FakeUser("user")

    assert user.role == "user"