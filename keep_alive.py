from threading import Thread
import time
import requests

def ping_loop():
    while True:
        try:
            # 自分のRender URLやヘルスチェック用エンドポイントに定期アクセス（任意）
            time.sleep(600)  # 10分おき
        except Exception:
            pass

def keep_alive():
    t = Thread(target=ping_loop)
    t.daemon = True
    t.start()
