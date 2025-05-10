from datetime import datetime
import pytz
from GetData.changehistorydata import get_changehistorydata

def history_update(cur, conn, table, loc, subloc, act, ori, upd):
    from Web_Page.login_page import get_username

    # Set up new primary key
    changehistorydata = get_changehistorydata(cur)

    if len(changehistorydata) == 0:
        new_change_id = "C001"
    else:
        current_change = changehistorydata['ChangeID'].iloc[-1]

        prefix = ''.join(filter(str.isalpha, current_change))
        number = ''.join(filter(str.isdigit, current_change))

        new_number = str(int(number) + 1).zfill(len(number))
        new_change_id = prefix + new_number

    ori = str(ori)
    upd = str(upd)

    username = get_username()

    # Thailand timezone
    tz_th = pytz.timezone("Asia/Bangkok")
    now_th = datetime.now(pytz.utc).astimezone(tz_th)
    date = now_th.date()
    now = now_th.strftime("%H:%M:%S")

    cur.execute("""
        INSERT INTO history_change (
            changeid, username, selected_table, location, sublocation, action,
            original_data, updated_data, date_change, time_change
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (new_change_id, username, table, loc, subloc, act, ori, upd, date, now))
    conn.commit()
