import config
from db import db
from datetime import datetime


def get_client_deals():
    """
    Get client deals.

    Args:
        client: Client name.
        account_no: Account number.
        delay: Delay in seconds.
        exceptions: Exceptions.

    Returns:
        A list of deals.
    """

    # Get the parameters from the request.
    client = request.args.get("client")
    account_no = request.args.get("account_no")
    delay = request.args.get("delay", type=int)
    exceptions = request.args.get("exceptions", default="0")

    # Validate the parameters.
    if not all([client, account_no, delay]):
        return "-1<br>invalid parameter format"

    # Create a db object.
    db = db()
    deals = []
    error = ""
    id = db.get_client_deals(client, account_no, delay, exceptions, deals, error)
    if id < 0:
        return f"{id}<br>{error}"
    else:
        deals_count = len(deals)
        print(f"{deals_count}<br>{deals_count} deals found<br>")
        for deal in deals:
            date = datetime.now()
            date2 = datetime.strptime(deal["catch_time"], "%Y-%m-%d %H:%M:%S")
            late = date.timestamp() - date2.timestamp()
            deal_str = ""
            status = int(deal["status"])
            if status == config.new_order:
                deal_str = f"{config.new_order},{deal['id']},{late},{deal['type']},"
                deal_str += f"{deal['lot']},{deal['open_price']},{deal['sl']},"
                deal_str += f"{deal['tp']},{deal['symbol']},{deal['balance']},"
                deal_str += f"{deal['equity']}<br>"
            elif status == config.close_order:
                deal_str = f"{config.close_order},{deal['id']},{late},{deal['cld_ticket']},"
                deal_str += f"{deal['close_price']}<br>"
            elif status == config.delete_order:
                deal_str = f"{config.delete_order},{deal['id']},{late},{deal['cld_ticket']}<br>"
            elif status == config.modify_order:
                deal_str = f"{config.modify_order},{deal['id']},{late},{deal['cld_ticket']},"
                deal_str += f"{deal['open_price']},{deal['sl']},{deal['tp']}<br>"
            elif status == config.sub_order:
                deal_str = f"{config.sub_order},{deal['id']},{late},{deal['cld_ticket']},"
                deal_str += f"{deal['lot']},{deal['old_lot']}<br>"
            print(deal_str)
        return deals
