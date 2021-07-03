import argparse
import time
import numpy as np
import sys


import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


def main():
    BoardShim.enable_dev_board_logger()

    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                        default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=True)
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file

    board = BoardShim(args.board_id, params)
    board.prepare_session()
    #np.set_printoptions(threshold=sys.maxsize)

    board.start_stream(45000, args.streamer_params)
    for i in range(10):
        print("contract hand - 1")
        board.insert_marker(1)
        time.sleep(1)

        print("release hand - 2")
        board.insert_marker(2)
        time.sleep(1)
    data = board.get_board_data()
    board.stop_stream()
    board.release_session()
    #
    timestamp_index = board.get_timestamp_channel(-1)
    marker_index = board.get_marker_channel(-1)
    emg_channel_index = board.get_emg_channels(-1)
    #print("emg channels" , emg_channel_index)

    count1= 0
    index = 0
    for i in data[marker_index]:
        #print(i)
        if i == 0:
            #print("theres a 1")
            count1 = count1 +1
        elif i == 2:
            print("theres a 2!!!!")
            epoch1 = data[1:16][1:238]
            break
        index += 1
    print(epoch1.shape)
    print(count1)

    #
    # print("data", data)
    # print("length of data", len(data))
    # print("timestamp_index", timestamp_index)
    # print("data[timestamp_index]", len(data[timestamp_index]))
    # print("marker_index", marker_index)
    # print("data[marker_index]", data[marker_index])
    # print("length of data[marker_index]", len(data[marker_index]))
    #
    # print(len(data[0]))
    # print(board.get_sampling_rate(-1))

    # for i in range (0, count1):
    #     print (data)

if __name__ == "__main__":
    main()
