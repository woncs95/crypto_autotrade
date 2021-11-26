import datetime
import math
import time

from Bitcoin_Tradebot.strategy.bullmarket_approximation import get_yesterday_ma5, is_over_ma5
from Bitcoin_Tradebot.strategy.volatility_breakout import get_target_price

from accountbalance import balance_btc, balance_usdt
from keyconnect import key_connect
from order import (buy_order, cancel_all_order, check_filled_order, sell_order,
                   sell_order_instant)
from telegram_alert import send_telegram_message
from ticker import get_ticker


async def enter_position(cur_price, buy_target_price, sell_target_price, position, over_ma5, surplus, key):
    # current price > buy target price and current prcie is over 5 day moving average
    if cur_price > buy_target_price and over_ma5:
        # price before today's trade
        surplus["before"] = await balance_usdt(key)

        # edit position as "we bought a coin already"
        position['type'] = True

        # calculate our btc target price and target amount
        amount = await btc_amount(cur_price, key)
        position['amount'] = amount

        # target price * target amount = our balance
        await buy_order("BTC_USDT", buy_target_price, amount, key)

        # send telegram message
        send_telegram_message(f"{amount} BTC for {cur_price} bought.")


async def exit_position(now, coin, position, cur_price, surplus, key):
    if position['type']:
        position['type'] = False
        position = await check_filled_order(coin, key, position)

        # if today trade(buy and sell order) already fulfilled or completely not fulfilled, cancel all orders
        if (position['buy_order'], position['sell_order']) and (not position['buy_order'], not position['sell_order']):
            await cancel_all_order(coin, key)
        elif position['buy_order'] and not position['sell_order']:
            amount_btc = await balance_btc(key)
            await sell_order_instant(coin, amount_btc, key)
            await cancel_all_order(coin, key)
        elif not position['buy_order'] and position['sell_order']:
            send_telegram_message("something is wrong in exiting position")

        # show our daily surplus
        surplus["after"] = await balance_usdt(key)
        after = surplus["after"]
        before = surplus["before"]
        begin = surplus["begin"]

        # send telegram message
        send_telegram_message(now)
        send_telegram_message(f"btc sold with {cur_price}.")
        send_telegram_message(f"balance now: {after}")
        send_telegram_message(f"daily surplus: {math.floor((after - before) * 100) / 100}USDT")
        send_telegram_message(f"total surplus: {math.floor((after - begin) * 100) / 100}USDT")
        send_telegram_message("- - - - - - - - - - - - - - -")

        # cancel all order
        await cancel_all_order(coin, key)
    else:
        send_telegram_message("No Investment Today")
        send_telegram_message("- - - - - - - - - - - - - - -")
        await cancel_all_order(coin, key)


def cal_amount(usdt_balance, cur_price):
    # portion = 1
    usdt_trade = usdt_balance  # portion
    amount = math.floor((usdt_trade * 1e6) / cur_price) / 1e6
    return amount


async def btc_amount(target_price, key):
    usdt_balance = await balance_usdt(key)
    amount = cal_amount(usdt_balance, target_price)
    return amount


async def invest_btc(op_mode, position, surplus):
    key = key_connect()

    # 현재 돈 기록
    surplus["begin"] = await balance_usdt(key)
    begin = surplus["begin"]
    send_telegram_message(f"your beginning balance is {math.floor(begin * 100) / 100} USDT")
    buy_target_price = 0
    sell_target_price = 0
    yesterday_ma5 = 0
    instrument = "BTC_USDT"
    print("initializing investment based on 'volatility break out' and 'bull market approximation...'")
    send_telegram_message("investment initializing...")
    while True:
        try:
            now = datetime.datetime.now(datetime.timezone.utc)
            # current price
            cur_price = get_ticker(instrument)

            # sell on the end of the day(UTC) and change position type as None
            if now.hour == 23 and now.minute == 50 and (0 <= now.second < 10):
                if op_mode and position['type']:
                    await exit_position(now, "BTC_USDT", position, cur_price, surplus, key)
                    op_mode = False

            # set daily target price
            if now.hour == 0 and now.minute == 0 and (20 <= now.second < 25):
                k = 0.5
                buy_target_price, sell_target_price = await get_target_price(instrument, k)
                op_mode = True
                send_telegram_message(f"buy_target_price: {buy_target_price}")
                send_telegram_message(f"sell_target_price: {sell_target_price}")

                # is it over ma5? true or false
                yesterday_ma5 = await get_yesterday_ma5(instrument)

            # over_ma5 = True / False
            if op_mode and position['type']:
                over_ma5 = await is_over_ma5(yesterday_ma5, cur_price)
                await enter_position(cur_price, buy_target_price, position, over_ma5, surplus, key)

            time.sleep(0.01)

        # usual error handling

        except IOError as e:
            send_telegram_message(e.args)
            send_telegram_message('Error occurred while opening the file.')
            break

        except ValueError as e:
            send_telegram_message(e.args)
            send_telegram_message('Non-numeric input detected.')
            break

        except ImportError as e:
            send_telegram_message(e.args)
            send_telegram_message('Unable to locate the module.')
            break

        except EOFError as e:
            send_telegram_message(e.args)
            send_telegram_message('Identified EOF error.')
            break

        except (KeyboardInterrupt, TypeError) as e:
            send_telegram_message(e.args)
            send_telegram_message('Wrong keyboard input.')
            break

        except KeyError as e:
            send_telegram_message(e.args)
            send_telegram_message('Wrong Key in Dataframe')
            break
