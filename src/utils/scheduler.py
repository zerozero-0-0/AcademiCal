from src.utils.read_json import read_json
import datetime

def get_subject_by_period(timeTable, week, period_num):
    for period_data in timeTable[week]:
        if period_data["period"] == period_num:
            return period_data["subject_name"]
    
    return None

def scheduler() -> tuple:
    """
    次に通知を送る時間を返す関数
    Args:
        None
    Returns:
        tuple: 次に通知を送る時間とその時間が何時間目か
    """
    
    timeTable = read_json("dataset/timetable.json")
    peroid = read_json("dataset/period.json")
    
    if not timeTable or not peroid:
        raise ValueError("タイムテーブルまたは期間のデータが読み込めません")
    
    current_hour = datetime.datetime.now().hour
    current_minute = datetime.datetime.now().minute
    
    next_notice_time = None
    idx = 1
    for i in range(1, 6):
        j = str(i)
        end_time_hour = int(peroid[j]["end_time"].split(':')[0])
        end_time_minute = int(peroid[j]["end_time"].split(':')[1])
        
        if next_notice_time is not None:
            break
        
        if current_hour == end_time_hour:
            if current_minute < end_time_minute:
                next_notice_time = f"{end_time_hour}:{end_time_minute}"
                idx = i
                
        if current_hour < end_time_hour:
            next_notice_time = f"{end_time_hour}:{end_time_minute}"
            idx = i
            
    
    if next_notice_time is None:
        next_notice_time = peroid['1']["end_time"]      
    
    return idx, next_notice_time
