#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import json
import os
import random
import unittest
from datetime import datetime
from tqsdk.test.api.helper import MockInsServer, MockServer
from tqsdk import TqApi, TqBacktest, utils


class TestMdBasic(unittest.TestCase):
    """
    测试TqApi行情相关函数基本功能, 以及TqApi与行情服务器交互是否符合设计预期

    注：
    1. 在本地运行测试用例前需设置运行环境变量(Environment variables), 保证api中dict及set等类型的数据序列在每次运行时元素顺序一致: PYTHONHASHSEED=32
    2. 若测试用例中调用了会使用uuid的功能函数时（如insert_order()会使用uuid生成order_id）,
        则：在生成script文件时及测试用例中都需设置 utils.RD = random.Random(x), 以保证两次生成的uuid一致, x取值范围为0-2^32
    3. 对盘中的测试用例（即非回测）：因为TqSim模拟交易 Order 的 insert_date_time 和 Trade 的 trade_date_time 不是固定值，所以改为判断范围。
        盘中时：self.assertAlmostEqual(1575292560005832000 / 1e9, order1.insert_date_time / 1e9, places=1)
        回测时：self.assertEqual(1575291600000000000, order1.insert_date_time)
    """

    def setUp(self):
        self.ins = MockInsServer()
        os.environ["TQ_INS_URL"] = f"http://127.0.0.1:{self.ins.port}/t/md/symbols/2020-09-15.json"
        os.environ["TQ_AUTH_URL"] = f"http://127.0.0.1:{self.ins.port}"
        self.mock = MockServer(md_url_character="nfmd")

    def tearDown(self):
        self.ins.close()
        self.mock.close()

    # 获取行情测试

    # @unittest.skip("无条件跳过")
    def test_get_quote_normal(self):
        """
        获取行情报价

        """
        # 预设服务器端响应
        utils.RD = random.Random(4)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.mock.run(os.path.join(dir_path, "log_file", "test_md_basic_get_quote_normal.script.lzma"))
        self.md_url = f"ws://127.0.0.1:{self.mock.md_port}/"
        self.td_url = f"ws://127.0.0.1:{self.mock.td_port}/"
        # 获取行情
        api = TqApi(auth="tianqin,tianqin", _td_url=self.td_url, _md_url=self.md_url)
        q = api.get_quote("SHFE.cu2101")
        self.assertEqual(q.datetime, "2020-10-30 10:14:59.500001")
        self.assertEqual(q.ask_price1, 51420.0)
        self.assertEqual(q.ask_volume1, 6)
        self.assertEqual(q.bid_price1, 51410.0)
        self.assertEqual(q.bid_volume1, 2)
        self.assertEqual(q.last_price, 51420.0)
        self.assertEqual(q.highest, 51510.0)
        self.assertEqual(q.lowest, 51180.0)
        self.assertEqual(q.open, 51210.0)
        self.assertNotEqual(q.close, q.close)  # q.close is nan
        self.assertEqual(q.average, 51339.144929)
        self.assertEqual(q.volume, 19858)
        self.assertEqual(q.amount, 5097463700.0)
        self.assertEqual(q.open_interest, 70724)
        self.assertNotEqual(q.settlement, q.settlement)
        self.assertEqual(q.upper_limit, 54510.0)
        self.assertEqual(q.lower_limit, 48340)
        self.assertEqual(q.pre_open_interest, 70303)
        self.assertEqual(q.pre_settlement, 51430.0)
        self.assertEqual(q.pre_close, 51540.0)
        self.assertEqual(q.price_tick, 10)
        self.assertEqual(q.price_decs, 0)
        self.assertEqual(q.volume_multiple, 5)
        self.assertEqual(q.max_limit_order_volume, 500)
        self.assertEqual(q.max_market_order_volume, 0)
        self.assertEqual(q.min_limit_order_volume, 0)
        self.assertEqual(q.min_market_order_volume, 0)
        self.assertEqual(q.underlying_symbol, "")
        self.assertTrue(q.strike_price != q.strike_price)  # 判定nan
        self.assertEqual(q.expired, False)
        self.assertEqual(q.ins_class, "FUTURE")
        # 这两个字段不是对用户承诺的字段，api 中调用 _symbols_to_quotes 只有 objs.quote 里说明的字段
        # self.assertEqual(q.margin, 18249.0)
        # self.assertEqual(q.commission, 13.035)
        self.assertEqual(repr(q.trading_time.day),
                         "[['09:00:00', '10:15:00'], ['10:30:00', '11:30:00'], ['13:30:00', '15:00:00']]")
        self.assertEqual(repr(q.trading_time.night), "[['21:00:00', '25:00:00']]")
        self.assertEqual(q.expire_datetime, 1610694000.0)
        self.assertEqual(q.delivery_month, 1)
        self.assertEqual(q.delivery_year, 2021)
        self.assertEqual(q.instrument_id, "SHFE.cu2101")
        self.assertEqual(q.ask_price2, 51430.0)
        self.assertEqual(q.ask_volume2, 6)
        self.assertEqual(q.ask_price3, 51440.0)
        self.assertEqual(q.ask_volume3, 15)
        self.assertEqual(q.ask_price4, 51450.0)
        self.assertEqual(q.ask_volume4, 23)
        self.assertEqual(q.ask_price5, 51460)
        self.assertEqual(q.ask_volume5, 11)
        self.assertEqual(q.bid_price2, 51400.0)
        self.assertEqual(q.bid_volume2, 4)
        self.assertEqual(q.bid_price3, 51390.0)
        self.assertEqual(q.bid_volume3, 4)
        self.assertEqual(q.bid_price4, 51380.0)
        self.assertEqual(q.bid_volume4, 58)
        self.assertEqual(q.bid_price5, 51370)
        self.assertEqual(q.bid_volume5, 37)

        # 其他取值方式
        self.assertEqual(q["pre_close"], 51540.0)
        self.assertEqual(q.get("pre_settlement"), 51430.0)
        self.assertEqual(q.get("highest"), 51510.0)
        self.assertEqual(q.get("lowest"), 51180.0)
        self.assertEqual(q["open"], 51210.0)
        self.assertNotEqual(q["close"], q["close"])
        # 报错测试
        self.assertRaises(Exception, api.get_quote, "SHFE.au2199")
        self.assertRaises(KeyError, q.__getitem__, "ask_price6")

        api.close()

    def test_get_kline_serial(self):
        """
        获取K线数据
        """
        # 预设服务器端响应
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.mock.run(os.path.join(dir_path, "log_file", "test_md_basic_get_kline_serial.script.lzma"))
        self.md_url = f"ws://127.0.0.1:{self.mock.md_port}/"
        self.td_url = f"ws://127.0.0.1:{self.mock.td_port}/"

        # 测试: 获取K线数据
        utils.RD = random.Random(4)
        api = TqApi(auth="tianqin,tianqin", _td_url=self.td_url, _md_url=self.md_url)
        klines = api.get_kline_serial("SHFE.cu2105", 10)
        self.assertEqual(klines.iloc[-1].close, 51730.0)
        self.assertEqual(klines.iloc[-1].id, 307100)
        self.assertEqual(klines.iloc[-2].id, 307099)
        self.assertEqual(klines.iloc[-1].datetime, 1.60402592e+18)
        self.assertEqual(klines.iloc[-1].open, 51730)
        self.assertEqual(klines.iloc[-1].volume, 0)
        self.assertEqual(klines.iloc[-1].open_oi, 9000)
        self.assertEqual(klines.iloc[-1].duration, 10)
        # 其他取值方式
        self.assertEqual(klines.duration.iloc[-1], 10)
        self.assertEqual(klines.iloc[-1]["duration"], 10)
        self.assertEqual(klines["duration"].iloc[-1], 10)
        # 报错测试
        self.assertRaises(Exception, api.get_kline_serial, "SHFE.au1999", 10)
        self.assertRaises(AttributeError, klines.iloc[-1].__getattribute__, "dur")
        self.assertRaises(KeyError, klines.iloc[-1].__getitem__, "dur")
        api.close()

    def test_get_tick_serial(self):
        """
        获取tick数据
        """
        # 预设服务器端响应
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.mock.run(os.path.join(dir_path, "log_file", "test_md_basic_get_tick_serial.script.lzma"))
        self.md_url = f"ws://127.0.0.1:{self.mock.md_port}/"
        self.td_url = f"ws://127.0.0.1:{self.mock.td_port}/"
        # 测试: 获取tick数据
        utils.RD = random.Random(4)
        api = TqApi(auth="tianqin,tianqin", _td_url=self.td_url, _md_url=self.md_url)
        ticks = api.get_tick_serial("SHFE.cu2105")
        self.assertEqual(ticks.iloc[-1].id, 915924)
        self.assertEqual(ticks.iloc[-1].datetime, 1.6040259605e+18)
        self.assertEqual(ticks.iloc[-1].last_price, 51730.0)
        self.assertEqual(ticks.iloc[-1].average, 51625.26946)
        self.assertEqual(ticks.iloc[-1].highest, 51740.0)
        self.assertEqual(ticks.iloc[-1].lowest, 51460.0)
        self.assertEqual(ticks.iloc[-1].ask_price1, 51750.0)
        self.assertEqual(ticks.iloc[-1].ask_volume1, 1)
        self.assertEqual(ticks.iloc[-1].bid_price1, 51710.0)
        self.assertEqual(ticks.iloc[-1].bid_volume1, 11)
        self.assertEqual(ticks.iloc[-1].volume, 167)
        self.assertEqual(ticks.iloc[-1].amount, 43107100.0)
        self.assertEqual(ticks.iloc[-1].open_interest, 9000)
        self.assertEqual(ticks.iloc[-1].duration, 0)
        # 其他调用方式
        self.assertEqual(ticks.open_interest.iloc[-1], 9000)
        self.assertEqual(ticks["open_interest"].iloc[-2], 9000)
        self.assertEqual(ticks.iloc[-1]["ask_price1"], 51750)
        # 报错测试
        self.assertRaises(Exception, api.get_tick_serial, "SHFE.au1999")
        self.assertRaises(AttributeError, ticks.iloc[-1].__getattribute__, "dur")
        self.assertRaises(KeyError, ticks.iloc[-1].__getitem__, "dur")
        api.close()

    def test_get_kline_serial_update(self):
        """
        获取K线数据, 行情应该随着 api.wait_update 一直更新时间
        """
        # 预设服务器端响应
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.mock.run(os.path.join(dir_path, "log_file", "test_md_basic_get_kline_serial_update.script.lzma"))
        self.md_url = f"ws://127.0.0.1:{self.mock.md_port}/"
        self.td_url = f"ws://127.0.0.1:{self.mock.td_port}/"

        # 测试: 获取K线数据
        utils.RD = random.Random(4)
        api = TqApi(backtest=TqBacktest(datetime(2020, 6, 2), datetime(2020, 6, 3)),
                    auth="tianqin,tianqin", _td_url=self.td_url, _md_url=self.md_url)

        quote = api.get_quote("SHFE.rb2009")
        df = api.get_kline_serial("SHFE.rb2009", 1, 10)

        self.assertEqual(quote["datetime"], "2020-06-01 22:59:59.999999")
        self.assertEqual(df["datetime"].iloc[-1], 1.591023599e+18)

        api.wait_update()
        df['ema5'] = df['close'].rolling(5, min_periods=1).mean()
        df.loc[df["ema5"] > 2.5, 'duo'] = 1
        self.assertEqual(quote["datetime"], "2020-06-02 09:00:00.000000")
        self.assertEqual(df["datetime"].iloc[-1], 1.5910596e+18)

        api.wait_update()
        df['ema5'] = df['close'].rolling(5, min_periods=1).mean()
        df.loc[df["ema5"] > 2.5, 'duo'] = 1
        self.assertEqual(quote["datetime"], "2020-06-02 09:00:00.999999")
        self.assertEqual(df["datetime"].iloc[-1], 1.5910596e+18)

        api.wait_update()
        df['ema5'] = df['close'].rolling(5, min_periods=1).mean()
        df.loc[df["ema5"] > 2.5, 'duo'] = 1
        self.assertEqual(quote["datetime"], "2020-06-02 09:00:01.000000")
        self.assertEqual(df["datetime"].iloc[-1], 1.591059601e+18)

        api.close()

