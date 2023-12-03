#!/usr/bin/env python
# coding: utf-8

import json
import os
from typing import Union

from xrpl.transaction import sign_and_submit, autofill, send_reliable_submission
from xrpl.clients.sync_client import SyncClient
from xrpl.models import GenericRequest, Response, Transaction
from xrpl.wallet import Wallet
from xrpl.core.binarycodec import encode
from xrpl.ledger import get_fee_estimate
from xrpl.models.requests import Tx

LEDGER_ACCEPT_REQUEST = GenericRequest(method="ledger_accept")


def verify_submitted_transaction(
    client: SyncClient, tx: Union[Transaction, str]
) -> Response:
    # hash = hash_tx if tx else hash_signed_tx(tx)
    hash = tx
    data = client.request(Tx(transaction=hash))

    # assert data.result
    # assert data.result == (decode(tx) if isinstance(tx, str) else tx)
    # if isinstance(data.result.meta, dict):
    #     assert data.result.meta["TransactionResult"] == "tesSUCCESS"
    # else:
    #     assert data.result.meta == "tesSUCCESS"
    return data


def get_transaction_fee(client: SyncClient, transaction: Transaction):
    # copy_tx = transaction.to_xrpl()
    # copy_tx["Fee"] = "0"
    # copy_tx["SigningPubKey"] = ""
    prepared_tx = autofill(transaction, client)

    tx_blob = encode(prepared_tx.to_xrpl())

    result = get_fee_estimate(client, tx_blob)

    return result


def app_transaction(
    client: SyncClient,
    transaction: Transaction,
    wallet: Wallet,
    hard_fail: bool = True,
    count: int = 0,
    delay_ms: int = 0,
) -> Response:
    if os.environ.get("RIPPLED_ENV", "standalone") == "standalone":
        return test_transaction(
            client, 
            transaction, 
            wallet, 
            hard_fail, 
            count, 
            delay_ms
        )
    raise ValueError("unimplemented")
    # return sign_and_reliable_submission(transaction, wallet, client)


def test_transaction(
    client: SyncClient,
    transaction: Transaction,
    wallet: Wallet,
    hard_fail: bool,
    count: int,
    delay_ms: int,
) -> Response:
    client.request(LEDGER_ACCEPT_REQUEST)

    response = sign_and_submit(transaction, wallet, client, True, False)

    assert response.type == "response"

    if response.result["engine_result"] != "tesSUCCESS":
        print(
            f"Transaction was not successful. Expected response.result.engine_result to be tesSUCCESS but got {response.result['engine_result']}"
        )
        print("The transaction was: ", transaction)
        print("The response was: ", json.dumps(response.result))

    if hard_fail:
        assert response.result["engine_result"] == "tesSUCCESS", response.result[
            "engine_result_message"
        ]

    # signed_tx = omit(response.result.tx_json, "hash")
    client.request(LEDGER_ACCEPT_REQUEST)
    # return verify_submitted_transaction(client, response.result["hash"])
    return verify_submitted_transaction(client, response.result["tx_json"]["hash"])


# export async function prod_transaction(
#   client: Client,
#   transaction: Transaction,
#   wallet: Wallet,
#   retry?: {
#     hardFail: boolean | true
#     count: number
#     delayMs: number
#   }
# ): Promise<TxResponse> {
#   // sign/submit the transaction
#   const response = await client.submit(transaction, {
#     autofill: true,
#     wallet: wallet,
#   })

#   console.log(response.result.engine_result)

#   // check that the transaction was successful
#   assert.equal(response.type, 'response')

#   // check that the transaction was successful
#   assert.equal(response.type, 'response')

#   if (response.result.engine_result !== 'tesSUCCESS') {
#     // eslint-disable-next-line no-console -- See output
#     console.error(
#       `Transaction was not successful. Expected response.result.engine_result to be tesSUCCESS but got ${response.result.engine_result}`
#     )
#     // eslint-disable-next-line no-console -- See output
#     console.error('The transaction was: ', transaction)
#     // eslint-disable-next-line no-console -- See output
#     console.error('The response was: ', JSON.stringify(response))
#   }

#   if (retry?.hardFail) {
#     assert.equal(
#       response.result.engine_result,
#       'tesSUCCESS',
#       response.result.engine_result_message
#     )
#   }

#   // check that the transaction is on the ledger
#   return await verifySubmittedTransaction(
#     client,
#     '',
#     response.result.tx_json.hash as string
#   )
#   // return response
# }
