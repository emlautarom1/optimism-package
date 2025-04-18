import argparse
import json
import json
from functools import reduce

ROOT = "/network-data"


def lookup(dictionary, path):
    try:
        return reduce(lambda d, key: d[key], path, dictionary)
    except KeyError:
        return None


def merge_all(*dicts):
    def merge(left: dict, right: dict, path=[]):
        for key in right:
            if key in left:
                if isinstance(left[key], dict) and isinstance(right[key], dict):
                    merge(left[key], right[key], path + [str(key)])
                elif left[key] != right[key]:
                    # Prefer right over left
                    left[key] = right[key]
            else:
                left[key] = right[key]
        return left

    return reduce(merge, [{}, *dicts])


def filter_none(d):
    return {k: v for k, v in d.items() if v is not None}


def optional(v, f):
    if v is None:
        return None
    return f(v)


def to_nethermind_accounts(genesis):
    alloc = lookup(genesis, ["alloc"])

    result = {}
    for address, account in alloc.items():
        result[f"0x{address}"] = account

    return result


def to_nethermind_chainspec(l1, genesis, rollup, state):
    constants = {
        "L1BeaconGenesisSlotTime": {
            "mainnet": 1606824023,
            "sepolia": 1655733600,
        }
    }

    nethermind = {
        "engine": {
            "Optimism": {
                "params": {
                    "regolithTimestamp": "0x0",
                    "bedrockBlockNumber": hex(lookup(genesis, ["config", "bedrockBlock"])),
                    "canyonTimestamp": hex(lookup(genesis, ["config", "canyonTime"])),
                    "ecotoneTimestamp": hex(lookup(genesis, ["config", "ecotoneTime"])),
                    "fjordTimestamp": hex(lookup(genesis, ["config", "fjordTime"])),
                    "graniteTimestamp": hex(lookup(genesis, ["config", "graniteTime"])),
                    "holoceneTimestamp": hex(lookup(genesis, ["config", "holoceneTime"])),
                    "isthmusTimestamp": optional(lookup(genesis, ["config", "isthmusTime"]), hex),
                    "canyonBaseFeeChangeDenominator": lookup(genesis, ["config", "optimism", "eip1559DenominatorCanyon"]),
                    "l1FeeRecipient": "0x420000000000000000000000000000000000001A",
                    "l1BlockAddress": "0x4200000000000000000000000000000000000015",
                    "create2DeployerAddress": "0x13b0D85CcB8bf860b6b79AF3029fCA081AE9beF2",
                    "create2DeployerCode": "6080604052600436106100435760003560e01c8063076c37b21461004f578063481286e61461007157806356299481146100ba57806366cfa057146100da57600080fd5b3661004a57005b600080fd5b34801561005b57600080fd5b5061006f61006a366004610327565b6100fa565b005b34801561007d57600080fd5b5061009161008c366004610327565b61014a565b60405173ffffffffffffffffffffffffffffffffffffffff909116815260200160405180910390f35b3480156100c657600080fd5b506100916100d5366004610349565b61015d565b3480156100e657600080fd5b5061006f6100f53660046103ca565b610172565b61014582826040518060200161010f9061031a565b7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe082820381018352601f90910116604052610183565b505050565b600061015683836102e7565b9392505050565b600061016a8484846102f0565b949350505050565b61017d838383610183565b50505050565b6000834710156101f4576040517f08c379a000000000000000000000000000000000000000000000000000000000815260206004820152601d60248201527f437265617465323a20696e73756666696369656e742062616c616e636500000060448201526064015b60405180910390fd5b815160000361025f576040517f08c379a000000000000000000000000000000000000000000000000000000000815260206004820181905260248201527f437265617465323a2062797465636f6465206c656e677468206973207a65726f60448201526064016101eb565b8282516020840186f5905073ffffffffffffffffffffffffffffffffffffffff8116610156576040517f08c379a000000000000000000000000000000000000000000000000000000000815260206004820152601960248201527f437265617465323a204661696c6564206f6e206465706c6f790000000000000060448201526064016101eb565b60006101568383305b6000604051836040820152846020820152828152600b8101905060ff815360559020949350505050565b61014e806104ad83390190565b6000806040838503121561033a57600080fd5b50508035926020909101359150565b60008060006060848603121561035e57600080fd5b8335925060208401359150604084013573ffffffffffffffffffffffffffffffffffffffff8116811461039057600080fd5b809150509250925092565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b6000806000606084860312156103df57600080fd5b8335925060208401359150604084013567ffffffffffffffff8082111561040557600080fd5b818601915086601f83011261041957600080fd5b81358181111561042b5761042b61039b565b604051601f82017fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe0908116603f011681019083821181831017156104715761047161039b565b8160405282815289602084870101111561048a57600080fd5b826020860160208301376000602084830101528095505050505050925092509256fe608060405234801561001057600080fd5b5061012e806100206000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c8063249cb3fa14602d575b600080fd5b603c603836600460b1565b604e565b60405190815260200160405180910390f35b60008281526020818152604080832073ffffffffffffffffffffffffffffffffffffffff8516845290915281205460ff16608857600060aa565b7fa2ef4600d742022d532d4747cb3547474667d6f13804902513b2ec01c848f4b45b9392505050565b6000806040838503121560c357600080fd5b82359150602083013573ffffffffffffffffffffffffffffffffffffffff8116811460ed57600080fd5b80915050925092905056fea26469706673582212205ffd4e6cede7d06a5daf93d48d0541fc68189eeb16608c1999a82063b666eb1164736f6c63430008130033a2646970667358221220fdc4a0fe96e3b21c108ca155438d37c9143fb01278a3c1d274948bad89c564ba64736f6c63430008130033",
                }
            },
            "OptimismCL": merge_all(
                {
                    "L1BeaconGenesisSlotTime": lookup(constants, ["L1BeaconGenesisSlotTime", l1]),
                    "BatcherInboxAddress": lookup(rollup, ["batch_inbox_address"]),
                    "L2BlockTime": lookup(rollup, ["block_time"]),
                    "SeqWindowSize": lookup(rollup, ["seq_window_size"]),
                    "MaxSequencerDrift": lookup(rollup, ["max_sequencer_drift"]),
                    "SystemTransactionSender": "0xDeaDDEaDDeAdDeAdDEAdDEaddeAddEAdDEAd0001",
                    "SystemTransactionTo": "0x4200000000000000000000000000000000000015",
                    # TODO: Get nodes as arguments
                    "Nodes": [],
                },
                # Roles
                {
                    "SystemConfigOwner": lookup(state, ["appliedIntent", "chains", 0, "roles", "systemConfigOwner"]),
                    "ProxyAdminOwner": lookup(state, ["appliedIntent", "superchainRoles", "proxyAdminOwner"]),
                    "Guardian": lookup(state, ["appliedIntent", "superchainRoles", "guardian"]),
                    "Challenger": lookup(state, ["appliedIntent", "chains", 0, "roles", "challenger"]),
                    "Proposer": lookup(state, ["appliedIntent", "chains", 0, "roles", "proposer"]),
                    "UnsafeBlockSigner": lookup(state, ["appliedIntent", "chains", 0, "roles", "unsafeBlockSigner"]),
                    "BatchSubmitter": lookup(state, ["appliedIntent", "chains", 0, "roles", "batcher"]),
                },
                # Addresses
                {
                    "AddressManager": lookup(state, ["opChainDeployments", 0, "addressManagerAddress"]),
                    "L1CrossDomainMessengerProxy": lookup(state, ["opChainDeployments", 0, "l1CrossDomainMessengerProxyAddress"]),
                    "L1ERC721BridgeProxy": lookup(state, ["opChainDeployments", 0, "l1ERC721BridgeProxyAddress"]),
                    "L1StandardBridgeProxy": lookup(state, ["opChainDeployments", 0, "l1StandardBridgeProxyAddress"]),
                    "OptimismMintableERC20FactoryProxy": lookup(state, ["opChainDeployments", 0, "optimismMintableERC20FactoryProxyAddress"]),
                    "OptimismPortalProxy": lookup(state, ["opChainDeployments", 0, "optimismPortalProxyAddress"]),
                    "SystemConfigProxy": lookup(state, ["opChainDeployments", 0, "systemConfigProxyAddress"]),
                    "ProxyAdmin": lookup(state, ["opChainDeployments", 0, "proxyAdminAddress"]),
                    "AnchorStateRegistryProxy": lookup(state, ["opChainDeployments", 0, "anchorStateRegistryProxyAddress"]),
                    "DelayedWETHProxy": lookup(state, ["opChainDeployments", 0, "delayedWETHPermissionedGameProxyAddress"]),
                    "DisputeGameFactoryProxy": lookup(state, ["opChainDeployments", 0, "disputeGameFactoryProxyAddress"]),
                    "MIPS": lookup(state, ["implementationsDeployment", "mipsSingletonAddress"]),
                    "PermissionedDisputeGame": lookup(state, ["opChainDeployments", 0, "permissionedDisputeGameAddress"]),
                    "PreimageOracle": lookup(state, ["implementationsDeployment", "preimageOracleSingletonAddress"]),
                    "SuperchainConfig": lookup(state, ["superchainDeployment", "superchainConfigImplAddress"]),
                    # TODO: Figure out these parameters
                    "L2OutputOracleProxy": None,
                },
            ),
        },
        "params": {
            "chainId": hex(lookup(genesis, ["config", "chainId"])),
            "gasLimitBoundDivisor": "0x400",
            "accountStartNonce": "0x0",
            "maximumExtraDataSize": "0x20",
            "minGasLimit": "0x1388",
            "forkBlock": "0x0",
            "maxCodeSize": "0x6000",
            "maxCodeSizeTransition": "0x0",
            "eip150Transition": "0x0",
            "eip160Transition": "0x0",
            "eip161abcTransition": "0x0",
            "eip161dTransition": "0x0",
            "eip155Transition": "0x0",
            "eip140Transition": "0x0",
            "eip211Transition": "0x0",
            "eip214Transition": "0x0",
            "eip658Transition": "0x0",
            "eip145Transition": "0x0",
            "eip1014Transition": "0x0",
            "eip1052Transition": "0x0",
            "eip1283Transition": "0x0",
            "eip1283DisableTransition": "0x0",
            "eip152Transition": "0x0",
            "eip1108Transition": "0x0",
            "eip1344Transition": "0x0",
            "eip1884Transition": "0x0",
            "eip2028Transition": "0x0",
            "eip2200Transition": "0x0",
            "eip2565Transition": "0x0",
            "eip2929Transition": "0x0",
            "eip2930Transition": "0x0",
            "eip1559Transition": hex(lookup(genesis, ["config", "londonBlock"])),
            "eip1559FeeCollectorTransition": hex(lookup(genesis, ["config", "londonBlock"])),
            "feeCollector": "0x4200000000000000000000000000000000000019",
            "eip1559ElasticityMultiplier": hex(lookup(genesis, ["config", "optimism", "eip1559Elasticity"])),
            "eip1559BaseFeeMaxChangeDenominator": hex(lookup(genesis, ["config", "optimism", "eip1559Denominator"])),
            "eip3198Transition": hex(lookup(genesis, ["config", "londonBlock"])),
            "eip3529Transition": hex(lookup(genesis, ["config", "londonBlock"])),
            "eip3541Transition": hex(lookup(genesis, ["config", "londonBlock"])),
            # Shanghai
            "eip4895TransitionTimestamp": hex(lookup(genesis, ["config", "shanghaiTime"])),
            "eip3651TransitionTimestamp": hex(lookup(genesis, ["config", "shanghaiTime"])),
            "eip3855TransitionTimestamp": hex(lookup(genesis, ["config", "shanghaiTime"])),
            "eip3860TransitionTimestamp": hex(lookup(genesis, ["config", "shanghaiTime"])),
            # Cancun
            "eip1153TransitionTimestamp": hex(lookup(genesis, ["config", "cancunTime"])),
            "eip4788TransitionTimestamp": hex(lookup(genesis, ["config", "cancunTime"])),
            "eip4844TransitionTimestamp": hex(lookup(genesis, ["config", "cancunTime"])),
            "eip5656TransitionTimestamp": hex(lookup(genesis, ["config", "cancunTime"])),
            "eip6780TransitionTimestamp": hex(lookup(genesis, ["config", "cancunTime"])),
            # OP Forks
            "rip7212TransitionTimestamp": hex(lookup(genesis, ["config", "fjordTime"])),
            "opGraniteTransitionTimestamp": hex(lookup(genesis, ["config", "graniteTime"])),
            "opHoloceneTransitionTimestamp": hex(lookup(genesis, ["config", "holoceneTime"])),
            "opIsthmusTransitionTimestamp": optional(lookup(genesis, ["config", "isthmusTime"]), hex),
            "terminalTotalDifficulty": "0x0",
        },
        "genesis": filter_none(
            {
                "seal": {
                    "ethereum": {
                        "nonce": lookup(genesis, ["nonce"]),
                        "mixHash": lookup(genesis, ["mixHash"]),
                    }
                },
                "number": lookup(genesis, ["number"]),
                "difficulty": lookup(genesis, ["difficulty"]),
                "author": lookup(genesis, ["coinbase"]),
                "timestamp": lookup(genesis, ["timestamp"]),
                "parentHash": lookup(genesis, ["parentHash"]),
                "extraData": lookup(genesis, ["extraData"]),
                "gasLimit": lookup(genesis, ["gasLimit"]),
                "baseFeePerGas": lookup(genesis, ["baseFeePerGas"]),
                "stateRoot": lookup(rollup, ["genesis", "l2", "hash"]),
            }
        ),
        "nodes": [],  # TODO: Nodes
        "accounts": to_nethermind_accounts(genesis),
    }
    return nethermind


def main(network, chain_id, output):
    GENESIS = f"{ROOT}/genesis-{chain_id}.json"
    ROLLUP = f"{ROOT}/rollup-{chain_id}.json"
    STATE = f"{ROOT}/state.json"

    with open(GENESIS, "r") as f:
        genesis = json.load(f)

    with open(ROLLUP, "r") as f:
        rollup = json.load(f)

    with open(STATE, "r") as f:
        state = json.load(f)

    chainspec = to_nethermind_chainspec(network, genesis, rollup, state)

    with open(output, "w") as f:
        json.dump(chainspec, f, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nethermind Optimism Kurtosis compatibility layer")
    parser.add_argument("-n", "--network", default="mainnet", help="network name")
    parser.add_argument("-c", "--chain", default="2151908", help="chain id")
    parser.add_argument("-o", "--output", default=f"{ROOT}/GEN_chainspec-2151908.json", help="output file for the generated chainspec")
    args = parser.parse_args()

    main(args.network, args.chain, args.output)
