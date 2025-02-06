#!/usr/bin/env python
# coding: utf-8

from unittest import TestCase
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


class TestSetupHook(TestCase):
    def test_create_hook_payload(cls):
        hook = create_hook_payload(
            SetHookParams(
                version=0,
                create_file="base",
                namespace="base",
                flags=[SetHookFlag.HSF_OVERRIDE],
                hook_on_array=["Payment"],
            )
        )
        cls.assertEqual(
            hook.hook_api_version,
            0,
        )
        cls.assertEqual(
            hook.create_code,
            "0061736D01000000011C0460057F7F7F7F7F017E60037F7F7E017E60027F7F017F60017F017E02230303656E76057472616365000003656E7606616363657074000103656E76025F670002030201030503010002062B077F0141C088040B7F004180080B7F0041B2080B7F004180080B7F0041C088040B7F0041000B7F0041010B07080104686F6F6B00030AC1800001BD800001017F230041106B220124002001200036020C41A00841114180084110410010001A4190084110420910011A4101410110021A200141106A240042000B0B3801004180080B31426173652E633A2043616C6C65642E00626173653A2046696E69736865642E0022426173652E633A2043616C6C65642E22",
        )
        cls.assertEqual(
            hook.hook_namespace,
            "CAE662172FD450BB0CD710A769079C05BFC5D8E35EFA6576EDC7D0377AFDD4A2",
        )
        cls.assertEqual(
            hook.flags[0],
            1,
        )
        cls.assertEqual(
            hook.hook_on,
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFFFE",
        )
