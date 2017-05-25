import telegram
import wechat

tele = telegram.Telegram()
wechat.set_tele_instance(tele)
tele.run()

