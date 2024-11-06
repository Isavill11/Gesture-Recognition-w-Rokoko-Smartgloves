import socket
import json
import keyboard
# import csv
import time
import math
import statistics


# I NEED TO GET THE THUMB DATA TOO THIS WILL BE IMPORTANT.

def getSocketData(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    data, addr = sock.recvfrom(65000)
    data = data.decode("utf-8")
    data = json.loads(data)
    return data


def getBodyData():
    body_data = []
    data = getSocketData(ip="127.0.0.1", port=14043)
    body = data["scene"]["actors"][0]["body"].keys()
    for body_part in body:
        b = body[body_part]
        temp = [b["position"]["x"], b["position"]["y"], b["position"]["z"], b["rotation"]["x"], b["rotation"]["y"],
                b["rotation"]["z"], b["rotation"]["w"]]
        body_data.extend(temp)
    return body_data


def quaternion_to_euler(x, y, z, w):
    # this code will return the euler angles (roll, pitch, yaw) in degrees.
    # roll is rotation around x axis in radians(ccw)
    # pitch is rotation around y axis in radians (ccw)
    # yaw is rotation around z axis in radians.(ccw)

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = round(math.atan2(t0, t1) * (180 / math.pi), 3)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = round(math.asin(t2) * (180 / math.pi), 3)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = round(math.atan2(t3, t4) * (180 / math.pi), 3)

    return roll_x, pitch_y, yaw_z  # in radians. to make it degrees it would be = round(180/math.pi, 3)


def any_finger_data(fingername, fingerpart):
    p_roll, p_pitch, p_yaw = quaternion_to_euler(
        data["scene"]["actors"][0]["body"]["right" + fingername + fingerpart[0]]["rotation"]["x"],
        data["scene"]["actors"][0]["body"]["right" + fingername + fingerpart[0]]["rotation"]["y"],
        data["scene"]["actors"][0]["body"]["right" + fingername + fingerpart[0]]["rotation"]["z"],
        data["scene"]["actors"][0]["body"]["right" + fingername + fingerpart[0]]["rotation"]["w"])
    m_roll, m_pitch, m_yaw = quaternion_to_euler(
        data["scene"]["actors"][0]["body"]["right" + fingername + fingerpart[1]]["rotation"]["x"],
        data["scene"]["actors"][0]["body"]["right" + fingername + fingerpart[1]]["rotation"]["y"],
        data["scene"]["actors"][0]["body"]["right" + fingername + fingerpart[1]]["rotation"]["z"],
        data["scene"]["actors"][0]["body"]["right" + fingername + fingerpart[1]]["rotation"]["w"])
    d_roll, d_pitch, d_yaw = quaternion_to_euler(
        data["scene"]["actors"][0]["body"]["right" + fingername + fingerpart[2]]["rotation"]["x"],
        data["scene"]["actors"][0]["body"]["right" + fingername + fingerpart[2]]["rotation"]["y"],
        data["scene"]["actors"][0]["body"]["right" + fingername + fingerpart[2]]["rotation"]["z"],
        data["scene"]["actors"][0]["body"]["right" + fingername + fingerpart[2]]["rotation"]["w"])
    t_roll, t_pitch, t_yaw = quaternion_to_euler(
        data["scene"]["actors"][0]["body"]["right" + fingername + fingerpart[3]]["rotation"]["x"],
        data["scene"]["actors"][0]["body"]["right" + fingername + fingerpart[3]]["rotation"]["y"],
        data["scene"]["actors"][0]["body"]["right" + fingername + fingerpart[3]]["rotation"]["z"],
        data["scene"]["actors"][0]["body"]["right" + fingername + fingerpart[3]]["rotation"]["w"])

    return p_roll, p_pitch, p_yaw, m_roll, m_pitch, m_yaw, d_roll, d_pitch, d_yaw, t_roll, t_pitch, t_yaw


data = getSocketData(ip="127.0.0.1", port=14043)


def get_hand_data():
    h_roll, h_pitch, h_yaw = quaternion_to_euler(
        data["scene"]["actors"][0]["body"]["rightHand"]["rotation"]["x"],
        data["scene"]["actors"][0]["body"]["rightHand"]["rotation"]["y"],
        data["scene"]["actors"][0]["body"]["rightHand"]["rotation"]["z"],
        data["scene"]["actors"][0]["body"]["rightHand"]["rotation"]["w"])

    return h_roll, h_pitch, h_yaw


print("press j once you're ready and in your starting position")
print("once running, press another button to stop running the program.")
key = input(keyboard.get_hotkey_name())

if key == "j":
    start = True
    print("\n")
else:
    start = False
    quit()

while True:

    data = getSocketData(ip="127.0.0.1", port=14043)

    fingerparts = ["Proximal", "Medial", "Distal", "Tip"]
    fingernames = ["Thumb", "Index", "Middle", "Ring", "Little"]

    fingerscurled = []
    fingersstraight = []
    fingershalfway = []

    i = 0

    for i in range(5):
        IP_roll, IP_pitch, IP_yaw, IM_roll, IM_pitch, IM_yaw, ID_roll, ID_pitch, ID_yaw, IT_roll, IT_pitch, IT_yaw = any_finger_data(
            fingernames[i], fingerparts)

        print("The parts of the right " + fingernames[i])

        # this will print out all the parts of the "insert finger name" and "insert finger part name"
        # for instance, this will print the middle fingers proximal joint

        hand_roll, hand_pitch, hand_yaw = get_hand_data()
        p_roll = abs(IP_roll - hand_roll)
        m_roll = abs(IM_roll - hand_roll)
        d_roll = abs(ID_roll - hand_roll)
        t_roll = abs(IT_roll - hand_roll)

        # print(fingernames[i] + " " + fingerparts[0])
        # print(IP_roll, IP_pitch, IP_yaw)
        # print(p_roll)
        # print("***************************")
        # #this will print the middle fingers medial joint
        # print(fingernames[i] + " " + fingerparts[1])
        # print(IM_roll, IM_pitch, IM_yaw)
        # print(m_roll)
        # print("***************************")
        #
        # # this will print the distal fingers distal joint
        # print(fingernames[i] + " " + fingerparts[2])
        # print(ID_roll, ID_pitch, ID_yaw)
        # print(d_roll)
        # print("***************************")
        #
        # # this will print out the tip of the finger
        # print(fingernames[i] + " " + fingerparts[3])
        # print(IT_roll, IT_pitch, IT_yaw)
        # print(t_roll)
        # print("***************************")
        if fingernames[i] == "Thumb" and (20 <= m_roll <=40 or 60 <= d_roll <=110 or 60<= t_roll<=120):
            print(f"This is the {fingernames[i]}. ")
            print(p_roll, m_roll, d_roll, t_roll)

            fingerscurled.append(fingernames[i])
        elif 140 < m_roll < 180 and m_roll > d_roll and m_roll > p_roll and m_roll > t_roll:
            print(f"The {fingernames[i]} is curled.{m_roll, IP_pitch, IP_yaw}")
            fingerscurled.append(fingernames[i])
        elif fingernames[i] == "Little" and 50 <= m_roll <=140:
            print(f"The {fingernames[i]} Finger is curledish")
            fingerscurled.append(fingernames[i])
        elif 90 <= m_roll <= 140:
            print(f"The {fingernames[i]} Finger is halfway down. {p_roll}, {IP_pitch}, {IP_yaw}")
            fingershalfway.append(fingernames[i])
        else:
            print(f"the {fingernames[i]} Finger is up. {m_roll}, {IP_pitch}, {IP_yaw}")
            fingersstraight.append(fingernames[i])

        print("***************************************")
        i += 1

    print(f"These are the fingers that are curled: {fingerscurled}")
    print(f"These are the fingers that are straight: {fingersstraight}")

    if ("Thumb" and "Ring" and "Little") in fingerscurled:
        print("Peace sign!")
    elif ("Thumb" and "Middle" and "Ring" and "Little") in fingerscurled:
        print("Pointing")
    elif ("Index" and "Middle" and "Ring" and "Little") in fingerscurled:
        print("A")
    elif "Thumb" in fingerscurled and ("Index" and "Middle" and "Ring" and "Little" in fingersstraight):
        print("B")
    elif ("Thumb" and "Index" and "Middle" and "Ring" and "Little") in fingershalfway:
        print("C")

    time.sleep(1.3)

# if proximal is between 70 and 105 and the rest are greater than proximal, then its curled. Yaw doesnt really matter i dont think.
#


#
#
# import socket
# import json
# import keyboard
# # import csv
# import time
# import math
# import statistics
#
#
# # sum_of_x = []
# # sum_of_y = []
# # sum_of_z = []
#
#
#
# # I NEED TO GET THE THUMB DATA TOO THIS WILL BE IMPORTANT.
#
# def getSocketData(ip, port):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.bind((ip, port))
#     data, addr = sock.recvfrom(65000)
#     data = data.decode("utf-8")
#     data = json.loads(data)
#     return data
#
# def getBodyData():
#     body_data = []
#     data = getSocketData(ip="127.0.0.1", port=14043)
#     body = data["scene"]["actors"][0]["body"].keys()
#     for body_part in body:
#         b = body[body_part]
#         temp = [b["position"]["x"], b["position"]["y"], b["position"]["z"], b["rotation"]["x"], b["rotation"]["y"],
#                 b["rotation"]["z"], b["rotation"]["w"]]
#         body_data.extend(temp)
#     return body_data
#
# def quaternion_to_euler(x, y, z, w):
#     # this code will return the euler angles (roll, pitch, yaw) in degrees.
#     # roll is rotation around x axis in radians(ccw)
#     # pitch is rotation around y axis in radians (ccw)
#     # yaw is rotation around z axis in radians.(ccw)
#
#     t0 = +2.0 * (w * x + y * z)
#     t1 = +1.0 - 2.0 * (x * x + y * y)
#     roll_x = round(math.atan2(t0, t1) * (180 / math.pi), 3)
#
#     t2 = +2.0 * (w * y - z * x)
#     t2 = +1.0 if t2 > +1.0 else t2
#     t2 = -1.0 if t2 < -1.0 else t2
#     pitch_y = round(math.asin(t2) * (180 / math.pi), 3)
#
#     t3 = +2.0 * (w * z + x * y)
#     t4 = +1.0 - 2.0 * (y * y + z * z)
#     yaw_z = round(math.atan2(t3, t4) * (180 / math.pi), 3)
#
#     return abs(roll_x), abs(pitch_y), abs(yaw_z)  # in radians. to make it degrees it would be = round(180/math.pi, 3)
#
# def any_finger_data(fingername, fingerpart):
#     p_roll, p_pitch, p_yaw = quaternion_to_euler(
#         data["scene"]["actors"][0]["body"]["right"+fingername+fingerpart[0]]["rotation"]["x"],
#         data["scene"]["actors"][0]["body"]["right"+fingername+fingerpart[0]]["rotation"]["y"],
#         data["scene"]["actors"][0]["body"]["right"+fingername+fingerpart[0]]["rotation"]["z"],
#         data["scene"]["actors"][0]["body"]["right"+fingername+fingerpart[0]]["rotation"]["w"])
#     m_roll, m_pitch, m_yaw = quaternion_to_euler(
#         data["scene"]["actors"][0]["body"]["right"+fingername+fingerpart[1]]["rotation"]["x"],
#         data["scene"]["actors"][0]["body"]["right"+fingername+fingerpart[1]]["rotation"]["y"],
#         data["scene"]["actors"][0]["body"]["right"+fingername+fingerpart[1]]["rotation"]["z"],
#         data["scene"]["actors"][0]["body"]["right"+fingername+fingerpart[1]]["rotation"]["w"])
#     d_roll, d_pitch, d_yaw = quaternion_to_euler(
#         data["scene"]["actors"][0]["body"]["right"+fingername+fingerpart[2]]["rotation"]["x"],
#         data["scene"]["actors"][0]["body"]["right"+fingername+fingerpart[2]]["rotation"]["y"],
#         data["scene"]["actors"][0]["body"]["right"+fingername+fingerpart[2]]["rotation"]["z"],
#         data["scene"]["actors"][0]["body"]["right"+fingername+fingerpart[2]]["rotation"]["w"])
#     t_roll, t_pitch, t_yaw = quaternion_to_euler(
#         data["scene"]["actors"][0]["body"]["right"+fingername+fingerpart[3]]["rotation"]["x"],
#         data["scene"]["actors"][0]["body"]["right"+fingername+fingerpart[3]]["rotation"]["y"],
#         data["scene"]["actors"][0]["body"]["right"+fingername+fingerpart[3]]["rotation"]["z"],
#         data["scene"]["actors"][0]["body"]["right"+fingername+fingerpart[3]]["rotation"]["w"])
#
#     return p_roll, p_pitch, p_yaw, m_roll, m_pitch, m_yaw, d_roll, d_pitch, d_yaw, t_roll, t_pitch, t_yaw
#
# data = getSocketData(ip="127.0.0.1", port=14043)
#
# def get_hand_data():
#     h_roll, h_pitch, h_yaw = quaternion_to_euler(
#         data["scene"]["actors"][0]["body"]["rightHand"]["rotation"]["x"],
#         data["scene"]["actors"][0]["body"]["rightHand"]["rotation"]["y"],
#         data["scene"]["actors"][0]["body"]["rightHand"]["rotation"]["z"],
#         data["scene"]["actors"][0]["body"]["rightHand"]["rotation"]["w"])
#     return h_roll, h_pitch, h_yaw
#
#
# print("press j once you're ready and in your starting position")
# print("once running, press another button to stop running the program.")
# key = input(keyboard.get_hotkey_name())
#
# if key == "j":
#     start = True
#     print("\n")
# else:
#     start = False
#     quit()
#
#
#
# while True:
#
#     data = getSocketData(ip="127.0.0.1", port=14043)
#     fingerparts = ["Proximal", "Medial", "Distal", "Tip"]
#     fingernames = ["Index", "Middle", "Ring", "Little"]
#     i = 0
#
#     # print("hand")
#     # print(hand_roll, hand_pitch, hand_yaw)
#     #
#     # print("proximal finger part")
#     # IP_roll, IP_pitch, IP_yaw, IM_roll, IM_pitch, IM_yaw, ID_roll, ID_pitch, ID_yaw, IT_roll, IT_pitch, IT_yaw = any_finger_data(
#     #     fingernames[i], fingerparts)
#     # print (IP_roll, IP_pitch, IP_yaw)
#     #
#     # print("when I subtract the hand axes from the finger parts:")
#     #
#
#     for i in range (4):
#         IP_roll, IP_pitch, IP_yaw, IM_roll, IM_pitch, IM_yaw, ID_roll, ID_pitch, ID_yaw, IT_roll, IT_pitch, IT_yaw = any_finger_data(
#             fingernames[i], fingerparts)
#
#         print("The parts of the right" + fingernames[i])
#
# # this will print out all the parts of the "insert finger name" and "insert finger part name"
#         # for instance, this will print the middle fingers proximal joint
#         hand_roll, hand_pitch, hand_yaw = get_hand_data()
#         p_roll = abs(IP_roll - hand_roll)
#         m_roll = abs(IM_roll - hand_roll)
#         d_roll = abs(ID_roll - hand_roll)
#         t_roll = abs(IT_roll - hand_roll)
#
#
#         print(fingernames[i] + " " + fingerparts[0])
#         print(IP_roll, IP_pitch, IP_yaw)
#         print(p_roll)
#
#         #this will print the middle fingers medial joint
#         print(fingernames[i] + " " + fingerparts[1])
#         print(IM_roll, IM_pitch, IM_yaw)
#         print(m_roll)
#         # this will print the distal fingers distal joint
#         print(fingernames[i] + " " + fingerparts[2])
#         print(ID_roll, ID_pitch, ID_yaw)
#         print(d_roll)
#         # this will print out the tip of the finger
#         print(fingernames[i] + " " + fingerparts[3])
#         print(IT_roll, IT_pitch, IT_yaw)
#         print(t_roll)
#
#
#         # if  IP_roll > 100:
#         #     print(f"the {fingernames[i]} Finger is down. {IP_roll}, {IP_pitch}, {IP_yaw}")
#         if m_roll > p_roll and d_roll > p_roll and t_roll > p_roll and 40 <= p_roll <= 100:
#             print(f"The {fingernames[i]} is curled.{p_roll, IP_pitch, IP_yaw}")
#         # elif 45 <= p_roll <= 110:
#         #     print(f"the {fingernames[i]} Finger is halfway down. {p_roll}, {IP_pitch}, {IP_yaw}")
#         else:
#             print(f"the {fingernames[i]} Finger is up. {p_roll}, {IP_pitch}, {IP_yaw}")
#             print ("***************************************")
#         i += 1
#     time.sleep(1.3)
#
#
# # if proximal is between 70 and 105 and the rest are greater than proximal, then its curled. Yaw doesnt really matter i dont think.
# #
#
#
