
from ctypes import *
import sys
import array
from ErrorCodes import *
#import msvcrt
from ndef_example import *
#################################################################

DLOGIC_CARD_TYPE = {
    'DL_NO_CARD': 0x00,
    'DL_MIFARE_ULTRALIGHT': 0x01,
    'DL_MIFARE_ULTRALIGHT_EV1_11': 0x02,
    'DL_MIFARE_ULTRALIGHT_EV1_21': 0x03,
    'DL_MIFARE_ULTRALIGHT_C': 0x04,
    'DL_NTAG_203': 0x05,
    'DL_NTAG_210': 0x06,
    'DL_NTAG_212': 0x07,
    'DL_NTAG_213': 0x08,
    'DL_NTAG_215': 0x09,
    'DL_NTAG_216': 0x0A,
    'DL_MIKRON_MIK640D': 0x0B,
    'NFC_T2T_GENERIC': 0x0C,
    'DL_NT3H_1101': 0x0D,
    'DL_NT3H_1201': 0x0E,
    'DL_NT3H_2111': 0x0F,
    'DL_NT3H_2211': 0x10,

    'DL_MIFARE_MINI': 0x20,
    'DL_MIFARE_CLASSIC_1K': 0x21,
    'DL_MIFARE_CLASSIC_4K': 0x22,
    'DL_MIFARE_PLUS_S_2K_SL0': 0x23,
    'DL_MIFARE_PLUS_S_4K_SL0': 0x24,
    'DL_MIFARE_PLUS_X_2K_SL0': 0x25,
    'DL_MIFARE_PLUS_X_4K_SL0': 0x26,
    'DL_MIFARE_DESFIRE': 0x27,
    'DL_MIFARE_DESFIRE_EV1_2K': 0x28,
    'DL_MIFARE_DESFIRE_EV1_4K': 0x29,
    'DL_MIFARE_DESFIRE_EV1_8K': 0x2A,
    'DL_MIFARE_DESFIRE_EV2_2K': 0x2B,
    'DL_MIFARE_DESFIRE_EV2_4K': 0x2C,
    'DL_MIFARE_DESFIRE_EV2_8K': 0x2D,
    'DL_MIFARE_PLUS_S_2K_SL1': 0x2E,
    'DL_MIFARE_PLUS_X_2K_SL1'	: 0x2F,
    'DL_MIFARE_PLUS_EV1_2K_SL1': 0x30,
    'DL_MIFARE_PLUS_X_2K_SL2': 0x31,
    'DL_MIFARE_PLUS_S_2K_SL3'	: 0x32,
    'DL_MIFARE_PLUS_X_2K_SL3'	: 0x33,
    'DL_MIFARE_PLUS_EV1_2K_SL3': 0x34,
    'DL_MIFARE_PLUS_S_4K_SL1': 0x35,
    'DL_MIFARE_PLUS_X_4K_SL1'	: 0x36,
    'DL_MIFARE_PLUS_EV1_4K_SL1': 0x37,
    'DL_MIFARE_PLUS_X_4K_SL2'	: 0x38,
    'DL_MIFARE_PLUS_S_4K_SL3'	: 0x39,
    'DL_MIFARE_PLUS_X_4K_SL3'	: 0x3A,
    'DL_MIFARE_PLUS_EV1_4K_SL3': 0x3B,

    # Special card type
    'DL_GENERIC_ISO14443_4': 0x40,
    'DL_GENERIC_ISO14443_4_TYPE_B': 0x41,
    'DL_GENERIC_ISO14443_3_TYPE_B': 0x42,

    'DL_UNKNOWN_ISO_14443_4': 0x40
}
##################################################################


def getCardType():
    cardtype_val = c_ubyte()
    getCardTypeFunc = uFR.GetDlogicCardType
    getCardTypeFunc.argtypes = [POINTER(c_ubyte)]
    status = uFR.GetDlogicCardType(byref(cardtype_val))
    if status == 0:
        return(cardtype_val.value)
##################################################################


def ndefReadRecords():
    #func = uFR.read_ndef_record
    #func.argtypes = [c_ubyte, ]

    
    message_nr = c_ubyte(1)
    tnf = c_ubyte(1)
    type_record = (c_ubyte * 256)()
    type_record[0] = c_ubyte(85) # 'U'
    type_length = c_ubyte(1)
    id = (c_ubyte * 256)()
    id_length = c_ubyte(0)
    payload = (c_ubyte * 1000)()
    payload_length = c_uint32(0)
    

    message_cnt = c_ubyte(0)
    record_cnt = c_ubyte(0)
    empty_record_cnt = c_ubyte(0)
    record_cnt_array = (c_ubyte * 100)()

    card_type = c_uint32()

    card_type = getCardType()
    for type_key, type_val in DLOGIC_CARD_TYPE.items():
        if type_val == card_type:
            print("-------------------------")
            print('Card type: ' + type_key)

    getNdefCountFunc = uFR.get_ndef_record_count
    getNdefCountFunc.argtypes = [POINTER(c_ubyte), POINTER(c_ubyte), (c_ubyte*100), POINTER(c_ubyte)]
    status = getNdefCountFunc(byref(message_cnt), byref(record_cnt), record_cnt_array, byref(empty_record_cnt))
    if status != 0:
        print("Card is not initialized.")
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        return

    print("Messages : " + str(message_cnt.value))
    print("Records : " + str(record_cnt.value))
    print("Empty records : " + str(empty_record_cnt.value))

    #for x in range(record_cnt.value):
    
    for x in range(1,record_cnt.value + 1):
        record_nr = c_ubyte(x)
        readNdefFunc = uFR.read_ndef_record
        readNdefFunc.argtypes = [c_ubyte, c_ubyte, POINTER(c_ubyte), (c_ubyte*256), POINTER(
            c_ubyte), (c_ubyte*256), POINTER(c_ubyte), (c_ubyte*1000), POINTER(c_uint32)]

        status = readNdefFunc(message_nr, record_nr, byref(tnf), type_record, byref(
          type_length), id, byref(id_length), payload, byref(payload_length))
        
        print_payload = payload[0:payload_length.value]
        print_type = type_record[0:type_length.value]

        if status != 0x00:
            if status == 0x80:
                print("NDEF format error.")
                print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
                return
            elif status == 0x81:
                print("NDEF message not found.")
                print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
                return
            else:
                print("Error occurred.")
                print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
                return
        else:
            print("-------------------------")
            print("No: " + str(record_nr.value))
            type_output = ''.join(chr(e) for e in print_type)
            print("Type: " + type_output)
            print("Length: " + str(payload_length.value))            
            payload_output = ''.join(chr(e) for e in print_payload)
            print("Payload: " + payload_output)
    print("-------------------------")
    print("Reading done.")

def ndefWriteRecords():
    print("Choose NDEF record type you wish to write:")
    print("   (1) - Phone ")
    print("   (2) - SMS ")
    print("   (3) - URI ")

    choice = input()
    choice = int(choice)

    if choice == 1:        
        #Tel TNF=1, Type = URI = "U", Type Length =1 , payload[0]=5

        print("Enter phone number you wish to write:")
        phone_nr = input()        
        payload_length = len(phone_nr) + 1

        tmp_payload = (c_ubyte*payload_length)()
        tmp_payload = phone_nr.encode('utf-8') # string to array conversion
        payload = (c_ubyte*payload_length)()
        payload[0] = 5       
        for x in range(1, payload_length):           
            payload[x] = tmp_payload[x-1]
        #loop for putting rest of our payload after 0 insertion
        message_nr = c_ubyte(1)
        tnf = c_ubyte(1)
        type_record = c_ubyte(85) # 'U'
        type_length = c_ubyte(1)
        id = (c_ubyte*2)()
        id_length = c_ubyte(0)
        payload_length = c_uint32(len(payload))
        card_formatted = c_ubyte()

        writeNdefFunc = uFR.write_ndef_record
        writeNdefFunc.argtypes =[c_ubyte,  POINTER(c_ubyte),POINTER(c_ubyte) , POINTER(c_ubyte),
        (c_ubyte*2), POINTER(c_ubyte), (c_ubyte*payload_length.value), POINTER(c_uint32), POINTER(c_ubyte)]
        status = writeNdefFunc(message_nr, byref(tnf), byref(type_record), byref(
        type_length), id, byref(id_length), payload, byref(payload_length), byref(card_formatted))
        if status == 0:
            print("Phone NDEF written successfully.")
            print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        else:
            print("Phone NDEF write failed.")
            print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])

    elif choice == 2:
        #SMS TNF=1, Type = URI = "U", Type Length =1 , payload[0]=0 , "sms:", "?body:"
        
        sms_header1 = "sms: "
        sms_header2 = "?body="        
        print("Enter SMS number you wish to write:")
        sms_nr = input()
        print("Enter SMS message you wish to write")
        sms_msg = input()
        tmp_str_payload = sms_header1 + sms_nr + sms_header2 + sms_msg
        payload_length = len(tmp_str_payload) + 1

        tmp_payload = (c_ubyte*payload_length)()
        tmp_payload = tmp_str_payload.encode('utf-8')
        payload = (c_ubyte*payload_length)()
        payload[0] = 0
        for x in range(1, payload_length):           
            payload[x] = tmp_payload[x-1]
        #loop for putting rest of our payload after 0 insertion
            message_nr = c_ubyte(1)
        tnf = c_ubyte(1)
        type_record = c_ubyte(85) # 'U'
        type_length = c_ubyte(1)
        id = (c_ubyte*2)()
        id_length = c_ubyte(0)
        payload_length = c_uint32(len(payload))
        card_formatted = c_ubyte()

        writeNdefFunc = uFR.write_ndef_record
        writeNdefFunc.argtypes =[c_ubyte,  POINTER(c_ubyte),POINTER(c_ubyte) , POINTER(c_ubyte),
        (c_ubyte*2), POINTER(c_ubyte), (c_ubyte*payload_length.value), POINTER(c_uint32), POINTER(c_ubyte)]
        status = writeNdefFunc(message_nr, byref(tnf), byref(type_record), byref(
        type_length), id, byref(id_length), payload, byref(payload_length), byref(card_formatted))
        if status == 0:
            print("SMS NDEF written successfully.")
            print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        else:
            print("SMS NDEF write failed.")
            print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    elif choice == 3:       
        #URL TNF=1, Type = URI = "U", Type Length =1 , payload[0]=depends on identifier

        print("Enter URI identifier you wish to write(''):")
        print("1 - http://www. | 2 - https://www. | 3 - http:// etc..")
        uri_id = input()
        print("Enter URI link you wish to write (e.g d-logic.net | google.com | etc")
        uri_link = input()        
        payload_length = len(uri_link) + 1

        tmp_payload = (c_ubyte*payload_length)()
        tmp_payload = uri_link.encode('utf-8') # string to array conversion
        payload = (c_ubyte*payload_length)()
        payload[0] = int(uri_id)       
        for x in range(1, payload_length):           
            payload[x] = tmp_payload[x-1]
        #loop for putting rest of our payload after 0 insertion
        message_nr = c_ubyte(1)
        tnf = c_ubyte(1)
        type_record = c_ubyte(85) # 'U'
        type_length = c_ubyte(1)
        id = (c_ubyte*2)()
        id_length = c_ubyte(0)
        payload_length = c_uint32(len(payload))
        card_formatted = c_ubyte()

        writeNdefFunc = uFR.write_ndef_record
        writeNdefFunc.argtypes =[c_ubyte,  POINTER(c_ubyte),POINTER(c_ubyte) , POINTER(c_ubyte),
        (c_ubyte*2), POINTER(c_ubyte), (c_ubyte*payload_length.value), POINTER(c_uint32), POINTER(c_ubyte)]
        status = writeNdefFunc(message_nr, byref(tnf), byref(type_record), byref(
        type_length), id, byref(id_length), payload, byref(payload_length), byref(card_formatted))
        if status == 0:
            print("URI NDEF written successfully.")
            print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        else:
            print("URI NDEF write failed.")
            print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    else:
        print("Invalid choice. Returning to main...")
        return

def ndefInitCard():

    status = uFR.ndef_card_initialization()
    if status == 0:
        print("Card initialized succesfully.")
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    else:
        print("Card initialization failed.")
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])

def ndefEraseLastRecord():
    status = uFR.erase_last_ndef_record(1)
    if status == 0:
        print("Last NDEF record deleted successfully")
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    else:
        print("Last NDEF record deletion - failed")
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])

def ndefEraseAllRecords():
    status = uFR.erase_all_ndef_records(1)
    if status == 0:
        print("All NDEF records deleted successfully")
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    else:
        print("All NDEF records deletion - failed")
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
