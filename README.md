# TransientX-Tools
## Using candsfile.py
candsfile.py can be used by running the command `python candsfile.py` with appropriate options. Next will be an overview of these options.

| Short | Long        | Type | Required | Description                                                                                                                                                            |
|-------|-------------|------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -n    | --number    | int  | yes      | Maximum amount of candidates to keep. Candidates will be eliminated based on low S/N ratio until the number of candidates is no longer above this value.               |
| -i    | --input     | str  | no       | Optionally specify an input file. If not specified, all .cands files in the current directory will be processed.                                                       |
| -o    | --output    | str  | no       | Give the output file a specific name. If not, the new file will get the _trunc suffix automatically.                                                                   |
|       | --dmc       | int  | no       | A DM threshold below which candidates will be eliminated without regard for their S/N value.                                                                           |
| -c    | --clean     |      | no       | Removes PNGs from eliminated candidates. This action cannot be undone and should only be performed on copies to prevent data loss.                                     |
| -w    | --overwrite |      | no       | Overwrites the original candidate file(s) with the output candidate file(s). This action cannot be undone and should only be performed on copies to prevent data loss. |
| -f    | --force     |      | no       | Skips the warning prompt when running either -c or -w. When used, the user will not be warned about potential data loss.                                               |
| -d    | --debug     |      | no       | Shows debug logging output.                                                                                                                                            |

## Using candidate file converter
### Environment
- Create a virtual environment using conda or venv.
- Activate the virtual environment and run `python -m pip -V` to confirm the environment is activated.
    - Caution: On some configurations `pip` defaults to the default or global environment. It is recommended to use `python -m pip` instead.
    - If `pip -V` shows the activated virtual environment, using `pip` works too.
- Ensure `git` is installed and clone this repo to a local folder using `git clone https://github.com/JoelvanIngen/TransientX-Tools/`
- Install required modules using `python -m pip install -r requirements.txt`
- Install `sigpyproc3` using `python -m pip install -U git+https://github.com/FRBs/sigpyproc3`

### Usage
Use `tx2fetch.py` by running `python tx2fetch.py -i [TransientX cands file] -f [filterbank file] (-o [Heimdall csv output location])`.

Usage can always be found running `python tx2fetch.py --help`.
