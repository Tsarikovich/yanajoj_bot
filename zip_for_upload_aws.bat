cd back/Lib/site-packages
7z a -r ../../../lambda.zip *
cd ../../../
cd src/
7z a ../lambda.zip *.py
cd ../
cd imgs/
7z a -r ../lambda.zip *
pause()