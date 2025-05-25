import sqlite3
from checker import Bot

if __name__ == '__main__':
    bot = Bot()
    conn = sqlite3.Connection('main.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM sites')
    sites = cur.fetchall()
    for site in sites:
        if site[1] == None or True:
            
            bot.run(site[0])
            cur.execute('''UPDATE sites SET 
                        Status_code = ?,
                        Description = ?,
                        SSL = ?,
                        Response_time = ?,
                        Browser_status =?,
                        Page_exists = ?,
                        Tag_count = ?,
                        Score = ? 
                        WHERE Domain = ?''', (
                            bot.status_code,
                            bot.description,
                            bot.ssl,
                            bot.response_time,
                            bot.browser_status,
                            bot.page_exists,
                            bot.dom_score,
                            bot.overall_score,
                            site[0])
                            )
            conn.commit()
           
