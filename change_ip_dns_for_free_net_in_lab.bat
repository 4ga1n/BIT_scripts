@echo off
:start
netsh interface show interface
echo 请输入需要修改ip的网络借口名称（todo，对应的数字序号）
set /P netname=":"
echo 请输入选项（1.实验室免费网；2.校内网）：
set /P var=":"
if %var%==1 goto ip10
if %var%==2 goto ipdhcp
:ip10
netsh interface ip set address name=%netname% source=static address=10.1.112.15 mask= 255.255.254.0 gateway= 10.1.112.2
cmd /c netsh interface ip set dns name=%netname% source=static address=114.114.114.114
cmd /c netsh interface ip add dns name=%netname% address=218.30.118.60
ipconfig /flushdns
echo IP设置成功
echo ---------------------------------
goto start
:ipdhcp
netsh interface ip set address name=%netname% source=dhcp
cmd /c netsh interface ip set dns name=%netname% source=dhcp
ipconfig /flushdns
echo IP设置成功
goto start