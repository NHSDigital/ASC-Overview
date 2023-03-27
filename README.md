# Adult Social Care Overview
This report brings together the latest data collected by NHS Digital across different aspects of adult social care supported by local authorities. It aims to produce an insightful and coherent narrative about the trends in adult social care in England.

The report looks at data collected by NHS Digital from local authorities, typically spanning the time period from 2015-16 up to the latest available data.

# Initial package set up

Run the following command to set up your environment correctly **from the root directory**

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If, while developing this package, you change the installed packages, please update the environment file using

```
pip list --format=freeze > requirements.txt
```

## VSCode specific setup

For Visual Studio Code it is necessary that you change your default interpreter to be the virtual environment you just created `.venv`. To do this use the shortcut `Ctrl-Shift-P`, search for `Python: Select interpreter` and select `.venv` from the list.

# Git Hook Setup

Please running the following command to setup the Git Hooks.

```
python .\scripts\setup-hooks.py
```

You will now be prompted when committing to add a JIRA ticket number to your commit message.

**Please do not use the VS Code Git Tab to commit as this will no longer work.**

_However, you can use it for adding files to be committed._

# Running the code

Please check that the settings, including the path to the input files, are correct in `ascs/params.py`.

You can then create the publication (from the base directory) using

```
python -m asc_overview.create_publication
```

You can run the tests on the repository using (from the base directory)

```
pytest
```

# Package structure

The main steps of the code are documented in `ascs_overview/create_publication.py`

# Important things to know

## Running for next year

Create a new params file in the `params_json` folder by duplicating the previous year's json file. Update the parameters accordingly. Be wary of the cell references as these may need to be changed if the data source publications change. You will also need to output cell references so that the timeseries data is outputted in the correct place. The template excel file may also need to be changed to reflect the updates of the previous year.

# Link to the publication

Report:
https://digital.nhs.uk/data-and-information/publications/statistical/adult-social-care-statistics-in-england/an-overview

# Authors
Adam Carruthers, Amaan Ibn-Nasar, Raman Chahal

Repo Owner Contact Details: raman.chahal1@nhs.net

# Licence

The Personal Social Services Adult Social Care Overview publication codebase is released under the MIT License.
The documentation is © Crown copyright and available under the terms of the Open Government 3.0 licence.
