#!/usr/bin/env python
# coding: utf-8

from tests.integration.asyncio_integration_test_case import AsyncioIntegrationTestCase
from hooks_toolkit.set_hook import create_hook_payload
from xrpl.models.transactions import SetHookFlag, Invoke
from xrpl.models.transactions.set_hook import Hook

from hooks_toolkit.asyncio_xrpld import Xrpld
from hooks_toolkit.asyncio_set_hook import set_hooks_v3, clear_hook_state_v3
from hooks_toolkit.types import SmartContractParams, SetHookParams
from hooks_toolkit.libs.asyncio.keylet_utils.state_utility import StateUtility
from hooks_toolkit.utils import hex_namespace, pad_hex_string, flip_hex
from hooks_toolkit.libs.binary_models import xrp_address_to_hex, hex_to_uint64


class TestStateUtility(AsyncioIntegrationTestCase):
    async def async_test_get_hook(cls):
        async with cls.context.client as _:
            hook = create_hook_payload(
                SetHookParams(
                    version=0,
                    create_file="state_basic",
                    namespace="state_basic",
                    flags=[SetHookFlag.HSF_OVERRIDE],
                    hook_on_array=["Invoke"],
                )
            )

            await set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])

            hook_wallet = cls.context.hook1
            built_tx = Invoke(
                account=hook_wallet.classic_address,
            )

            await Xrpld.submit(
                cls.context.client, SmartContractParams(hook_wallet, built_tx)
            )

            hook = await StateUtility.get_hook(
                cls.context.client,
                hook_wallet.classic_address,
            )
            cls.assertEqual(
                hook["Hooks"][0]["Hook"]["HookHash"],
                "B1F39E63D27603F1A2E7E804E92514FAC721F353D849B0787288F5026809AD84",
            )

            # clear hook
            hook = Hook(**{"create_code": "", "flags": [SetHookFlag.HSF_OVERRIDE]})
            await set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])
            clear_hook = create_hook_payload(
                SetHookParams(
                    flags=[SetHookFlag.HSF_NS_DELETE],
                    namespace="state_basic",
                )
            )
            await clear_hook_state_v3(
                cls.context.client, cls.context.hook1.seed, [clear_hook]
            )

    async def async_test_get_hook_definition(cls):
        async with cls.context.client as _:
            hook = create_hook_payload(
                SetHookParams(
                    version=0,
                    create_file="state_basic",
                    namespace="state_basic",
                    flags=[SetHookFlag.HSF_OVERRIDE],
                    hook_on_array=["Invoke"],
                )
            )

            await set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])

            hook_wallet = cls.context.hook1
            built_tx = Invoke(
                account=hook_wallet.classic_address,
            )

            await Xrpld.submit(
                cls.context.client, SmartContractParams(hook_wallet, built_tx)
            )

            hook_definition = await StateUtility.get_hook_definition(
                cls.context.client,
                "B1F39E63D27603F1A2E7E804E92514FAC721F353D849B0787288F5026809AD84",
            )
            cls.assertEqual(
                hook_definition["LedgerEntryType"],
                "HookDefinition",
            )

            # clear hook
            hook = Hook(**{"create_code": "", "flags": [SetHookFlag.HSF_OVERRIDE]})
            await set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])
            clear_hook = create_hook_payload(
                SetHookParams(
                    flags=[SetHookFlag.HSF_NS_DELETE],
                    namespace="state_basic",
                )
            )
            await clear_hook_state_v3(
                cls.context.client, cls.context.hook1.seed, [clear_hook]
            )

    async def async_test_hook_state_dir(cls):
        async with cls.context.client as _:
            hook = create_hook_payload(
                SetHookParams(
                    version=0,
                    create_file="state_basic",
                    namespace="state_basic",
                    flags=[SetHookFlag.HSF_OVERRIDE],
                    hook_on_array=["Invoke"],
                )
            )

            await set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])

            hook_wallet = cls.context.hook1
            built_tx = Invoke(
                account=hook_wallet.classic_address,
            )

            await Xrpld.submit(
                cls.context.client, SmartContractParams(hook_wallet, built_tx)
            )

            hook_state_dir = await StateUtility.get_hook_state_dir(
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
            await set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])
            clear_hook = create_hook_payload(
                SetHookParams(
                    flags=[SetHookFlag.HSF_NS_DELETE],
                    namespace="state_basic",
                )
            )
            await clear_hook_state_v3(
                cls.context.client, cls.context.hook1.seed, [clear_hook]
            )

    async def async_test_hook_state(cls):
        async with cls.context.client as _:
            hook = create_hook_payload(
                SetHookParams(
                    version=0,
                    create_file="state_basic",
                    namespace="state_basic",
                    flags=[SetHookFlag.HSF_OVERRIDE],
                    hook_on_array=["Invoke"],
                )
            )

            await set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])

            hook_wallet = cls.context.hook1
            built_tx = Invoke(
                account=hook_wallet.classic_address,
            )

            await Xrpld.submit(
                cls.context.client, SmartContractParams(hook_wallet, built_tx)
            )

            hook_state = await StateUtility.get_hook_state(
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
            await set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])
            clear_hook = create_hook_payload(
                SetHookParams(
                    flags=[SetHookFlag.HSF_NS_DELETE],
                    namespace="state_basic",
                )
            )
            await clear_hook_state_v3(
                cls.context.client, cls.context.hook1.seed, [clear_hook]
            )
