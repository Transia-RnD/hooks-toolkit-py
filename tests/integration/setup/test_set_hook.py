#!/usr/bin/env python
# coding: utf-8

from tests.integration.integration_test_case import IntegrationTestCase
from hooks_toolkit.set_hook import create_hook_payload
from xrpl.models.transactions import SetHookFlag

# from xrpl.models.transactions.set_hook import Hook
from xrpl.models.requests import LedgerEntry
from xrpl.models.requests.ledger_entry import (
    Hook as LeHook,
    HookDefinition as LeHookDefinition,
)

from hooks_toolkit.set_hook import set_hooks_v3


class TestMockClient(IntegrationTestCase):
    def test_set_hook_create(cls):
        with cls.context.client as _:
            hook = create_hook_payload(
                0, "base", "base", [SetHookFlag.HSF_OVERRIDE], ["Payment"]
            )

            set_hooks_v3(cls.context.client, cls.context.alice.seed, [hook])

            le_hook_req = LedgerEntry(
                hook=LeHook(account=cls.context.alice.classic_address)
            )
            result = cls.context.client.request(le_hook_req).result
            le_hook = result["node"]

            cls.assertEqual(
                le_hook["Hooks"][0]["Hook"]["HookHash"],
                "77934E9067CC9311121627CB3C9AF3D9137D6008D308CC5F57D1BBFC27A1C5C1",
            )

            le_hook_def_req = LedgerEntry(
                hook_definition=le_hook["Hooks"][0]["Hook"]["HookHash"]
            )

            le_hook_def_res = cls.context.client.request(le_hook_def_req).result
            print(le_hook_def_res)

            cls.assertEqual(
                le_hook_def_res["node"]["HookNamespace"],
                "CAE662172FD450BB0CD710A769079C05BFC5D8E35EFA6576EDC7D0377AFDD4A2",
            )
