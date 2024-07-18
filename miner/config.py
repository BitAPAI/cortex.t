import argparse
from pathlib import Path
from os import environ, path
from sys import argv
from msgspec import yaml

import bittensor as bt


def check_config(cls, config: bt.config):
    bt.axon.check_config(config)
    bt.logging.check_config(config)
    full_path = Path(
        f'{config.logging.logging_dir}/{config.wallet.get("name", bt.defaults.wallet.name)}/'
        f'{config.wallet.get("hotkey", bt.defaults.wallet.hotkey)}/{config.miner.name}'
    ).expanduser()
    config.miner.full_path = str(full_path)
    full_path.mkdir(parents=True, exist_ok=True)


def get_config() -> bt.config:
    parser = argparse.ArgumentParser()
    parser.add_argument("--axon.port", type=int, default=8098, help="Port to run the axon on.")
    # External IP
    parser.add_argument("--axon.external_ip", type=str, default=bt.utils.networking.get_external_ip(), help="IP for the metagraph")
    # Subtensor network to connect to
    parser.add_argument(
        "--subtensor.network",
        default="finney",
        help="Bittensor network to connect to.",
    )
    # Chain endpoint to connect to
    parser.add_argument(
        "--subtensor.chain_endpoint",
        default="wss://entrypoint-finney.opentensor.ai:443",
        help="Chain endpoint to connect to.",
    )
    # Adds override arguments for network and netuid.
    parser.add_argument("--netuid", type=int, default=1, help="The chain subnet uid.")

    parser.add_argument(
        "--miner.root",
        type=str,
        help="Trials for this miner go in miner.root / (wallet_cold - wallet_hot) / miner.name ",
        default="~/.bittensor/miners/",
    )
    parser.add_argument(
        "--miner.name",
        type=str,
        help="Trials for this miner go in miner.root / (wallet_cold - wallet_hot) / miner.name ",
        default="Bittensor Miner",
    )

    # Run config.
    parser.add_argument(
        "--miner.blocks_per_epoch",
        type=str,
        help="Blocks until the miner sets weights on chain",
        default=100,
    )

    # Switches.
    parser.add_argument(
        "--miner.no_set_weights",
        action="store_true",
        help="If True, the miner does not set weights.",
        default=False,
    )
    parser.add_argument(
        "--miner.no_serve",
        action="store_true",
        help="If True, the miner doesnt serve the axon.",
        default=False,
    )
    parser.add_argument(
        "--miner.no_start_axon",
        action="store_true",
        help="If True, the miner doesnt start the axon.",
        default=False,
    )

    # Mocks.
    parser.add_argument(
        "--miner.mock_subtensor",
        action="store_true",
        help="If True, the miner will allow non-registered hotkeys to mine.",
        default=False,
    )

    # Adds subtensor specific arguments i.e. --subtensor.chain_endpoint ... --subtensor.network ...
    bt.subtensor.add_args(parser)

    # Adds logging specific arguments i.e. --logging.debug ..., --logging.trace .. or --logging.logging_dir ...
    bt.logging.add_args(parser)

    # Adds wallet specific arguments i.e. --wallet.name ..., --wallet.hotkey ./. or --wallet.path ...
    bt.wallet.add_args(parser)

    # Adds axon specific arguments i.e. --axon.port ...
    bt.axon.add_args(parser)

    # Activating the parser to read any command-line inputs.
    # To print help message, run python3 template/miner.py --help
    config = bt.config(parser)

    # Logging captures events for diagnosis or understanding miner's behavior.
    full_path = Path(f"{config.logging.logging_dir}/{config.wallet.name}/{config.wallet.hotkey}" f"/netuid{config.netuid}/miner").expanduser()
    config.full_path = str(full_path)
    # Ensure the directory for logging exists, else create one.
    full_path.mkdir(parents=True, exist_ok=True)
    return config


def check_endpoint_overrides() -> bool:
    """Check if the endpoint_overrides.yaml file exists in the current directory or script directory.

    Returns:
        bool: True if the file exists in either location, False otherwise."""

    file_path = path.join(path.dirname(__file__), "endpoint_overrides.yaml")
    script_dir_file_path = path.join(path.dirname(path.abspath(argv[0])), "endpoint_overrides.yaml")
    return path.exists(file_path) or path.exists(script_dir_file_path)


def get_endpoint_overrides() -> dict:
    """Get endpoint overrides from the endpoint_overrides.yaml file.

    Returns:
        dict: A dictionary containing the endpoint overrides.

    Raises:
        FileNotFoundError: If the endpoint_overrides.yaml file is not found.
        Exception: If an error occurs while reading the file.
    """

    if not check_endpoint_overrides():
        return {}
    try:
        with open(path.join(path.dirname(__file__), "endpoint_overrides.yaml"), "r") as f:
            return yaml.decode(f.read())
    except FileNotFoundError:
        with open(path.join(path.dirname(path.abspath(argv[0])), "endpoint_overrides.yaml"), "r") as f:
            return yaml.decode(f.read())
    except Exception:
        raise


def override_endpoint_keys() -> None:
    """Override endpoint keys based on the values provided in the endpoint_overrides.yaml file.

    Args:
        None

    Returns:
        None"""

    environ.update(get_endpoint_overrides().get("OVERRIDE_ENVIRONMENT_KEYS", {}))
