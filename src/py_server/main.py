"""Основной файл запуска MCP-прокси сервера."""

import asyncio
import logging
import os
import sys
import argparse
from pathlib import Path

from dotenv import load_dotenv

from py_server.config import get_config
from py_server.http_server import run_http_server
from py_server.stdio_server import run_stdio_server


def setup_logging(level: str = "INFO"):
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
    )


def create_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("mode", nargs="?", default="stdio", choices=["stdio", "http"])
    parser.add_argument("--env-file", type=str)
    parser.add_argument("--log-level", type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    parser.add_argument("--host", type=str)
    parser.add_argument("--port", type=int)

    parser.add_argument("--onec-url", type=str)
    parser.add_argument("--onec-username", type=str)
    parser.add_argument("--onec-password", type=str)
    parser.add_argument("--onec-service-root", type=str)

    parser.add_argument("--auth-mode", type=str, choices=["none", "oauth2"])
    parser.add_argument("--public-url", type=str)

    return parser


async def main(env_file=None, mode="stdio"):
    """Основная функция запуска."""

    # -----------------------------
    # CLI args
    # -----------------------------
    parser = create_parser()

    if env_file is None:
        args = parser.parse_args()
    else:
        args = argparse.Namespace(
            mode=mode,
            env_file=str(env_file),

            onec_url=None,
            onec_username=None,
            onec_password=None,
            onec_service_root=None,

            log_level=None,
            host=None,
            port=None,

            auth_mode=None,
            public_url=None,
        )

    # -----------------------------
    # env loading
    # -----------------------------
    if args.env_file:
        env_path = Path(args.env_file)
        if env_path.exists():
            load_dotenv(env_path)

    # -----------------------------
    # overrides
    # -----------------------------
    if args.onec_url:
        os.environ["MCP_ONEC_URL"] = args.onec_url

    if args.onec_username:
        os.environ["MCP_ONEC_USERNAME"] = args.onec_username

    if args.onec_password:
        os.environ["MCP_ONEC_PASSWORD"] = args.onec_password

    if args.onec_service_root:
        os.environ["MCP_ONEC_SERVICE_ROOT"] = args.onec_service_root

    if args.host:
        os.environ["MCP_HOST"] = args.host

    if args.port:
        os.environ["MCP_PORT"] = str(args.port)

    if args.log_level:
        os.environ["MCP_LOG_LEVEL"] = args.log_level

    if args.auth_mode:
        os.environ["MCP_AUTH_MODE"] = args.auth_mode

    if args.public_url:
        os.environ["MCP_PUBLIC_URL"] = args.public_url

    # -----------------------------
    # config
    # -----------------------------
    config = get_config(args.env_file)

    setup_logging(config.log_level)

    logger = logging.getLogger(__name__)

    logger.info(f"mode={args.mode}")
    logger.info(f"onec={config.onec_url}")

    # -----------------------------
    # run
    # -----------------------------
    if args.mode == "stdio":
        await run_stdio_server(config)

    elif args.mode == "http":
        await run_http_server(config)

    else:
        raise RuntimeError(f"Unknown mode: {args.mode}")


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    asyncio.run(main(env_file=args.env_file, mode=args.mode))