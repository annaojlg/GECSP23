from django.shortcuts import render
import json
from web3 import Web3, HTTPProvider

# Create your views here.
def index(request):
    return render(request, 'ethapp/index.html')

def eth_test(request):
    # set up web3 connection with Ganache
    ganache_url = 'http://127.0.0.1:8545'
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    abi = json.loads('''[{"constant":false,"inputs":[{"name":"_greeting","type":"string"}],"name":"setGreeting","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"greet","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"greeting","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]''')
    bytecode = "6060604052341561000f57600080fd5b6040805190810160405280600581526020017f48656c6c6f0000000000000000000000000000000000000000000000000000008152506000908051906020019061005a929190610060565b50610105565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106100a157805160ff19168380011785556100cf565b828001600101855582156100cf579182015b828111156100ce5782518255916020019190600101906100b3565b5b5090506100dc91906100e0565b5090565b61010291905b808211156100fe5760008160009055506001016100e6565b5090565b90565b61041a806101146000396000f300606060405260043610610057576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063a41368621461005c578063cfae3217146100b9578063ef690cc014610147575b600080fd5b341561006757600080fd5b6100b7600480803590602001908201803590602001908080601f016020809104026020016040519081016040528093929190818152602001838380828437820191505050505050919050506101d5565b005b34156100c457600080fd5b6100cc6101ef565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561010c5780820151818401526020810190506100f1565b50505050905090810190601f1680156101395780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b341561015257600080fd5b61015a610297565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561019a57808201518184015260208101905061017f565b50505050905090810190601f1680156101c75780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b80600090805190602001906101eb929190610335565b5050565b6101f76103b5565b60008054600181600116156101000203166002900480601f01602080910402602001604051908101604052809291908181526020018280546001816001161561010002031660029004801561028d5780601f106102625761010080835404028352916020019161028d565b820191906000526020600020905b81548152906001019060200180831161027057829003601f168201915b5050505050905090565b60008054600181600116156101000203166002900480601f01602080910402602001604051908101604052809291908181526020018280546001816001161561010002031660029004801561032d5780601f106103025761010080835404028352916020019161032d565b820191906000526020600020905b81548152906001019060200180831161031057829003601f168201915b505050505081565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061037657805160ff19168380011785556103a4565b828001600101855582156103a4579182015b828111156103a3578251825591602001919060010190610388565b5b5090506103b191906103c9565b5090565b602060405190810160405280600081525090565b6103eb91905b808211156103e75760008160009055506001016103cf565b5090565b905600a165627a7a7230582006f39b9b9b558a328403f9c048af30519c79e6536660d7660e8002af27f240930029"
    
    # set pre-funded account as sender
    web3.eth.defaultAccount = web3.eth.accounts[0]
    
    # instantiate and deploy contract
    Greeter = web3.eth.contract(abi=abi, bytecode=bytecode)
    
    # submit the transaction that deploys the contract
    tx_hash = Greeter.constructor().transact()
    
    # wait for the transaction that deploys the contract
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    
    # create the contract instance with newly-deployed address
    contract = web3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=abi
    )
    
    tx_receipt = tx_receipt.contractAddress
    print(tx_receipt)
    
    contract_greet_call = 'Default contract greeting: {}'.format(contract.functions.greet().call())
    print(contract_greet_call)
    
    # update the greeting
    tx_hash = contract.functions.setGreeting('Hello - SETTING A NEW GREETING!').transact()
    print(tx_hash)
    
    # wait for the transaction to be minded
    web3.eth.waitForTransactionReceipt(tx_hash)
    
    updated_contract_greeting = 'Updated contract greeting: {}'.format(contract.functions.greet().call())
    print(updated_contract_greeting)
    
    message = "Ethereum transaction completed"
    
    return render(request, 'ethapp/eth_test.html', {'message': message, 'tx_receipt': tx_receipt, 'contract_greet_call': contract_greet_call, 'tx_hash': tx_hash, 'updated_contract_greeting': updated_contract_greeting})

def eth_hello(request):
    # set up Web3 connection with Ganache
    ganache_url = "http://127.0.0.1:8545"
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    abi = json.loads('''[
	{
		"constant": true,
		"inputs": [],
		"name": "sayHello",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "constructor"
	}
    ]''')
    bytecode = "608060405234801561001057600080fd5b5061013f806100206000396000f3fe608060405260043610610041576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063ef5fb05b14610046575b600080fd5b34801561005257600080fd5b5061005b6100d6565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561009b578082015181840152602081019050610080565b50505050905090810190601f1680156100c85780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b60606040805190810160405280601581526020017f48656c6c6f20576f726c6420457468657265756d21000000000000000000000081525090509056fea165627a7a723058207ca63dcec98fa6ba34f159470ebfa03f609c2000303ebecc1d1a660de4c31db40029"

    # set pre-funded account as sender
    web3.eth.defaultAccount = web3.eth.accounts[0]
    
    # instantiate and deploy the contract
    Greeter = web3.eth.contract(abi=abi, bytecode=bytecode)
    
    # submit the transaction that deploys the contract
    tx_hash = Greeter.constructor().transact()
    
    # wait for the transaction to be mined, get the transaction receipt
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    
    # Create the contract instance with newly deployed address
    contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    tx_receipt = tx_receipt.contractAddress
    print(tx_receipt)
    
    # call contract function (not persisted to blockchain)
    message = contract.functions.sayHello().call()
    print(message)
    
    return render(request, 'ethapp/eth_hello.html', { 'message': message })
    
    
