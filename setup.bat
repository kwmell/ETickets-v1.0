@echo off
if not exists "transcripts" (
 mkdir transcripts
 goto a
) ELSE (goto a)
:a
pip install os
pip install discord