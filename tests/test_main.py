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


def test_main_missing_token_exits(caplog):
     import logging
     with patch("os.getenv", return_value=None):
        with pytest.raises(SystemExit) as exc_info:
            from main import main
            import asyncio
            asyncio.run(main())
     assert any(
     "Токен" in record.message or "токен" in record.message
     for record in caplog.records
     if record.levelno == logging.CRITICAL
    )
