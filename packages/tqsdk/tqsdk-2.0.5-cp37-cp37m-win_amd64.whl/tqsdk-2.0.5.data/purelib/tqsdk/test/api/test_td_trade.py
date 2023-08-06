#!usr/bin/env python3
#-*- coding:utf-8 -*-
"""
@author: yanqiong
@file: test_td_trade.py
@create_on: 2020/6/12
@description: 
"""
import os
import random
import unittest

from tqsdk import TqApi, TqAccount, utils
from tqsdk.test.api.helper import MockInsServer, MockServer


class TestTdTrade(unittest.TestCase):
    """
    实盘账户下，insert_order 各种情况测试
    """

    def setUp(self):
        self.ins = MockInsServer()
        os.environ["TQ_INS_URL"] = f"http://127.0.0.1:{self.ins.port}/t/md/symbols/2020-09-15.json"
        os.environ["TQ_AUTH_URL"] = f"http://127.0.0.1:{self.ins.port}"
        self.mock = MockServer(md_url_character="nfmd", td_url_character="q7.htfutures.com")

    def tearDown(self):
        self.ins.close()
        self.mock.close()

    def test_insert_order_shfe_anyprice(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.mock.run(os.path.join(dir_path, "log_file", "test_insert_order_shfe_anyprice.script.lzma"))
        self.md_url = f"ws://127.0.0.1:{self.mock.md_port}/"
        self.td_url = f"ws://127.0.0.1:{self.mock.td_port}/"
        # 测试
        account = TqAccount("H海通期货", "83011119", "sha121212")
        utils.RD = random.Random(4)
        # 测试
        api = TqApi(account=account, auth="tianqin,tianqin", _md_url=self.md_url, _td_url=self.td_url, debug=False)
        self.assertRaises(Exception, api.insert_order, "SHFE.au2012", "BUY", "OPEN", 1)
        api.close()

    def test_insert_order_shfe_limit_fok(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.mock.run(os.path.join(dir_path, "log_file", "test_insert_order_shfe_limit_fok.script.lzma"))
        self.md_url = f"ws://127.0.0.1:{self.mock.md_port}/"
        self.td_url = f"ws://127.0.0.1:{self.mock.td_port}/"
        # 测试
        account = TqAccount("H海通期货", "83011119", "sha121212")
        utils.RD = random.Random(4)
        with TqApi(account=account, auth="tianqin,tianqin", _md_url=self.md_url, _td_url=self.td_url, debug=False) as api:
            order1 = api.insert_order("SHFE.au2012", "BUY", "OPEN", 2, limit_price=380, advanced="FOK", order_id="PYSDK_insert_SHFE_limit_FOK2")
            while True:
                api.wait_update()
                if order1.status == "FINISHED":
                    break
            self.assertEqual("PYSDK_insert_SHFE_limit_FOK2", order1.order_id)
            self.assertEqual("", order1.exchange_order_id)
            self.assertEqual("SHFE", order1.exchange_id)
            self.assertEqual("au2012", order1.instrument_id)
            self.assertEqual("BUY", order1.direction)
            self.assertEqual("OPEN", order1.offset)
            self.assertEqual(2, order1.volume_orign)
            self.assertEqual(2, order1.volume_left)
            self.assertEqual(380.0, order1.limit_price)
            self.assertEqual(1604028207403039240, order1.insert_date_time)
            self.assertEqual("FINISHED", order1.status)
            self.assertEqual("LIMIT", order1.price_type)
            self.assertEqual("ALL", order1.volume_condition)
            self.assertEqual("IOC", order1.time_condition)
            self.assertEqual("CTP:资金不足", order1.last_msg)
            self.assertEqual(
                "{'order_id': 'PYSDK_insert_SHFE_limit_FOK2', 'exchange_order_id': '', 'exchange_id': 'SHFE', 'instrument_id': 'au2012', 'direction': 'BUY', 'offset': 'OPEN', 'volume_orign': 2, 'volume_left': 2, 'limit_price': 380.0, 'price_type': 'LIMIT', 'volume_condition': 'ALL', 'time_condition': 'IOC', 'insert_date_time': 1604028207403039240, 'last_msg': 'CTP:资金不足', 'status': 'FINISHED', 'seqno': 0, 'user_id': '83011119', 'frozen_margin': 0.0, 'frozen_premium': 0.0, 'frozen_commission': 0.0}",
                str(order1))

    def test_insert_order_shfe_limit_fak(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.mock.run(os.path.join(dir_path, "log_file", "test_insert_order_shfe_limit_fak.script.lzma"))
        self.md_url = f"ws://127.0.0.1:{self.mock.md_port}/"
        self.td_url = f"ws://127.0.0.1:{self.mock.td_port}/"
        # 测试
        account = TqAccount("H海通期货", "83011119", "sha121212")
        utils.RD = random.Random(4)
        with TqApi(account=account, auth="tianqin,tianqin", _md_url=self.md_url, _td_url=self.td_url, debug=False) as api:
            order1 = api.insert_order("SHFE.au2012", "BUY", "OPEN", 2, limit_price=380, advanced="FAK", order_id="PYSDK_insert_SHFE_limit_FAK2")
            while True:
                api.wait_update()
                if order1.status == "FINISHED":
                    break
            self.assertEqual("PYSDK_insert_SHFE_limit_FAK2", order1.order_id)
            self.assertEqual("", order1.exchange_order_id)
            self.assertEqual("SHFE", order1.exchange_id)
            self.assertEqual("au2012", order1.instrument_id)
            self.assertEqual("BUY", order1.direction)
            self.assertEqual("OPEN", order1.offset)
            self.assertEqual(2, order1.volume_orign)
            self.assertEqual(2, order1.volume_left)
            self.assertEqual(380.0, order1.limit_price)
            self.assertEqual(1604028233751296278, order1.insert_date_time)
            self.assertEqual("FINISHED", order1.status)
            self.assertEqual("LIMIT", order1.price_type)
            self.assertEqual("ANY", order1.volume_condition)
            self.assertEqual("IOC", order1.time_condition)
            self.assertEqual("CTP:资金不足", order1.last_msg)
            self.assertEqual(
                "{'order_id': 'PYSDK_insert_SHFE_limit_FAK2', 'exchange_order_id': '', 'exchange_id': 'SHFE', 'instrument_id': 'au2012', 'direction': 'BUY', 'offset': 'OPEN', 'volume_orign': 2, 'volume_left': 2, 'limit_price': 380.0, 'price_type': 'LIMIT', 'volume_condition': 'ANY', 'time_condition': 'IOC', 'insert_date_time': 1604028233751296278, 'last_msg': 'CTP:资金不足', 'status': 'FINISHED', 'seqno': 0, 'user_id': '83011119', 'frozen_margin': 0.0, 'frozen_premium': 0.0, 'frozen_commission': 0.0}",
                str(order1))

    def test_insert_order_dec_best(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.mock.run(os.path.join(dir_path, "log_file", "test_insert_order_dec_best.script.lzma"))
        self.md_url = f"ws://127.0.0.1:{self.mock.md_port}/"
        self.td_url = f"ws://127.0.0.1:{self.mock.td_port}/"
        # 测试
        account = TqAccount("H海通期货", "83011119", "sha121212")
        utils.RD = random.Random(4)
        # 测试
        api = TqApi(account=account, auth="tianqin,tianqin", _md_url=self.md_url, _td_url=self.td_url, debug=False)
        self.assertRaises(Exception, api.insert_order, "DCE.m2101", "BUY", "OPEN", 1, limit_price="BEST", order_id="PYSDK_insert_DCE_BEST")
        api.close()

    def test_insert_order_dec_fivelevel(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.mock.run(os.path.join(dir_path, "log_file", "test_insert_order_dec_fivelevel.script.lzma"))
        self.md_url = f"ws://127.0.0.1:{self.mock.md_port}/"
        self.td_url = f"ws://127.0.0.1:{self.mock.td_port}/"
        # 测试
        account = TqAccount("H海通期货", "83011119", "sha121212")
        utils.RD = random.Random(4)
        # 测试
        api = TqApi(account=account, auth="tianqin,tianqin", _md_url=self.md_url, _td_url=self.td_url, debug=False)
        self.assertRaises(Exception, api.insert_order, "DCE.m2101", "BUY", "OPEN", 1, limit_price="FIVELEVEL",
                                          order_id="PYSDK_insert_DCE_FIVELEVEL")
        api.close()

    def test_insert_order_dce_anyprice(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.mock.run(os.path.join(dir_path, "log_file", "test_insert_order_dce_anyprice.script.lzma"))
        self.md_url = f"ws://127.0.0.1:{self.mock.md_port}/"
        self.td_url = f"ws://127.0.0.1:{self.mock.td_port}/"
        # 测试
        account = TqAccount("H海通期货", "83011119", "sha121212")
        utils.RD = random.Random(4)
        with TqApi(account=account, auth="tianqin,tianqin", _md_url=self.md_url, _td_url=self.td_url,
                   debug=False) as api:
            order1 = api.insert_order("DCE.m2101", "BUY", "OPEN", 1, order_id="PYSDK_insert_DCE_any")
            while True:
                api.wait_update()
                if order1.status == "FINISHED":
                    break
            self.assertEqual("PYSDK_insert_DCE_any", order1.order_id)
            self.assertEqual("    34516514", order1.exchange_order_id)
            self.assertEqual("DCE", order1.exchange_id)
            self.assertEqual("m2101", order1.instrument_id)
            self.assertEqual("BUY", order1.direction)
            self.assertEqual("OPEN", order1.offset)
            self.assertEqual(1, order1.volume_orign)
            self.assertEqual(0, order1.volume_left)
            self.assertEqual(0.0, order1.limit_price)
            self.assertEqual(1604036822000000000, order1.insert_date_time)
            self.assertEqual("FINISHED", order1.status)
            self.assertEqual("ANY", order1.price_type)
            self.assertEqual("ANY", order1.volume_condition)
            self.assertEqual("IOC", order1.time_condition)
            self.assertEqual("全部成交", order1.last_msg)
            self.assertEqual(
                "{'order_id': 'PYSDK_insert_DCE_any', 'exchange_order_id': '    34516514', 'exchange_id': 'DCE', 'instrument_id': 'm2101', 'direction': 'BUY', 'offset': 'OPEN', 'volume_orign': 1, 'volume_left': 0, 'limit_price': 0.0, 'price_type': 'ANY', 'volume_condition': 'ANY', 'time_condition': 'IOC', 'insert_date_time': 1604036822000000000, 'last_msg': '全部成交', 'status': 'FINISHED', 'seqno': 6, 'user_id': '83011119', 'frozen_margin': 0.0, 'frozen_premium': 0.0, 'frozen_commission': 0.0}",
                str(order1))

    def test_insert_order_dce_anyprice_fok(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.mock.run(os.path.join(dir_path, "log_file", "test_insert_order_dce_anyprice_fok.script.lzma"))
        self.md_url = f"ws://127.0.0.1:{self.mock.md_port}/"
        self.td_url = f"ws://127.0.0.1:{self.mock.td_port}/"
        # 测试
        account = TqAccount("H海通期货", "83011119", "sha121212")
        utils.RD = random.Random(4)
        with TqApi(account=account, auth="tianqin,tianqin", _md_url=self.md_url, _td_url=self.td_url,
                   debug=False) as api:
            order1 = api.insert_order("DCE.m2101", "BUY", "OPEN", 2, advanced="FOK", order_id="PYSDK_insert_DCE_any_FOK")
            while True:
                api.wait_update()
                if order1.status == "FINISHED":
                    break
            self.assertEqual("PYSDK_insert_DCE_any_FOK", order1.order_id)
            self.assertEqual("    34962461", order1.exchange_order_id)
            self.assertEqual("DCE", order1.exchange_id)
            self.assertEqual("m2101", order1.instrument_id)
            self.assertEqual("BUY", order1.direction)
            self.assertEqual("OPEN", order1.offset)
            self.assertEqual(2, order1.volume_orign)
            self.assertEqual(0, order1.volume_left)
            self.assertEqual(0.0, order1.limit_price)
            self.assertEqual(1604037086000000000, order1.insert_date_time)
            self.assertEqual("FINISHED", order1.status)
            self.assertEqual("ANY", order1.price_type)
            self.assertEqual("ALL", order1.volume_condition)
            self.assertEqual("IOC", order1.time_condition)
            self.assertEqual("全部成交", order1.last_msg)
            self.assertEqual(
                "{'order_id': 'PYSDK_insert_DCE_any_FOK', 'exchange_order_id': '    34962461', 'exchange_id': 'DCE', 'instrument_id': 'm2101', 'direction': 'BUY', 'offset': 'OPEN', 'volume_orign': 2, 'volume_left': 0, 'limit_price': 0.0, 'price_type': 'ANY', 'volume_condition': 'ALL', 'time_condition': 'IOC', 'insert_date_time': 1604037086000000000, 'last_msg': '全部成交', 'status': 'FINISHED', 'seqno': 17, 'user_id': '83011119', 'frozen_margin': 0.0, 'frozen_premium': 0.0, 'frozen_commission': 0.0}",
                str(order1))

    def test_insert_order_dce_limit_fak(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.mock.run(os.path.join(dir_path, "log_file", "test_insert_order_dce_limit_fak.script.lzma"))
        self.md_url = f"ws://127.0.0.1:{self.mock.md_port}/"
        self.td_url = f"ws://127.0.0.1:{self.mock.td_port}/"
        # 测试
        account = TqAccount("H海通期货", "83011119", "sha121212")
        utils.RD = random.Random(4)
        with TqApi(account=account, auth="tianqin,tianqin", _md_url=self.md_url, _td_url=self.td_url,
                   debug=False) as api:
            order1 = api.insert_order("DCE.m2101", "SELL", "CLOSE", 1, limit_price=3198, advanced="FAK", order_id="PYSDK_insert_DCE_limit_FAK1")
            while True:
                api.wait_update()
                if order1.status == "FINISHED":
                    break
            self.assertEqual("PYSDK_insert_DCE_limit_FAK1", order1.order_id)
            self.assertEqual("    34883153", order1.exchange_order_id)
            self.assertEqual("DCE", order1.exchange_id)
            self.assertEqual("m2101", order1.instrument_id)
            self.assertEqual("SELL", order1.direction)
            self.assertEqual("CLOSE", order1.offset)
            self.assertEqual(1, order1.volume_orign)
            self.assertEqual(0, order1.volume_left)
            self.assertEqual(3198.0, order1.limit_price)
            self.assertEqual(1604037038000000000, order1.insert_date_time)
            self.assertEqual("FINISHED", order1.status)
            self.assertEqual("LIMIT", order1.price_type)
            self.assertEqual("ANY", order1.volume_condition)
            self.assertEqual("IOC", order1.time_condition)
            self.assertEqual("全部成交", order1.last_msg)
            self.assertEqual(
                "{'order_id': 'PYSDK_insert_DCE_limit_FAK1', 'exchange_order_id': '    34883153', 'exchange_id': 'DCE', 'instrument_id': 'm2101', 'direction': 'SELL', 'offset': 'CLOSE', 'volume_orign': 1, 'volume_left': 0, 'limit_price': 3198.0, 'price_type': 'LIMIT', 'volume_condition': 'ANY', 'time_condition': 'IOC', 'insert_date_time': 1604037038000000000, 'last_msg': '全部成交', 'status': 'FINISHED', 'seqno': 12, 'user_id': '83011119', 'frozen_margin': 0.0, 'frozen_premium': 0.0, 'frozen_commission': 0.0}",
                str(order1))

    def test_insert_order_dce_limit_fok(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.mock.run(os.path.join(dir_path, "log_file", "test_insert_order_dce_limit_fok.script.lzma"))
        self.md_url = f"ws://127.0.0.1:{self.mock.md_port}/"
        self.td_url = f"ws://127.0.0.1:{self.mock.td_port}/"
        # 测试
        account = TqAccount("H海通期货", "83011119", "sha121212")
        utils.RD = random.Random(4)
        with TqApi(account=account, auth="tianqin,tianqin", _md_url=self.md_url, _td_url=self.td_url,
                   debug=False) as api:
            order1 = api.insert_order("DCE.m2101", "SELL", "OPEN", 2, limit_price=3204, advanced="FOK", order_id="PYSDK_insert_DCE_limit_FOK5")
            while True:
                api.wait_update()
                if order1.status == "FINISHED":
                    break
            print(order1)
            self.assertEqual("PYSDK_insert_DCE_limit_FOK5", order1.order_id)
            self.assertEqual("    36131210", order1.exchange_order_id)
            self.assertEqual("DCE", order1.exchange_id)
            self.assertEqual("m2101", order1.instrument_id)
            self.assertEqual("SELL", order1.direction)
            self.assertEqual("OPEN", order1.offset)
            self.assertEqual(2, order1.volume_orign)
            self.assertEqual(2, order1.volume_left)
            self.assertEqual(3204.0, order1.limit_price)
            self.assertEqual(1604037807000000000, order1.insert_date_time)
            self.assertEqual("FINISHED", order1.status)
            self.assertEqual("LIMIT", order1.price_type)
            self.assertEqual("ALL", order1.volume_condition)
            self.assertEqual("IOC", order1.time_condition)
            self.assertEqual("已撤单", order1.last_msg)
            self.assertEqual(
                "{'order_id': 'PYSDK_insert_DCE_limit_FOK5', 'exchange_order_id': '    36131210', 'exchange_id': 'DCE', 'instrument_id': 'm2101', 'direction': 'SELL', 'offset': 'OPEN', 'volume_orign': 2, 'volume_left': 2, 'limit_price': 3204.0, 'price_type': 'LIMIT', 'volume_condition': 'ALL', 'time_condition': 'IOC', 'insert_date_time': 1604037807000000000, 'last_msg': '已撤单', 'status': 'FINISHED', 'seqno': 42, 'user_id': '83011119', 'frozen_margin': 0.0, 'frozen_premium': 0.0, 'frozen_commission': 0.0}",
                str(order1))

    def test_insert_order_dce_limit_fak1(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.mock.run(os.path.join(dir_path, "log_file", "test_insert_order_dce_limit_fak1.script.lzma"))
        self.md_url = f"ws://127.0.0.1:{self.mock.md_port}/"
        self.td_url = f"ws://127.0.0.1:{self.mock.td_port}/"
        # 测试
        account = TqAccount("H海通期货", "83011119", "sha121212")
        utils.RD = random.Random(4)
        with TqApi(account=account, auth="tianqin,tianqin", _md_url=self.md_url, _td_url=self.td_url,
                   debug=False) as api:
            order1 = api.insert_order("DCE.m2101", "BUY", "OPEN", 2, limit_price=2890, advanced="FAK", order_id="PYSDK_insert_DCE_limit_FAK2")
            while True:
                api.wait_update()
                if order1.status == "FINISHED":
                    break
            self.assertEqual("PYSDK_insert_DCE_limit_FAK2", order1.order_id)
            self.assertEqual("", order1.exchange_order_id)
            self.assertEqual("DCE", order1.exchange_id)
            self.assertEqual("m2101", order1.instrument_id)
            self.assertEqual("BUY", order1.direction)
            self.assertEqual("OPEN", order1.offset)
            self.assertEqual(2, order1.volume_orign)
            self.assertEqual(2, order1.volume_left)
            self.assertEqual(2890.0, order1.limit_price)
            self.assertEqual(1604037465658810695, order1.insert_date_time)
            self.assertEqual("FINISHED", order1.status)
            self.assertEqual("LIMIT", order1.price_type)
            self.assertEqual("ANY", order1.volume_condition)
            self.assertEqual("IOC", order1.time_condition)
            self.assertEqual("CTP:资金不足", order1.last_msg)
            self.assertEqual(
                "{'order_id': 'PYSDK_insert_DCE_limit_FAK2', 'exchange_order_id': '', 'exchange_id': 'DCE', 'instrument_id': 'm2101', 'direction': 'BUY', 'offset': 'OPEN', 'volume_orign': 2, 'volume_left': 2, 'limit_price': 2890.0, 'price_type': 'LIMIT', 'volume_condition': 'ANY', 'time_condition': 'IOC', 'insert_date_time': 1604037465658810695, 'last_msg': 'CTP:资金不足', 'status': 'FINISHED', 'seqno': 0, 'user_id': '83011119', 'frozen_margin': 0.0, 'frozen_premium': 0.0, 'frozen_commission': 0.0}",
                str(order1))

    def test_insert_order_dce_limit_fok1(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.mock.run(os.path.join(dir_path, "log_file", "test_insert_order_dce_limit_fok1.script.lzma"))
        self.md_url = f"ws://127.0.0.1:{self.mock.md_port}/"
        self.td_url = f"ws://127.0.0.1:{self.mock.td_port}/"
        # 测试
        account = TqAccount("H海通期货", "83011119", "sha121212")
        utils.RD = random.Random(4)
        with TqApi(account=account, auth="tianqin,tianqin", _md_url=self.md_url, _td_url=self.td_url,
                   debug=False) as api:
            order1 = api.insert_order("DCE.m2101", "SELL", "CLOSE", 2, limit_price=3200, advanced="FOK", order_id="PYSDK_insert_DCE_limit_FOK2")
            while True:
                api.wait_update()
                if order1.status == "FINISHED":
                    break
            print(str(order1))
            self.assertEqual("PYSDK_insert_DCE_limit_FOK2", order1.order_id)
            self.assertEqual("    35241113", order1.exchange_order_id)
            self.assertEqual("DCE", order1.exchange_id)
            self.assertEqual("m2101", order1.instrument_id)
            self.assertEqual("SELL", order1.direction)
            self.assertEqual("CLOSE", order1.offset)
            self.assertEqual(2, order1.volume_orign)
            self.assertEqual(2, order1.volume_left)
            self.assertEqual(3200.0, order1.limit_price)
            self.assertEqual(1604037297000000000, order1.insert_date_time)
            self.assertEqual("FINISHED", order1.status)
            self.assertEqual("LIMIT", order1.price_type)
            self.assertEqual("ALL", order1.volume_condition)
            self.assertEqual("IOC", order1.time_condition)
            self.assertEqual("已撤单", order1.last_msg)
            self.assertEqual(
                "{'order_id': 'PYSDK_insert_DCE_limit_FOK2', 'exchange_order_id': '    35241113', 'exchange_id': 'DCE', 'instrument_id': 'm2101', 'direction': 'SELL', 'offset': 'CLOSE', 'volume_orign': 2, 'volume_left': 2, 'limit_price': 3200.0, 'price_type': 'LIMIT', 'volume_condition': 'ALL', 'time_condition': 'IOC', 'insert_date_time': 1604037297000000000, 'last_msg': '已撤单', 'status': 'FINISHED', 'seqno': 29, 'user_id': '83011119', 'frozen_margin': 0.0, 'frozen_premium': 0.0, 'frozen_commission': 0.0}",
                str(order1))
