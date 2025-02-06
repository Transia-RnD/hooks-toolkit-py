#!/usr/bin/env python
# coding: utf-8

from tests.integration.integration_test_case import IntegrationTestCase
from hooks_toolkit.set_hook import create_hook_payload
from xahau.models.transactions import SetHookFlag, Invoke
from xahau.models.transactions.set_hook import Hook

from hooks_toolkit.xrpld import Xrpld
from hooks_toolkit.set_hook import set_hooks_v3, clear_hook_state_v3
from hooks_toolkit.types import SmartContractParams, SetHookParams
from hooks_toolkit.libs.keylet_utils.execution_utility import ExecutionUtility
from hooks_toolkit.utils import hex_namespace, pad_hex_string, flip_hex
from hooks_toolkit.libs.binary_models import xrp_address_to_hex, hex_to_uint64


class TestExecutionUtility(IntegrationTestCase):
    def test_executions_from_meta(cls):
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

            response = Xrpld.submit(
                cls.context.client, SmartContractParams(hook_wallet, built_tx)
            )
            executions = ExecutionUtility.get_hook_executions_from_meta(
                response["meta"]
            )
            cls.assertEqual(
                executions.executions[0].HookReturnCode,
                "22",
            )
            cls.assertEqual(
                executions.executions[0].HookHash,
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

    def test_executions_from_tx_hash(cls):
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

            response = Xrpld.submit(
                cls.context.client, SmartContractParams(hook_wallet, built_tx)
            )
            print(response["hash"])
            executions = ExecutionUtility.get_hook_executions_from_tx(
                cls.context.client, response["hash"]
            )
            cls.assertEqual(
                executions.executions[0].HookReturnCode,
                "22",
            )
            cls.assertEqual(
                executions.executions[0].HookHash,
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

    def test_emissions_from_meta(cls):
        with cls.context.client as _:
            hook = create_hook_payload(
                SetHookParams(
                    version=0,
                    create_file="callback",
                    namespace="callback",
                    flags=[SetHookFlag.HSF_OVERRIDE],
                    hook_on_array=["Invoke"],
                )
            )

            set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])

            hook_wallet = cls.context.hook1
            built_tx = Invoke(
                account=hook_wallet.classic_address,
            )

            response = Xrpld.submit(
                cls.context.client, SmartContractParams(hook_wallet, built_tx)
            )
            emissions = ExecutionUtility.get_hook_emitted_txs_from_meta(
                response["meta"]
            )
            cls.assertEqual(
                emissions.txs[0].HookHash,
                "2E079E2D4D5C54386612F323C3BF0689942E8856CCE23DD262793C20A15D0A0B",
            )
            cls.assertEqual(
                emissions.txs[0].HookAccount,
                "rBpVrkKc8QnxsCGsngMJgmDKqxJKoWHfKt",
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
