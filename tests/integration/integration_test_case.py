#!/usr/bin/env python
# coding: utf-8

from unittest import TestCase

from hooks_toolkit.libs.xahau_helpers.server_url import server_url
from hooks_toolkit.libs.xahau_helpers.setup import (
    setup_client,
    XahauIntegrationTestContext,
    teardown_client,
)


class IntegrationTestCase(TestCase):
    context: XahauIntegrationTestContext

    @classmethod
    def setUpClass(cls):
        # DA: TODO FIX AWAIT
        print("setUpClass")
        cls.context = setup_client(server_url)

    @classmethod
    def tearDownClass(cls):
        # DA: TODO FIX AWAIT
        print("tearDownClass")
        teardown_client(cls.context)
