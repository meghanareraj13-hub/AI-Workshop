import os
import pytest
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, os.path.abspath("campusai"))

from config import (
    get_gemini_api_key,
    APP_TITLE,
    APP_SUBTITLE,
    SYSTEM_INSTRUCTION,
    SUGGESTED_QUESTIONS,
    WELCOME_MESSAGE,
)
from gemini_service import (
    get_gemini_client,
    format_chat_history,
    generate_response,
    GeminiServiceError,
)


class TestConfig:
    def test_constants_defined(self):
        assert APP_TITLE == "CampusAI"
        assert "College" in APP_SUBTITLE
        assert len(SUGGESTED_QUESTIONS) == 6
        assert "CampusAI" in WELCOME_MESSAGE
        assert "faculty" in SYSTEM_INSTRUCTION.lower()

    def test_get_gemini_api_key_env_var(self, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "test-secret-key-123")
        assert get_gemini_api_key() == "test-secret-key-123"

    def test_get_gemini_api_key_placeholder(self, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "your_gemini_api_key_here")
        assert get_gemini_api_key() is None

    def test_get_gemini_api_key_missing(self, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        # Assuming no streamlit secrets in test environment
        assert get_gemini_api_key() is None


class TestGeminiService:
    def test_get_gemini_client_missing_key(self):
        with pytest.raises(GeminiServiceError) as exc_info:
            get_gemini_client(None)
        assert "API key is missing" in str(exc_info.value)

        with pytest.raises(GeminiServiceError):
            get_gemini_client("   ")

    def test_get_gemini_client_valid_key(self):
        client = get_gemini_client("valid_mock_api_key")
        assert client is not None

    def test_format_chat_history(self):
        messages = [
            {"role": "user", "content": "How do I build a resume?"},
            {"role": "assistant", "content": "Focus on projects and skills."},
            {"role": "user", "content": ""},  # empty content ignored
        ]
        formatted = format_chat_history(messages)
        assert len(formatted) == 2
        assert formatted[0].role == "user"
        assert formatted[0].parts[0].text == "How do I build a resume?"
        assert formatted[1].role == "model"
        assert formatted[1].parts[0].text == "Focus on projects and skills."

    def test_generate_response_empty_message(self):
        with pytest.raises(GeminiServiceError) as exc_info:
            generate_response("some-key", "   ")
        assert "cannot be empty" in str(exc_info.value)

    @patch("gemini_service.get_gemini_client")
    def test_generate_response_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Here are the top placement preparation tips..."
        mock_client.models.generate_content.return_value = mock_response
        mock_get_client.return_value = mock_client

        reply = generate_response(
            api_key="mock_key",
            user_message="How to prepare for placements?",
            chat_history=[{"role": "user", "content": "Hi"}],
        )

        assert reply == "Here are the top placement preparation tips..."
        mock_client.models.generate_content.assert_called_once()
        call_kwargs = mock_client.models.generate_content.call_args.kwargs
        assert len(call_kwargs["contents"]) == 2  # 1 history + 1 current message

    @patch("gemini_service.get_gemini_client")
    def test_generate_response_api_error_handling(self, mock_get_client):
        from google.genai.errors import APIError

        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = APIError(
            400,
            {"error": {"message": "API_KEY_INVALID: Key not valid"}}
        )
        mock_get_client.return_value = mock_client

        with pytest.raises(GeminiServiceError) as exc_info:
            generate_response(
                api_key="bad_key",
                user_message="Hello",
            )
        assert "invalid" in str(exc_info.value).lower()
