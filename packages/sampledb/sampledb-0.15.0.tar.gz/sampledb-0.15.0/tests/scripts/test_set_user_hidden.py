# coding: utf-8
"""

"""

import pytest
from sampledb import db
from sampledb.logic import users
import sampledb.__main__ as scripts


def test_set_hidden_yes(capsys):
    user_id = users.create_user("username", "example@fz-juelich.de", users.UserType.PERSON).id

    scripts.main([scripts.__file__, 'set_user_hidden', str(user_id), 'yes'])
    assert 'Success' in capsys.readouterr()[0]
    user = users.get_user(user_id)
    assert user.is_hidden


def test_set_hidden_no(capsys):
    user_id = users.create_user("username", "example@fz-juelich.de", users.UserType.PERSON).id
    user = users.get_user(user_id)
    user.is_hidden = True
    db.session.add(user)
    db.session.commit()

    scripts.main([scripts.__file__, 'set_user_hidden', str(user_id), 'no'])
    assert 'Success' in capsys.readouterr()[0]
    user = users.get_user(user_id)
    assert not user.is_hidden


def test_set_hidden_yes_no_change(capsys):
    user_id = users.create_user("username", "example@fz-juelich.de", users.UserType.PERSON).id
    user = users.get_user(user_id)
    user.is_hidden = True
    db.session.add(user)
    db.session.commit()

    scripts.main([scripts.__file__, 'set_user_hidden', str(user_id), 'yes'])
    assert 'Success' in capsys.readouterr()[0]
    user = users.get_user(user_id)
    assert user.is_hidden


def test_set_hidden_no_no_change(capsys):
    user_id = users.create_user("username", "example@fz-juelich.de", users.UserType.PERSON).id

    scripts.main([scripts.__file__, 'set_user_hidden', str(user_id), 'no'])
    assert 'Success' in capsys.readouterr()[0]
    user = users.get_user(user_id)
    assert not user.is_hidden


def test_set_hidden_missing_arguments(capsys):
    user_id = users.create_user("username", "example@fz-juelich.de", users.UserType.PERSON).id

    with pytest.raises(SystemExit) as exc_info:
        scripts.main([scripts.__file__, 'set_user_hidden', str(user_id)])
    assert exc_info.value != 0
    assert 'Usage' in capsys.readouterr()[0]
    user = users.get_user(user_id)
    assert not user.is_hidden


def test_set_hidden_invalid_user_id(capsys):
    with pytest.raises(SystemExit) as exc_info:
        scripts.main([scripts.__file__, 'set_user_hidden', '1', 'yes'])
    assert exc_info.value != 0
    assert 'Error' in capsys.readouterr()[1]


def test_set_hidden_invalid_argument(capsys):
    user_id = users.create_user("username", "example@fz-juelich.de", users.UserType.PERSON).id

    with pytest.raises(SystemExit) as exc_info:
        scripts.main([scripts.__file__, 'set_user_hidden', str(user_id), 'maybe'])
    assert exc_info.value != 0
    assert 'Usage' in capsys.readouterr()[0]
    user = users.get_user(user_id)
    assert not user.is_hidden
