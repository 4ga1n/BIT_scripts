@echo off
:start
netsh interface show interface
echo ��������Ҫ�޸�ip�����������ƣ�todo����Ӧ��������ţ�
set /P netname=":"
echo ������ѡ�1.ʵ�����������2.У��������
set /P var=":"
if %var%==1 goto ip10
if %var%==2 goto ipdhcp
:ip10
netsh interface ip set address name=%netname% source=static address=10.1.112.15 mask= 255.255.254.0 gateway= 10.1.112.2
cmd /c netsh interface ip set dns name=%netname% source=static address=114.114.114.114
cmd /c netsh interface ip add dns name=%netname% address=218.30.118.60
ipconfig /flushdns
echo IP���óɹ�
echo ---------------------------------
goto start
:ipdhcp
netsh interface ip set address name=%netname% source=dhcp
cmd /c netsh interface ip set dns name=%netname% source=dhcp
ipconfig /flushdns
echo IP���óɹ�
goto start