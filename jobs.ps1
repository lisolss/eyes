Remove-Job *
#测试计时开始
$start_time = (Get-Date)

Start-Job -ScriptBlock {python D:\Code\code\eyes\main.py rk; } -Name "rk"
Start-Job -ScriptBlock {python D:\Code\code\eyes\main.py rttoday; } -Name "rttoday"


$taskCount = 2
while($taskCount -gt 0)
{
    foreach($job in Get-Job)
    {
        $state = [string]$job.State
        if($state -eq "Completed")
        {   
            Write-Host($job.Name + " 已经完成")
            Receive-Job $job
            $taskCount--
            Remove-Job $job
        }
    }
    sleep 1
}
"所有任务已完成"
 
Start-Job -ScriptBlock {python D:\Code\code\eyes\main.py summary_ticks; } -Name "myJob2"
$taskCount = 2
while($taskCount -gt 0)
{
    foreach($job in Get-Job)
    {
        $state = [string]$job.State
        if($state -eq "Completed")
        {   
            Write-Host($job.Name + " 已经完成")
            Receive-Job $job
            $taskCount--
            Remove-Job $job
        }
    }
    sleep 1
}
"所有任务已完成"
#得出任务运行的时间
(New-TimeSpan $start_time).totalseconds