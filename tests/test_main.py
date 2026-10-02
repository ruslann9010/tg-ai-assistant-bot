import os
import sys
import pytest
from unittest.mock import patch


def test_main_with_valid_token():
    test_token = "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ"  
    with patch.dict(os.environ, {"BOT_TOKEN": test_token}):
        with patch("aiogram.Bot"), patch("aiogram.Dispatcher"):
            import main
            assert main.BOT_TOKEN == test_token    


def test_main_missing_token_exits():
     with patch("os.getenv", return_value=None):
        breakpoint() 
        with pytest.raises(SystemExit) as exc_info:
            breakpoint() 
            import main
            breakpoint() 
        assert "Токен" in str(exc_info.value) or "токен" in str(exc_info.value).lower()
