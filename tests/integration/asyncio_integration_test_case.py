#!/usr/bin/env python
# coding: utf-8

import asyncio
from unittest import IsolatedAsyncioTestCase

from hooks_toolkit.libs.xrpl_helpers.server_url import server_url
from hooks_toolkit.libs.xrpl_helpers.setup import (
    XrplIntegrationTestContext,
)
from hooks_toolkit.libs.asyncio.xrpl_helpers.setup import setup_client, teardown_client


class AsyncioIntegrationTestCase(IsolatedAsyncioTestCase):
    context: XrplIntegrationTestContext

    @classmethod
    async def asyncSetUpClass(cls):
        cls.context = await setup_client(server_url)

    @classmethod
    async def asyncTearDownClass(cls):
        await teardown_client(cls.context)

    @classmethod
    def setUpClass(cls):
        asyncio.run(cls.asyncSetUpClass())

    @classmethod
    def tearDownClass(cls):
        asyncio.run(cls.asyncTearDownClass())
