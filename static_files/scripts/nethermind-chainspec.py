import argparse

ROOT = "/network-data"


def main(network, chain_id, output):
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nethermind Optimism Kurtosis compatibility layer")
    parser.add_argument("-n", "--network", default="mainnet", help="network name")
    parser.add_argument("-c", "--chain", default="2151908", help="chain id")
    parser.add_argument("-o", "--output", default=f"{ROOT}/GEN_chainspec-2151908.json", help="output file for the generated chainspec")
    args = parser.parse_args()

    main(args.network, args.chain, args.output)
