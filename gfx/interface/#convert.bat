@echo off
for /r %%a in (*.png) do magick mogrify -format dds -define dds:compression=none "%%~a"