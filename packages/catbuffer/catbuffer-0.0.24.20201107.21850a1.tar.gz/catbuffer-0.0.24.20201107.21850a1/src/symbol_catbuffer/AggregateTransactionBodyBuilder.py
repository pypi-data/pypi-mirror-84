#!/usr/bin/python
"""
    Copyright (c) 2016-2019, Jaguar0625, gimre, BloodyRookie, Tech Bureau, Corp.
    Copyright (c) 2020-present, Jaguar0625, gimre, BloodyRookie.

    This file is part of Catapult.

    Catapult is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Catapult is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with Catapult. If not, see <http://www.gnu.org/licenses/>.
"""

# pylint: disable=W0622,W0612,C0301,R0904

from __future__ import annotations
from functools import reduce
from typing import List
import TransactionBuilderFactory
from .CosignatureBuilder import CosignatureBuilder
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .GeneratorUtils import GeneratorUtils
from .Hash256Dto import Hash256Dto


class AggregateTransactionBodyBuilder:
    """Binary layout for an aggregate transaction.
    Attributes:
        transactionsHash: Aggregate hash of an aggregate's transactions.
        aggregateTransactionHeader_Reserved1: Reserved padding to align end of AggregateTransactionHeader on 8-byte boundary.
        transactions: Sub-transaction data (transactions are variable sized and payload size is in bytes).
        cosignatures: Cosignatures data (fills remaining body space after transactions).
    """

    def __init__(self, transactionsHash: Hash256Dto, transactions: List[EmbeddedTransactionBuilder], cosignatures: List[CosignatureBuilder]):
        """Constructor.
        Args:
            transactionsHash: Aggregate hash of an aggregate's transactions.
            transactions: Sub-transaction data (transactions are variable sized and payload size is in bytes).
            cosignatures: Cosignatures data (fills remaining body space after transactions).
        """
        self.transactionsHash = transactionsHash
        self.aggregateTransactionHeader_Reserved1 = 0
        self.transactions = transactions
        self.cosignatures = cosignatures

    @classmethod
    def _serialize(cls, transaction: EmbeddedTransactionBuilder) -> bytes:
        """Serializes an embedded transaction correctly with padding.
        Returns:
            Serialized bytes.
        """
        bytes_ = transaction.serialize()
        padding = bytes(GeneratorUtils.getTransactionPaddingSize(len(bytes_), 8))
        return GeneratorUtils.concatTypedArrays(bytes_, padding)

    @classmethod
    def _getEmbeddedTransactionSize(cls, transactions: List[EmbeddedTransactionBuilder]) -> int:
        """Gets actual size of embedded transactions.
        Returns:
            Size in bytes.
        """
        return reduce(lambda a, b: a + b, map(lambda x: len(cls._serialize(x)), transactions), 0)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AggregateTransactionBodyBuilder:
        """Creates an instance of AggregateTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AggregateTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        transactionsHash = Hash256Dto.loadFromBinary(bytes_)
        bytes_ = bytes_[transactionsHash.getSize():]
        payloadSize = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))
        bytes_ = bytes_[4:]

        aggregateTransactionHeader_Reserved1 = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))
        bytes_ = bytes_[4:]

        transactionsByteSize = payloadSize
        transactions: List[EmbeddedTransactionBuilder] = []
        while transactionsByteSize > 0:
            builder = TransactionBuilderFactory.TransactionBuilderFactory.createEmbeddedTransactionBuilder(bytes_)
            transactions.append(builder)
            builderSize = builder.getSize() + GeneratorUtils.getTransactionPaddingSize(builder.getSize(), 8)
            transactionsByteSize -= builderSize
            bytes_ = bytes_[builderSize:]

        cosignaturesByteSize = len(bytes_)
        cosignatures: List[CosignatureBuilder] = []
        while cosignaturesByteSize > 0:
            builder = CosignatureBuilder.loadFromBinary(bytes_)
            cosignatures.append(builder)
            builderSize = builder.getSize()
            cosignaturesByteSize -= builderSize
            bytes_ = bytes_[builderSize:]
        return AggregateTransactionBodyBuilder(transactionsHash, transactions, cosignatures)

    def getTransactionsHash(self) -> Hash256Dto:
        """Gets aggregate hash of an aggregate's transactions.
        Returns:
            Aggregate hash of an aggregate's transactions.
        """
        return self.transactionsHash

    def getAggregateTransactionHeader_Reserved1(self) -> int:
        """Gets reserved padding to align end of AggregateTransactionHeader on 8-byte boundary.
        Returns:
            Reserved padding to align end of AggregateTransactionHeader on 8-byte boundary.
        """
        return self.aggregateTransactionHeader_Reserved1

    def getTransactions(self) -> List[EmbeddedTransactionBuilder]:
        """Gets sub-transaction data (transactions are variable sized and payload size is in bytes).
        Returns:
            Sub-transaction data (transactions are variable sized and payload size is in bytes).
        """
        return self.transactions

    def getCosignatures(self) -> List[CosignatureBuilder]:
        """Gets cosignatures data (fills remaining body space after transactions).
        Returns:
            Cosignatures data (fills remaining body space after transactions).
        """
        return self.cosignatures

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.transactionsHash.getSize()
        size += 4  # payloadSize
        size += 4  # aggregateTransactionHeader_Reserved1
        for _ in self.transactions:
            size += len(self._serialize(_))
        for _ in self.cosignatures:
            size += _.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        transactionsHashBytes = self.transactionsHash.serialize()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, transactionsHashBytes)
        payloadSizeBytes = GeneratorUtils.uintToBuffer(self._getEmbeddedTransactionSize(self.transactions), 4)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, payloadSizeBytes)
        aggregateTransactionHeader_Reserved1Bytes = GeneratorUtils.uintToBuffer(self.getAggregateTransactionHeader_Reserved1(), 4)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, aggregateTransactionHeader_Reserved1Bytes)
        for embeddedTransactionBuilder in self.transactions:
            transactionsBytes = self._serialize(embeddedTransactionBuilder)
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, transactionsBytes)
        for cosignatureBuilder in self.cosignatures:
            cosignaturesBytes = cosignatureBuilder.serialize()
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, cosignaturesBytes)
        return bytes_
