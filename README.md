
## Example usage of the frontend to the Cll compiler library

Create a file called **script.cll** with the following contents:

    if tx.value <= 25 * 10^18:
        stop
    elif contract.storage[tx.data[0]] or tx.data[0] < 1000:
        stop
    contract.storage[tx.data[0]] = tx.data[1]

Call the cllfrontend as following:

    python run.py -i script.cll > script.es

**-o** option will eventually be added to specify the output file

The resulting script.es file will look like this:

    TXVALUE PUSH 25 PUSH 10 PUSH 18 EXP MUL LE NOT PUSH 34 JMPI STOP PUSH 34 JMP PUSH 0 TXDATA SLOAD NOT PUSH 0 TXDATA PUSH 1000 LT NOT MUL NOT NOT PUSH 34 JMPI STOP PUSH 1 TXDATA PUSH 0 TXDATA SSTORE

That's about it.

**References:**

[Language Specification - Whitepaper](https://www.ethereum.org/whitepaper/ethereum.html#p421)

[Implementation - Github](https://github.com/ethereum/compiler/blob/master/cllcompiler.py)