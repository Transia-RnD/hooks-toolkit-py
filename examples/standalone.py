#!/usr/bin/env python
# coding: utf-8

from hooks_toolkit.set_hook import create_hook_payload
from xahau.models.transactions import SetHookFlag, Invoke

from hooks_toolkit.libs.xahau_helpers.server_url import server_url
from hooks_toolkit.libs.xahau_helpers.setup import (
    setup_client,
    teardown_client,
)
from hooks_toolkit.xahaud import Xrpld
from hooks_toolkit.set_hook import set_hooks_v3
from hooks_toolkit.types import SmartContractParams, SetHookParams
from hooks_toolkit.libs.keylet_utils.execution_utility import ExecutionUtility


def main():
    context = setup_client(server_url)

    hook = create_hook_payload(
        SetHookParams(
            version=0,
            namespace="hook_on_tt",
            create_file="hook_on_tt",
            flags=[SetHookFlag.HSF_OVERRIDE],
            hook_on_array=["Invoke"],
        )
    )

    set_hooks_v3(context.client, context.hook1.seed, [hook])

    hook_wallet = context.hook1
    alice_wallet = context.alice
    built_tx = Invoke(
        account=alice_wallet.classic_address,
        destination=hook_wallet.classic_address,
    )

    result = Xahaud.submit(context.client, SmartContractParams(alice_wallet, built_tx))

    hook_executions = ExecutionUtility.get_hook_executions_from_meta(result["meta"])

    print(hook_executions.executions[0].HookReturnString)

    teardown_client(context)


main()
