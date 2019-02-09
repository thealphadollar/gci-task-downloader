## GCITaskDown

Helps to download all the GCI tasks at once in JSON and csv format.

It can be used to download the list of tasks for this year and then upload the tasks the following year since the CSV is created in an upload-friendly manner.

NOTE: Please set your GCI token to `GCI_API_TOKEN` env variable.

## How to use?

Please follow the below steps to use the application.

NOTE: Clone the repository to your system before following the below instructions.

#### First Time

You need to have python3 and pip installed in your system.

- `pip install pipenv`
- `cd /to/project/directory/`
- `pipenv shell --three`
- `pipenv install` (use `pipenv install --dev` to install [GCI csv validator](https://github.com/Arthelon/gci-csv-validator/) as well)
- `python3 client.py --save-as [json/csv]`

#### Consecutive Usage

- `pipenv shell`
- `python3 client.py --save-as [json/csv]`

## Arguments Available

The client can be used with the following arguments (powered by [Click](https://click.palletsprojects.com/en/7.x/))

```text
Usage: client.py [OPTIONS]

Options:
  --verbose / --no-verbose  show debug information
  --save-as [json|csv]      format to save the tasks in  [required]
  --help                    Show this message and exit.

```

## Contributions And Improvements

Suggestions and improvements are warmly welcomed; kindly create a ticket in the issues section.