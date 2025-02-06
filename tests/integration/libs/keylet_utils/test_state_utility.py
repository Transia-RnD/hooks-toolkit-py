#!/usr/bin/env python
# coding: utf-8

from tests.integration.integration_test_case import IntegrationTestCase
from hooks_toolkit.set_hook import create_hook_payload
from xahau.models.transactions import SetHookFlag, Invoke
from xahau.models.transactions.set_hook import Hook

from hooks_toolkit.xahaud import Xrpld
from hooks_toolkit.set_hook import set_hooks_v3, clear_hook_state_v3
from hooks_toolkit.types import SmartContractParams, SetHookParams
from hooks_toolkit.libs.keylet_utils.state_utility import StateUtility
from hooks_toolkit.utils import hex_namespace, pad_hex_string, flip_hex
from hooks_toolkit.libs.binary_models import xrp_address_to_hex, hex_to_uint64


class TestStateUtility(IntegrationTestCase):
    def test_get_hook(cls):
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

            Xahaud.submit(
                cls.context.client, SmartContractParams(hook_wallet, built_tx)
            )

            hook = StateUtility.get_hook(
                cls.context.client,
                hook_wallet.classic_address,
            )
            cls.assertEqual(
                hook["Hooks"][0]["Hook"]["HookHash"],
                "B1F39E63D27603F1A2E7E804E92514FAC721F353D849B0787288F5026809AD84",
            )

            # clear hook
            hook = Hook(**{"create_code": "", "flags": [SetHookFlag.HSF_OVERRIDE]})
            set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])
            clear_hook = create_hook_payload(
                SetHookParams(
                    flags=[SetHookFlag.HSF_NS_DELETE],
                    namespace="state_basic",
                )
            )
            clear_hook_state_v3(
                cls.context.client, cls.context.hook1.seed, [clear_hook]
            )

    def test_get_hook_definition(cls):
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

            Xahaud.submit(
                cls.context.client, SmartContractParams(hook_wallet, built_tx)
            )

            hook_definition = StateUtility.get_hook_definition(
                cls.context.client,
                "B1F39E63D27603F1A2E7E804E92514FAC721F353D849B0787288F5026809AD84",
            )
            cls.assertEqual(
                hook_definition["LedgerEntryType"],
                "HookDefinition",
            )

            # clear hook
            hook = Hook(**{"create_code": "", "flags": [SetHookFlag.HSF_OVERRIDE]})
            set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])
            clear_hook = create_hook_payload(
                SetHookParams(
                    flags=[SetHookFlag.HSF_NS_DELETE],
                    namespace="state_basic",
                )
            )
            clear_hook_state_v3(
                cls.context.client, cls.context.hook1.seed, [clear_hook]
            )

    def test_hook_state_dir(cls):
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

            Xahaud.submit(
                cls.context.client, SmartContractParams(hook_wallet, built_tx)
            )

            hook_state_dir = StateUtility.get_hook_state_dir(
                cls.context.client,
                hook_wallet.classic_address,
                hex_namespace("state_basic"),
            )
            cls.assertEqual(
                len(hook_state_dir),
                1,
            )
            # clear hook
            hook = Hook(**{"create_code": "", "flags": [SetHookFlag.HSF_OVERRIDE]})
            set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])
            clear_hook = create_hook_payload(
                SetHookParams(
                    flags=[SetHookFlag.HSF_NS_DELETE],
                    namespace="state_basic",
                )
            )
            clear_hook_state_v3(
                cls.context.client, cls.context.hook1.seed, [clear_hook]
            )

    def test_hook_state(cls):
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

            Xahaud.submit(
                cls.context.client, SmartContractParams(hook_wallet, built_tx)
            )

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
            # clear hook
            hook = Hook(**{"create_code": "", "flags": [SetHookFlag.HSF_OVERRIDE]})
            set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])
            clear_hook = create_hook_payload(
                SetHookParams(
                    flags=[SetHookFlag.HSF_NS_DELETE],
                    namespace="state_basic",
                )
            )
            clear_hook_state_v3(
                cls.context.client, cls.context.hook1.seed, [clear_hook]
            )
