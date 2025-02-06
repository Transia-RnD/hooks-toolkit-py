#!/usr/bin/env python
# coding: utf-8

from tests.integration.integration_test_case import IntegrationTestCase
from hooks_toolkit.set_hook import create_hook_payload
from xahau.models.transactions import SetHookFlag, Invoke

from xahau.models.transactions.set_hook import Hook
from xahau.models.requests import LedgerEntry
from xahau.models.requests.ledger_entry import (
    Hook as LeHook,
)

from hooks_toolkit.xrpld import Xrpld
from hooks_toolkit.set_hook import set_hooks_v3, clear_hook_state_v3
from hooks_toolkit.types import SmartContractParams, SetHookParams
from hooks_toolkit.libs.keylet_utils.state_utility import StateUtility
from hooks_toolkit.utils import hex_namespace, pad_hex_string, flip_hex
from hooks_toolkit.libs.binary_models import xrp_address_to_hex, hex_to_uint64


class TestSetupHook(IntegrationTestCase):
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
                    version=0,
                    create_file="base",
                    namespace="base",
                    flags=[SetHookFlag.HSF_OVERRIDE],
                    hook_on_array=["Invoke"],
                )
            )

            set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])

            le_hook_req = LedgerEntry(
                hook=LeHook(account=cls.context.hook1.classic_address)
            )
            result = cls.context.client.request(le_hook_req).result
            le_hook = result["node"]

            hash = le_hook["Hooks"][0]["Hook"]["HookHash"]

            hook = create_hook_payload(
                SetHookParams(
                    hook_hash=hash,
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
                    version=0,
                    create_file="base",
                    namespace="base",
                    flags=[SetHookFlag.HSF_OVERRIDE],
                    hook_on_array=["Invoke"],
                )
            )

            set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])

            hook = create_hook_payload(
                SetHookParams(
                    namespace="base1",
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

    def test_set_hook_delete(cls):
        with cls.context.client as _:
            hook = create_hook_payload(
                SetHookParams(
                    version=0,
                    create_file="base",
                    namespace="base",
                    flags=[SetHookFlag.HSF_OVERRIDE],
                    hook_on_array=["Invoke"],
                )
            )

            set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])

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
                SetHookParams(
                    version=0,
                    create_file="state_basic",
                    namespace="state_basic",
                    flags=[SetHookFlag.HSF_OVERRIDE],
                    hook_on_array=["Invoke"],
                )
            )

            set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])

            hook_wallet = cls.context.hook1
            built_tx = Invoke(
                account=hook_wallet.classic_address,
            )

            Xrpld.submit(cls.context.client, SmartContractParams(hook_wallet, built_tx))

            hook_state = StateUtility.get_hook_state(
                cls.context.client,
                hook_wallet.classic_address,
                pad_hex_string(xrp_address_to_hex(hook_wallet.classic_address)),
                hex_namespace("state_basic"),
            )
            cls.assertGreater(
                hex_to_uint64(flip_hex(hook_state["HookStateData"])),
                0,
            )

            clear_hook = create_hook_payload(
                SetHookParams(
                    flags=[SetHookFlag.HSF_NS_DELETE],
                    namespace="state_basic",
                )
            )
            clear_hook_state_v3(
                cls.context.client, cls.context.hook1.seed, [clear_hook]
            )

            with cls.assertRaises(Exception):
                StateUtility.get_hook_state(
                    cls.context.client,
                    hook_wallet.classic_address,
                    pad_hex_string(xrp_address_to_hex(hook_wallet.classic_address)),
                    hex_namespace("state_basic"),
                )
