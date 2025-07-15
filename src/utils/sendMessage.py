from src.utils.read_json import read_json
from src.utils.scheduler import get_subject_by_period

def sendMessage(idx, next_notice_time) -> None:
    """
    メッセージを送信する関数
    Args:
        idx (int): 時間目のインデックス
        next_notice_time (str): 次に通知を送る時間
    Returns:
        None
    """
    subject = get_subject_by_period(read_json("dataset/timetable.json"), "week", idx)
    
    if subject:
        message = f"次の授業は {subject} です。時間: {next_notice_time}"
    else:
        message = f"次の授業はまだ決まっていません。時間: {next_notice_time}"
    
    # ここでメッセージを送信する処理を実装
    print(message)  # 例としてコンソールに出力
    
