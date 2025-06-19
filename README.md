# PNNLSummer_2025
if you are reading this you succesfully copied the repo!

# Needed to run
to run this project you need to have ROOT installed (I am using Ubuntu but works for macos and windows) and Gegede installed, here are some link that are helpful with installation for both: https://github.com/brettviren/gegede(Gegede Installation)
https://www.youtube.com/watch?v=pmfM4Zq6OQU(ROOT installation, Ubuntu WSL)

# How to run
Once you finish installing everything you will be able to run the code , amke sure you are in the python directory! Once in there the command you need to run once you make chnages to any of the builders or its your first itial time building the geomtry is gegede-cli dunevd_v6.cfg -o dunevd_v10.gdml this will look in the dunvevd_v6.cfg file and do whats it gotta do then spit out a dgml file in this case it being called dunevd_v10.gdml. Once you make sure it worked and the file is there you can go ahead adn run the ROOT macro by compiling it with g++ Macro.cpp `root-config --cflags --libs` -lGdml -lGeom -o runGeo this will create the executable runGeo. To run this executable just do ./runGeo
