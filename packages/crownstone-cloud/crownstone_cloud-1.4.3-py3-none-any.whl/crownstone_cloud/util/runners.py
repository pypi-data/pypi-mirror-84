"""Functions to run async functions from sync context"""
from typing import Coroutine
import asyncio


def run_async(coroutine: Coroutine):
    """Run an async function from sync context."""
    return asyncio.get_event_loop().run_until_complete(coroutine)
