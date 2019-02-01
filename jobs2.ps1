$start_time = (Get-Date)

python D:\Code\code\eyes\main.py rt
python D:\Code\code\eyes\main.py rk
python D:\Code\code\eyes\main.py summary_ticks
python D:\Code\code\eyes\main.py summary_class

"所有任务已完成"
#得出任务运行的时间
(New-TimeSpan $start_time).totalseconds