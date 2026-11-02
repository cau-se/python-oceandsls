#  Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""Helpers to exercise a language server process end-to-end over stdio (used by the DSL test suites).

Running the real server process catches problems unit tests cannot see, e.g. output written to stdout, which corrupts
the JSON-RPC stream when the server is started with ``start_io()``.
"""

from __future__ import annotations

import asyncio
import tempfile
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

from lsprotocol.types import (
    ClientCapabilities, CompletionParams, Diagnostic, DidOpenTextDocumentParams, InitializeParams, InitializedParams,
    Position, PublishDiagnosticsParams, SemanticTokensParams, TEXT_DOCUMENT_PUBLISH_DIAGNOSTICS, TextDocumentIdentifier,
    TextDocumentItem,
)
from pygls.client import aio_readline
from pygls.lsp.client import BaseLanguageClient


@dataclass
class SessionResult:
    """What a server returned during :func:`run_lsp_session`."""
    server_name: Optional[str] = None
    diagnostics: List[Diagnostic] = field(default_factory=list)
    completions: Dict[Tuple[int, int], List[str]] = field(default_factory=dict)
    semantic_tokens: List[int] = field(default_factory=list)


async def lsp_session(
        command: Sequence[str], uri: str, text: str, language_id: str,
        completion_positions: Sequence[Tuple[int, int]] = (), cwd: Optional[str] = None, timeout: float = 60,
        env: Optional[Dict[str, str]] = None,
) -> SessionResult:
    """Start ``command``, open one document, request completions and semantic tokens and shut the server down."""
    client = BaseLanguageClient("odsllib-test-client", "1.0")
    result = SessionResult()
    diagnostics_received = asyncio.Event()

    @client.feature(TEXT_DOCUMENT_PUBLISH_DIAGNOSTICS)
    def _diagnostics(params: PublishDiagnosticsParams):
        if params.uri == uri:
            result.diagnostics = list(params.diagnostics)
            diagnostics_received.set()

    # Started like BaseLanguageClient.start_io(), but stderr goes to a file: pygls pipes stderr without reading it,
    # which blocks a server that logs more than the pipe buffer holds. The log is reported if the server dies.
    stderr = tempfile.TemporaryFile()
    process = await asyncio.create_subprocess_exec(
        *command, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=stderr, cwd=cwd, env=env,
    )
    client.protocol.connection_made(process.stdin)
    client._server = process
    client._async_tasks.append(
        asyncio.create_task(aio_readline(client._stop_event, process.stdout, client.protocol.data_received))
    )

    async def wait(awaitable):
        """Await a response, but fail immediately with the server's stderr if the server process exits."""
        task = asyncio.ensure_future(awaitable)
        exited = asyncio.ensure_future(process.wait())
        done, _ = await asyncio.wait({task, exited}, timeout=timeout, return_when=asyncio.FIRST_COMPLETED)
        if task in done:
            exited.cancel()
            return task.result()
        task.cancel()
        exited.cancel()
        stderr.seek(0)
        log = stderr.read().decode(errors="replace")[-4000:]
        reason = f"exited with code {process.returncode}" if done else f"did not answer within {timeout}s"
        raise RuntimeError(f"Language server {reason}. stderr:\n{log}")

    try:
        init = await wait(client.initialize_async(
            InitializeParams(process_id=None, root_uri=None, capabilities=ClientCapabilities())))
        result.server_name = init.server_info.name if init.server_info else None
        client.initialized(InitializedParams())
        client.text_document_did_open(DidOpenTextDocumentParams(
            text_document=TextDocumentItem(uri=uri, language_id=language_id, version=1, text=text)))
        await wait(diagnostics_received.wait())

        for line, character in completion_positions:
            completion = await wait(client.text_document_completion_async(CompletionParams(
                text_document=TextDocumentIdentifier(uri=uri), position=Position(line=line, character=character))))
            items = completion.items if hasattr(completion, "items") else (completion or [])
            result.completions[(line, character)] = [item.label for item in items]

        tokens = await wait(client.text_document_semantic_tokens_full_async(
            SemanticTokensParams(text_document=TextDocumentIdentifier(uri=uri))))
        result.semantic_tokens = list(tokens.data) if tokens else []

        await wait(client.shutdown_async(None))
        client.exit(None)
    finally:
        await client.stop()
        stderr.close()
    return result


def subprocess_env(*extra_paths: str) -> Dict[str, str]:
    """Environment for a server subprocess that sees the same modules as the current interpreter."""
    import os
    import sys
    paths = [os.path.abspath(p) for p in (*extra_paths, *sys.path) if p]
    return {**os.environ, "PYTHONPATH": os.pathsep.join(dict.fromkeys(paths))}


def run_lsp_session(*args, **kwargs) -> SessionResult:
    """Synchronous wrapper around :func:`lsp_session`."""
    return asyncio.run(lsp_session(*args, **kwargs))
