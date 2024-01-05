#!/usr/bin/env python
# coding: utf-8

from tests.integration.integration_test_case import IntegrationTestCase
from hooks_toolkit.set_hook import create_hook_payload
from xrpl.models.transactions import SetHookFlag

from xrpl.models.transactions.set_hook import Hook
from xrpl.models.requests import LedgerEntry
from xrpl.models.requests.ledger_entry import (
    Hook as LeHook,
    HookDefinition as LeHookDefinition,
)

from hooks_toolkit.set_hook import set_hooks_v3
from hooks_toolkit.types import SetHookParams


class TestMockClient(IntegrationTestCase):
    def test_set_hook_create(cls):
        with cls.context.client as _:
            hook = create_hook_payload(
                SetHookParams(
                    version=0,
                    create_file="base",
                    namespace="base",
                    flags=[SetHookFlag.HSF_OVERRIDE],
                    hook_on_array=["Payment"],
                )
            )

            set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])

            le_hook_req = LedgerEntry(
                hook=LeHook(account=cls.context.hook1.classic_address)
            )
            result = cls.context.client.request(le_hook_req).result
            le_hook = result["node"]

            cls.assertEqual(
                le_hook["Hooks"][0]["Hook"]["HookHash"],
                "A5663784D04ED1B4408C6B97193464D27C9C3334AAF8BBB4FA5EB8E557FC4A2C",
            )

            le_hook_def_req = LedgerEntry(
                hook_definition=le_hook["Hooks"][0]["Hook"]["HookHash"]
            )

            le_hook_def_res = cls.context.client.request(le_hook_def_req).result
            cls.assertEqual(
                le_hook_def_res["node"]["HookNamespace"],
                "CAE662172FD450BB0CD710A769079C05BFC5D8E35EFA6576EDC7D0377AFDD4A2",
            )

    def test_set_hook_install(cls):
        with cls.context.client as _:
            hook = create_hook_payload(
                SetHookParams(
                    hook_hash="A5663784D04ED1B4408C6B97193464D27C9C3334AAF8BBB4FA5EB8E557FC4A2C",
                    namespace="base",
                    flags=[SetHookFlag.HSF_OVERRIDE],
                    hook_on_array=["Payment"],
                )
            )

            set_hooks_v3(cls.context.client, cls.context.hook2.seed, [hook])

            le_hook_req = LedgerEntry(
                hook=LeHook(account=cls.context.hook2.classic_address)
            )
            result = cls.context.client.request(le_hook_req).result
            le_hook = result["node"]

            cls.assertEqual(
                le_hook["Hooks"][0]["Hook"]["HookHash"],
                "A5663784D04ED1B4408C6B97193464D27C9C3334AAF8BBB4FA5EB8E557FC4A2C",
            )

            le_hook_def_req = LedgerEntry(
                hook_definition=le_hook["Hooks"][0]["Hook"]["HookHash"]
            )

            le_hook_def_res = cls.context.client.request(le_hook_def_req).result
            cls.assertEqual(
                le_hook_def_res["node"]["HookNamespace"],
                "CAE662172FD450BB0CD710A769079C05BFC5D8E35EFA6576EDC7D0377AFDD4A2",
            )

    def test_set_hook_update(cls):
        with cls.context.client as _:
            hook = create_hook_payload(
                SetHookParams(
                    namespace="base1",
                )
            )

            set_hooks_v3(cls.context.client, cls.context.hook2.seed, [hook])

            le_hook_req = LedgerEntry(
                hook=LeHook(account=cls.context.hook2.classic_address)
            )
            result = cls.context.client.request(le_hook_req).result
            le_hook = result["node"]

            cls.assertEqual(
                le_hook["Hooks"][0]["Hook"]["HookHash"],
                "A5663784D04ED1B4408C6B97193464D27C9C3334AAF8BBB4FA5EB8E557FC4A2C",
            )

            le_hook_def_req = LedgerEntry(
                hook_definition=le_hook["Hooks"][0]["Hook"]["HookHash"]
            )

            le_hook_def_res = cls.context.client.request(le_hook_def_req).result
            cls.assertEqual(
                le_hook_def_res["node"]["HookNamespace"],
                "CAE662172FD450BB0CD710A769079C05BFC5D8E35EFA6576EDC7D0377AFDD4A2",
            )

    def test_set_hook_delete(cls):
        with cls.context.client as _:
            hook = Hook(**{"create_code": "", "flags": [SetHookFlag.HSF_OVERRIDE]})

            set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])

            le_hook_req = LedgerEntry(
                hook=LeHook(account=cls.context.hook1.classic_address)
            )
            result = cls.context.client.request(le_hook_req).result
            cls.assertEqual(
                result["error"],
                "entryNotFound",
            )

    def test_set_hook_delete_ns(cls):
        with cls.context.client as _:
            hook = create_hook_payload(
                SetHookParams(namespace="base", flags=[SetHookFlag.HSF_NS_DELETE])
            )

            set_hooks_v3(cls.context.client, cls.context.hook2.seed, [hook])

            le_hook_req = LedgerEntry(
                hook=LeHook(account=cls.context.hook2.classic_address)
            )
            result = cls.context.client.request(le_hook_req).result
            le_hook = result["node"]

            cls.assertEqual(
                le_hook["Hooks"][0]["Hook"]["HookHash"],
                "A5663784D04ED1B4408C6B97193464D27C9C3334AAF8BBB4FA5EB8E557FC4A2C",
            )

            le_hook_def_req = LedgerEntry(
                hook_definition=le_hook["Hooks"][0]["Hook"]["HookHash"]
            )

            le_hook_def_res = cls.context.client.request(le_hook_def_req).result
            cls.assertEqual(
                le_hook_def_res["node"]["HookNamespace"],
                "CAE662172FD450BB0CD710A769079C05BFC5D8E35EFA6576EDC7D0377AFDD4A2",
            )
