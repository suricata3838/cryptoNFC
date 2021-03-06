import numpy
import json


class Transaction:
    def __init__(self, accountID, tag, payload):
        self.flag = True
        self.accountID = accountID
        self.tag = tag
        self.payload = payload

    def Sign(self, private_key):
        # the message to be signed is the uint64(0) as little endian bytes +
        # tag + payload appended together as bytes
        signstr = bytes.fromhex("0000000000000000") + bytes.fromhex("%02x" %
                                                                    self.tag) + bytes.fromhex(self.payload.Build())
        self.signature = private_key.sign(signstr)
        return self

    def Build(self):
        txn = dict()
        txn["sender"] = self.accountID
        txn["tag"] = self.tag
        txn["payload"] = self.payload.Build()
        signaturestr = str()
        for ch in self.signature:
            signaturestr += "%02x" % ch
        txn["signature"] = signaturestr
        return json.dumps(txn)


class Payload:
    def __init__(self, recipientID, numPERLSSent, gasLimit, gasDeposit, functionName, functionPayload):
        self.recipientID = recipientID
        self.numPERLSSent = numpy.uint64(numPERLSSent)
        self.gasLimit = numpy.uint64(gasLimit)
        self.gasDeposit = numpy.uint64(gasDeposit)
        self.functionName = functionName
        self.functionPayload = functionPayload

    def Build(self):
        ret = str()
        ret += self.recipientID
        ret += "%016x" % self.numPERLSSent.newbyteorder()
        ret += "%016x" % self.gasLimit.newbyteorder()
        ret += "%016x" % self.gasDeposit.newbyteorder()

        # prefix the length
        ret += "%08x" % numpy.int32(len(self.functionName)).newbyteorder()
        for ch in self.functionName:
            ret += "%02x" % ord(ch)
        payload = self.functionPayload.Build()
        ret += "%08x" % numpy.int32(len(payload) / 2).newbyteorder()
        ret += payload
        return ret


class ICTransactionPayload:
    def __init__(self, recipientID, amount):
        self.recipientID = recipientID
        self.amount = numpy.int64(amount)

    def Build(self):
        ret = str()
        ret += self.recipientID
        ret += "%02x" % self.amount
        ret += "%016x" % self.amount
        ret += "00"
        return ret
