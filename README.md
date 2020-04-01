# mica cLASS pipeline

This repository contains the main functions for the cLASS (Computational Linguistic Analysis of ScriptS) project.

The following flow diagram illustrates the different components we envision for the cLASS system. `Client Side` refers to the expected input to our system. `System side` is the backend computation processes. The `Output` includes main results, sheets and related visualizations.  

![drawing](https://docs.google.com/drawings/d/12w5iizScxpwlOGhFRsVGModb8Vhgzl0Jnpd3T5x5XpE/export/png)  
[Edit flow diagram here](https://docs.google.com/drawings/d/12w5iizScxpwlOGhFRsVGModb8Vhgzl0Jnpd3T5x5XpE/edit)


The [mica-text-script-parser](https://github.com/usc-sail/mica-text-script-parser/releases/tag/v0.0) is used to parse screenplays.

[Gspread](https://github.com/burnash/gspread) is used to create and share Google spreadsheets.

_micaclasssail_ Google account is used to store the spreadsheets and send emails.
