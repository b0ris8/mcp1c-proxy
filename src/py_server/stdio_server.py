"""Stdio сервер для MCP."""

import asyncio
import logging
import traceback

import mcp.server.stdio

from .mcp_server import MCPProxy
from .config import Config


logger = logging.getLogger(__name__)

async def run_stdio_server(config: Config):
    """Запуск stdio сервера."""
    logger.info("Запуск MCP сервера в режиме stdio")
    mcp_proxy = MCPProxy(config)
    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            try:
                await mcp_proxy.server.run(
                    read_stream,
                    write_stream,
                    mcp_proxy.get_initialization_options()
                )
            except* Exception as eg:
                logger.error("TaskGroup ошибка: %s", repr(eg))
                for i, ex in enumerate(eg.exceptions, start=1):
                    logger.error(
                        "SUBERROR %s:\n%s", i,
                        "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
                    )
                raise
    except Exception:
        logger.error("STDIO ошибка:\n%s", traceback.format_exc())
        raise