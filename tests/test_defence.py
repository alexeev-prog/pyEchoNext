# tests/test_defence.py
import pytest

from pyechonext.security.defence import CSRFTokenManager


class TestCSRFTokenManager:
    @pytest.fixture
    def manager(self):
        return CSRFTokenManager()

    def test_generate_validate(self, manager):
        session_id = "session123"
        token = manager.generate_token(session_id)
        assert manager.validate_token(session_id, token) is True
        assert manager.validate_token(session_id, "wrong_token") is False

    def test_revoke(self, manager):
        session_id = "session456"
        token = manager.generate_token(session_id)
        manager.revoke_token(session_id)
        assert manager.validate_token(session_id, token) is False

    def test_different_sessions(self, manager):
        token1 = manager.generate_token("user1")
        token2 = manager.generate_token("user2")
        assert token1 != token2
        assert manager.validate_token("user1", token2) is False
