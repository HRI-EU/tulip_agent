# robo eval


## Setup

### Automatic
Run the setup script: `bash setup.sh` \
Only necessary once; automatically starts the interactive mode

### Manual
1. Clone the AttentiveSupport repo: `git@github.com:HRI-EU/AttentiveSupport.git` - it comes with a simulator and python bindings for tools
2. Build the AttentiveSupport repo: `cd AttentiveSupport && bash build.sh`
3. Copy the extended tools to the robo_eval directory: `cp src/tools.py ../tools.py`
4. Adapt the paths in the system setup in `tools.py` as follows:
    ```python
    with open(Path(__file__).parent.resolve() / "AttentiveSupport" / "src" / "config.yaml", "r") as config:
        config_data = yaml.safe_load(config)
        SMILE_WS_PATH = Path(__file__).parent.resolve() / "AttentiveSupport" / config_data["install"]
        print(f"{SMILE_WS_PATH=}")
    ```


## Run
1. Activate the `tulip_agent` venv from `robo_eval`: `source ../../../.venv/bin/activate`
2. Run `robo_eval.py` in interactive mode from `robo_eval`: `python -i robo_eval.py`


## Example
In the interactive mode, run, e.g.: `tulip_agent.query("hand the glass_blue over to Felix")`

![Examples](../../../docs/static/images/robot-examples.png)
