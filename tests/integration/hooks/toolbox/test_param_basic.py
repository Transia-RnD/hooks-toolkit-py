#!/usr/bin/env python
# coding: utf-8

from unittest import TestCase
from hooks_toolkit.set_hook import create_hook_payload
from xrpl.models.transactions import SetHookFlag, Payment

from hooks_toolkit.libs.xrpl_helpers.server_url import server_url
from hooks_toolkit.libs.xrpl_helpers.setup import (
    setup_client,
    XrplIntegrationTestContext,
    teardown_client,
)
from hooks_toolkit.xrpld import Xrpld
from hooks_toolkit.set_hook import set_hooks_v3, clear_all_hooks_v3
from hooks_toolkit.types import SmartContractParams, SetHookParams
from hooks_toolkit.models.parameters import (
    iHookParamEntry,
    iHookParamName,
    iHookParamValue,
)
from hooks_toolkit.utils import float_to_le_xfl
from hooks_toolkit.libs.keylet_utils.execution_utility import ExecutionUtility


class TestBase(TestCase):
    context: XrplIntegrationTestContext

    def setUp(cls) -> None:
        cls.context = setup_client(server_url)
        return super().setUp()

    def tearDown(cls) -> None:
        # with cls.context.client as _:
        #     clear_all_hooks_v3(cls.context.client, cls.context.hook1.seed)
        teardown_client(cls.context)
        return super().tearDown()

    def test_param_basic(cls):
        with cls.context.client as _:
            hook_param1 = iHookParamEntry(
                iHookParamName("TEST"), iHookParamValue(float_to_le_xfl(10), True)
            )

            hook = create_hook_payload(
                SetHookParams(
                    version=0,
                    namespace="param_basic",
                    create_file="param_basic",
                    flags=[SetHookFlag.HSF_OVERRIDE],
                    hook_on_array=["Payment"],
                    hook_parameters=[hook_param1.to_xrpl()],
                )
            )

            set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])

            # INVOKE IN
            hook_wallet = cls.context.hook1
            alice_wallet = cls.context.alice
            otxn_param1 = iHookParamEntry(
                iHookParamName("TEST"), iHookParamValue(float_to_le_xfl(10), True)
            )
            built_tx = Payment(
                account=alice_wallet.classic_address,
                destination=hook_wallet.classic_address,
                amount="10000000",
                hook_parameters=[otxn_param1.to_xrpl()],
            )

            result = Xrpld.submit(
                cls.context.client, SmartContractParams(alice_wallet, built_tx)
            )

            hook_executions = ExecutionUtility.get_hook_executions_from_meta(
                cls.context.client, result["meta"]
            )

            cls.assertEqual(
                hook_executions.executions[0].HookReturnString, "param_basic: Finished."
            )
