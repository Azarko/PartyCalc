IF EXIST "WIN" RD /S /Q "win"
@MKDIR win
@CD win
pyinstaller --noconfirm --onefile --windowed  "../PartyCalc/gui.py"
@COPY dist\gui.exe PartyCalc.exe
@RD /S /Q "build"
@RD /S /Q "dist"
@DEL gui.spec
@cd ../
