#!/usr/bin/env python
# coding: utf-8

from typing import Dict
from xrpl.clients import WebsocketClient
from xrpl.wallet import Wallet
from xrpl.ledger import get_network_id

from hooks_toolkit.libs.xrpl_helpers.constants import (
    NOT_ACTIVE_WALLET,
    MASTER_ACCOUNT_WALLET,
    GW_ACCOUNT_WALLET,
    ALICE_ACCOUNT_WALLET,
    BOB_ACCOUNT_WALLET,
    CAROL_ACCOUNT_WALLET,
    DAVE_ACCOUNT_WALLET,
    ELSA_ACCOUNT_WALLET,
    FRANK_ACCOUNT_WALLET,
    GRACE_ACCOUNT_WALLET,
    HEIDI_ACCOUNT_WALLET,
    IVAN_ACCOUNT_WALLET,
    JUDY_ACCOUNT_WALLET,
    HOOK1_ACCOUNT_WALLET,
    HOOK2_ACCOUNT_WALLET,
    HOOK3_ACCOUNT_WALLET,
    HOOK4_ACCOUNT_WALLET,
    HOOK5_ACCOUNT_WALLET,
)
from hooks_toolkit.libs.xrpl_helpers.fund_system import fund_system
from hooks_toolkit.libs.xrpl_helpers.tools import IC


class XrplIntegrationTestContext:
    def __init__(
        self,
        client: WebsocketClient,
        notactive: Wallet,
        master: Wallet,
        gw: Wallet,
        ic: IC,
        alice: Wallet,
        bob: Wallet,
        carol: Wallet,
        dave: Wallet,
        elsa: Wallet,
        frank: Wallet,
        grace: Wallet,
        heidi: Wallet,
        ivan: Wallet,
        judy: Wallet,
        hook1: Wallet,
        hook2: Wallet,
        hook3: Wallet,
        hook4: Wallet,
        hook5: Wallet,
    ):
        self.client = client
        self.notactive = notactive
        self.master = master
        self.gw = gw
        self.ic = ic
        self.alice = alice
        self.bob = bob
        self.carol = carol
        self.dave = dave
        self.elsa = elsa
        self.frank = frank
        self.grace = grace
        self.heidi = heidi
        self.ivan = ivan
        self.judy = judy
        self.hook1 = hook1
        self.hook2 = hook2
        self.hook3 = hook3
        self.hook4 = hook4
        self.hook5 = hook5


def teardown_client(context: XrplIntegrationTestContext) -> None:
    if not context or not context.client:
        return
    return context.client.close()


def setup_client(server: str, native_amount: int = 20000, ic_limit: int = 100000, ic_amount: int = 50000) -> XrplIntegrationTestContext:
    currency = "USD"

    with WebsocketClient(server) as client:
        context = XrplIntegrationTestContext(
            client=client,
            notactive=NOT_ACTIVE_WALLET,
            master=MASTER_ACCOUNT_WALLET,
            gw=GW_ACCOUNT_WALLET,
            ic=IC.gw(currency, GW_ACCOUNT_WALLET.classic_address),
            alice=ALICE_ACCOUNT_WALLET,
            bob=BOB_ACCOUNT_WALLET,
            carol=CAROL_ACCOUNT_WALLET,
            dave=DAVE_ACCOUNT_WALLET,
            elsa=ELSA_ACCOUNT_WALLET,
            frank=FRANK_ACCOUNT_WALLET,
            grace=GRACE_ACCOUNT_WALLET,
            heidi=HEIDI_ACCOUNT_WALLET,
            ivan=IVAN_ACCOUNT_WALLET,
            judy=JUDY_ACCOUNT_WALLET,
            hook1=HOOK1_ACCOUNT_WALLET,
            hook2=HOOK2_ACCOUNT_WALLET,
            hook3=HOOK3_ACCOUNT_WALLET,
            hook4=HOOK4_ACCOUNT_WALLET,
            hook5=HOOK5_ACCOUNT_WALLET,
        )
        context.client.network_id = get_network_id(client)
        fund_system(
            context.client, 
            context.master, 
            context.ic,
            native_amount, 
            ic_limit, 
            ic_amount
        )
        return context
