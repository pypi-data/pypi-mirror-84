# tBTC.py

A python client to interact with the [tbtc](https://tbtc.network/) protocol.

tBTC Protocol version: `1.1.0`


## Setup:
1. Create & activate virtulenv (python 3.6+)
2. Install the library using pypi. 

    ```
    pip install tbtc
    ```

## Usage:
1. Initialize the tbtc system
    ```
    >>> from tbtc.session import init_web3
    >>> node_url = os.getenv("ROPSTEN_URL")
    >>> private_key = os.getenv("TBTC_PRIVATE_KEY")
    >>> w3 = init_web3(node_url)
    >>> version = "1.1.0"
    >>> t = TBTC(version, w3, 'testnet', private_key)
    ```

2. Get lot sizes
    ```
    >>> lot_sizes = t.get_available_lot_sizes()
    ```

3. Create a deposit contract
    ```
    >>> logs = t.create_deposit(lot_sizes[0])
    ```
    Example [txn](https://ropsten.etherscan.io/tx/0x23dbdbda025bfb41f00486b6b0994b2f271b7505b79738202b9940f81c374206) created the deposit [contract](https://ropsten.etherscan.io/address/0xd7Edcd864c79C54AEFD82636103BA263C361d49D)

4. Get the bitcoin address for depositing BTC
    ```
    >>> d = Deposit(
    ... t, 
    ... logs[0]['args']['_depositContractAddress'],
    ... logs[0]['args']['_keepAddress']
    ... )
    >>> address = d.get_signer_public_key()
    ```
    Example [txn](https://ropsten.etherscan.io/tx/0xadeee43cacd1d333d23d1445aceb91287e8680667fc4cff0c55382c2b8d37a77) retrieved the address: tb1q38yzl97hg0vnn4wf7srguwjnmlgfa30uq3nrwt


## Development:
1. Clone & enter the repo. `git clone https://github.com/ankitchiplunkar/tbtc.py.git`
2. Install required libraries. `pip install -r requirements.txt`

## Testing:
1. Run the tests locally 

    ```pytest -vv tests/```
