#!/usr/bin/python
# -*- coding: utf-8 -*-

####################################################################
#  Project:        Controller Interface
#  Filename:       ucprotocol.h
#
#  Purpose:        Protocol Elements
#
#  Author:         MAXIV translated into python from N-Hands GmbH & Co KG
#
###################################################################
# ucprotocol.py
#  Protocol elements for communication with N-Hands devices
#
#  Defines types of telegrams and constants for its data fields
#  for use in the communication protocol of N-Hands devices.
#
###################################################################

from struct import Struct, calcsize

# Maximum size of a telegram
# Maximum size of a telegram including header (with length field) and data,
# in bytes.

# Maximum number of items
# Maximum number of 32-bit data items in a telegram.

# UC_MAXDATA   ((UC_MAXSIZE - sizeof(UcTelegram))  sizeof(Int32))

# OpCodes
# These constants are used to identify the protocol elements and fit to the
# opcode field of the @ref UcTelegram "telegram header".

UC_SET = 0         # Set telegram
UC_GET = 1         # Get telegram
UC_ACK = 3         # Ack (acknowledge) telegram
UC_TELL = 4        # Tell (event) telegramm

# Reason codes
#  These constants are used to notify about errors in the processing of
#  UcSetTelegram "Set" and UcGetTelegram "Get" telegrams
#  They are found in the reason field of the UcAckTelegram "Ack Telegram".

UC_REASON_OK = 0          # All ok
UC_REASON_ADDR = 1        # Invalid address
UC_REASON_RANGE = 2       # Value out of range
UC_REASON_IGNORED = 3    # Telegram was ignored
UC_REASON_VERIFY = 4      # Verify of data failed
UC_REASON_TYPE = 5        # Wrong type of data
UC_REASON_UNKNW = 99      # unknown error

# Basic Type
# Type of all data fields of the telegrams.

# Telegram header
# Common header for all telegram types.

UcTelegram = Struct('iiiii')
UcTelegram_size = calcsize('iiii')  # do not take into account size field
# length = 0             # Length of the rest(!) of the telegram
# opcode = 0             # Opcode, UC_SET, UC_GET etc.
# address = 0            # Identifier (name) of the controller object
# index = 0              # Sub-identifier of the object (if applicable)
# correlationNumber = 0  # Identity number for matching the answer

# Set telegram
# This telegram sets a value to an object.
# In case of a correlationNumber > 0 an acknowledgement is expected.

UcSetTelegram = Struct('iiiiii')
UcSetTelegram_size = calcsize('iiiii')  # do not take into account size field
# hdr = UcTelegram()        # Telegram header
# data = []

# Get telegram
# This telegram requests a value from a controller object.

UcGetTelegram = Struct('iiiii')
UcGetTelegram_size = calcsize('iiii')  # do not take into account size field
# hdr = UcTelegram()        # Telegram header

# Ack telegram
# Acknowledges a done or denied set of a value to a controller object or
# represents the answer on a request for a value.

UcAckTelegram = Struct('iiiiiii')
UcAckTelegram_size = calcsize('iiiiii')  # do not take into account size field
# hdr = UcTelegram()           # Telegram header
# reason = 0            # Error code, UC_REASON...
# data = []            # Data. May have more than 1 element if necessary

# Tell telegram
# Spontaneously tells a value change of a controller object.

UcTellTelegram = Struct('iiiiii')
UcTellTelegram_size = calcsize('iiiii')  # do not take into account size field
# hdr = UcTelegram()        # Telegram header
# data = []        # Data. May have more than 1 element if necessary
