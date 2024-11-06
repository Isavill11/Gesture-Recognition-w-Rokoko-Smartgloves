import socket
import json
import pandas as pd
import statistics
import math
import time

# def check_variance(df):
#     temp_df = df.iloc[-10:]
#     var = temp_df.var()
#     var.tolist()
#     maximum_var = max(var)
#     return maximum_var

# def live_data_to_df(length=None, use_while_loop=False):
#
#     noHeader = True
#     column_names = []
#     df = pd.DataFrame
#     i = 0
#     no_movement_count = 0
#     # start_with_movement = True
#     print("moving...")
#
#     while use_while_loop or (length and i < length):
#         body_data = []
#
#         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         sock.bind(("", 14043))
#         d, addr = sock.recvfrom(65000)
#         d = d.decode("utf-8")
#         d = json.loads(d)
#
#         body = d["scene"]["actors"][0]["body"]
#         body_parts = list(body.keys())
#
#         if noHeader:
#             for body_part in body_parts:
#                 if "right" in body_part:
#                     if "Hand" in body_part or "Thumb" in body_part or "Index" in body_part or "Middle" in body_part or "Ring" in body_part or "Little" in body_part:
#                         another_temp = [body_part + "_positionX", body_part + "_positionY", body_part + "_positionZ",
#                                         body_part + "rotation_x", body_part + "rotation_y", body_part + "rotation_z", body_part + "rotation_w"]
#                         column_names.extend(another_temp)
#             df = pd.DataFrame(columns=column_names)
#             noHeader = False
#
#         # print(body["rightIndexMedial"]["rotation"]["x"])
#         for body_part in body_parts:
#             if "right" in body_part:
#                 if "Hand" in body_part or "Thumb" in body_part or "Index" in body_part or "Middle" in body_part or "Ring" in body_part or "Little" in body_part:
#                     b = body[body_part]
#                     temp = [b["position"]["x"], b["position"]["y"], b["position"]["z"], b["rotation"]["x"],b["rotation"]["y"],
#                             b["rotation"]["z"], b["rotation"]["w"]]
#                     body_data.extend(temp)
#
#         df.loc[len(df)] = body_data
#         if i % 8 == 0 and i != 0:
#             session_variance = check_variance(df)
#             # print(session_variance)
#             if session_variance < 0.00001:
#                 no_movement_count += 1
#                 # print(f"No movement detected! Count: {no_movement_count}")
#                 if no_movement_count >= 2:
#                     print("No movement detected. Exiting loop.")
#                     df.drop(df.tail(15).index, inplace=True)
#                     return df # delete this depending on whether youre collecting data or if youre performing live classification.
#             else:
#                 no_movement_count = 0
#
#         i += 1
#
#     return df


def live_data_to_df(t):

    noHeader = True
    column_names = []
    df = pd.DataFrame
    variance_df = pd.DataFrame
    print("moving...")

    for i in range(t):
        #TODO: for each loop, add the "body_data" list to a dataframe object. since the body data is going to
        # reset to have nothing in it each time, i have to add the row after each iteration of this for loop.
        # Then, i need to set the column names after each finger part and then include its roll, pitch and yaw instead of quaternion rotational units.

        body_data = []

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("", 14043))
        d, addr = sock.recvfrom(65000)
        d = d.decode("utf-8")
        d = json.loads(d)

        # timestamp = d["scene"]

        body = d["scene"]["actors"][0]["body"]
        body_parts = list(body.keys())

        if noHeader:
            for body_part in body_parts:
                if "right" in body_part:
                    if "Lower" in body_part or "Hand" in body_part or "Thumb" in body_part or "Index" in body_part or "Middle" in body_part or "Ring" in body_part or "Little" in body_part:
                        another_temp = [body_part + "_positionX", body_part + "_positionY", body_part + "_positionZ",
                                        body_part + "rotation_x", body_part + "rotation_y", body_part + "rotation_z", body_part + "rotation_w"]
                        column_names.extend(another_temp)
            # print(column_names)
            df = pd.DataFrame(columns=column_names)
            variance_df = pd.DataFrame(columns=column_names)
            noHeader = False

        # print(body["leftIndexMedial"]["rotation"]["x"])
        for body_part in body_parts:
            if "right" in body_part:
                if "Lower" in body_part or "Hand" in body_part or "Thumb" in body_part or "Index" in body_part or "Middle" in body_part or "Ring" in body_part or "Little" in body_part:
                    b = body[body_part]
                    # r, p, y = quaternion_to_euler(b["rotation"]["x"], b["rotation"]["y"], b["rotation"]["z"],
                    #                               b["rotation"]["w"])
                    temp = [b["position"]["x"], b["position"]["y"], b["position"]["z"], b["rotation"]["x"],b["rotation"]["y"],
                            b["rotation"]["z"], b["rotation"]["w"]]
                    body_data.extend(temp)

        df.loc[len(df)] = body_data

    return df
