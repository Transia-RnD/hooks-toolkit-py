#!/usr/bin/env python
# coding: utf-8

from tests.integration.integration_test_case import IntegrationTestCase
from hooks_toolkit.set_hook import create_hook_payload
from xrpl.models.transactions import SetHookFlag, Invoke

from hooks_toolkit.xrpld import Xrpld
from hooks_toolkit.set_hook import set_hooks_v3
from hooks_toolkit.types import SmartContractParams
from hooks_toolkit.libs.keylet_utils.execution_utils import ExecutionUtility


class TestBase(IntegrationTestCase):
    def test_base_hook(cls):
        with cls.context.client as _:
            hook = create_hook_payload(
                0, "base", "base", [SetHookFlag.HSF_OVERRIDE], ["Invoke"]
            )

            set_hooks_v3(cls.context.client, cls.context.alice.seed, [hook])

            # INVOKE IN
            alice_wallet = cls.context.alice
            bob_wallet = cls.context.bob
            built_tx = Invoke(
                account=bob_wallet.classic_address,
                destination=alice_wallet.classic_address,
            )

            result = Xrpld.submit(
                cls.context.client, SmartContractParams(bob_wallet, built_tx)
            )

            hook_executions = ExecutionUtility.get_hook_executions_from_meta(
                cls.context.client, result["meta"]
            )

            cls.assertEqual(
                hook_executions.executions[0].HookReturnString, "base: Finished."
            )
