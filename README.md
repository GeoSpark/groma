ls
==

Surveying Calculation plug-in for QGIS

* Users' Guide: http://digikom.hu/SurveyingCalculation/usersguide.pdf
* Tutorial:  http://digikom.hu/SurveyingCalculation/tutorial.pdf
* Developers' guide: http://digikom.hu/SurveyingCalculation/devdoc.html

Uses PrettyTable to print pretty tables. Because of dependency fun when writing QGIS plugins,
I have just grabbed a copy of PrettyTable and put it in this repo, but credit should go to:
https://github.com/jazzband/prettytable and ultimately https://github.com/lmaurits/prettytable

I have disabled plotting for now because it seems to just crash QGIS 3.

Moved tests to the tests directory. But I've not done any cleanup on them yet.

TODO:
* Add more logging
* Output results to the QGIS log
* Turn message boxes to toasts
