#!/usr/bin/env python
# coding: utf-8

from tests.integration.integration_test_case import IntegrationTestCase
from hooks_toolkit.set_hook import create_hook_payload
from xahau.models.transactions import SetHookFlag, Invoke

from hooks_toolkit.libs.xahau_helpers.server_url import server_url
from hooks_toolkit.libs.xahau_helpers.setup import (
    setup_client,
    XahauIntegrationTestContext,
    teardown_client,
)
from hooks_toolkit.xahaud import Xrpld
from hooks_toolkit.set_hook import set_hooks_v3, clear_all_hooks_v3
from hooks_toolkit.types import SmartContractParams, SetHookParams
from hooks_toolkit.libs.keylet_utils.execution_utility import ExecutionUtility


class TestBase(IntegrationTestCase):
    context: XahauIntegrationTestContext

    def setUp(cls) -> None:
        cls.context = setup_client(server_url)
        return super().setUp()

    def tearDown(cls) -> None:
        with cls.context.client as _:
            clear_all_hooks_v3(cls.context.client, cls.context.hook1.seed)
        teardown_client(cls.context)
        return super().tearDown()

    def test_base(cls):
        with cls.context.client as _:
            hook = create_hook_payload(
                SetHookParams(
                    version=0,
                    namespace="base",
                    create_file="base",
                    flags=[SetHookFlag.HSF_OVERRIDE],
                    hook_on_array=["Invoke"],
                )
            )

            set_hooks_v3(cls.context.client, cls.context.hook1.seed, [hook])

            # INVOKE IN
            hook_wallet = cls.context.hook1
            alice_wallet = cls.context.alice
            built_tx = Invoke(
                account=alice_wallet.classic_address,
                destination=hook_wallet.classic_address,
            )

            result = Xahaud.submit(
                cls.context.client, SmartContractParams(alice_wallet, built_tx)
            )

            hook_executions = ExecutionUtility.get_hook_executions_from_meta(
                result["meta"]
            )

            cls.assertEqual(
                hook_executions.executions[0].HookReturnString, "base: Finished."
            )
