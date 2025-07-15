from datetime import date

def GetWeek() -> str:
    """
    現在の曜日を取得する関数
    Returns:
        str: 現在の曜日（例: "Monday", "Tuesday", ...）
    """
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = date.today()
    
    week = days[today.weekday()]
    return week  # 0=月, 1=火, ..., 6=日
