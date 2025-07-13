from logging import raiseExceptions
from os import read
from src.utils.read_json import read_json

def scheduler() -> str:
    """
    次に通知を送る時間を返す関数
    Args:
        None
    Returns:
        str: 次に通知を送る時間
    """
    
    timeTable = read_json(".dataset/timetable.json")
    peroid = read_json(".dataset/period.json")
    
    if not timeTable or not peroid:
        raise ValueError("タイムテーブルまたは期間のデータが読み込めません")
