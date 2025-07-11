import discord
from src.database import DB_Done

def Done() -> :
    """
    doneメソッドの関数
    モーダルの表示 -> 未完了の課題を表示 -> 完了したかどうかをGUIで確認 -> 変更をDBに適用 
    """
