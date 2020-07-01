import pytest
import logging
import json
import collections
import os
LOGGER = logging.getLogger(__name__)

# os.remove("platform.txt")

file1 = "/tmp/output/simulation.output"
file2 = "./simulation_baseline_files/13-node-sim.output"
with open(file1, 'r') as f1:
    with open(file2, 'r') as f2:
        dict1 = json.load(f1)
        dict1["data"].keys()
        dict2 = json.load(f2)


class Test:

    def test_dictsAlmostEqual(self):

        assert len(dict1) == len(dict2), "Lengths do not match"
        print("Lengths of the dictionaries are same")

    def test_mRIDs(self):
        list_of_mismatch = []  # {"i":[],"j":[]}

        for i in dict1["data"].keys():
            if i in dict2["data"].keys():
                for j in dict1["data"][i].keys():
                    if j in dict2["data"][i].keys():
                        if j == "measurement_mrid":
                            if dict2["data"][i][j] != dict1["data"][i][j]:  # ,"mRIDS do not match"
                                list_of_mismatch.append(i + "_" + j + "_value")
                        elif j == "value":
                            if dict2["data"][i][j] != dict1["data"][i][j]:  # , "Values do not match"
                                list_of_mismatch.append(i + "_" + j + "_value")
                        elif j == "angle":
                            if (abs(dict2["data"][i][j]) - abs(dict1["data"][i][j])) > 0.1 or 0:
                                print(abs(dict2["data"][i][j]), abs(dict1["data"][i][j]), abs(dict2["data"][i][j]) - abs(dict1["data"][i][j]))
                                list_of_mismatch.append(i + "_" + j + "_value")
                        else:
                            if (abs(dict2["data"][i][j]) - abs(dict1["data"][i][j])) >= 0.0001: # "Values do not match for" + j
                                list_of_mismatch.append(i + "_" + j + "_value")
                    else:
                        list_of_mismatch.append(i + "_" + j)
                        print(j + "does not exist in" + i)

            else:
                print(i + " mRID not present in simulation output")
                list_of_mismatch.append(i)
                print("Failed")
        #print("list of mRIDS not present are" + str(list_of_mismatch))
        assert len(list_of_mismatch) == 0, "Number of mismatches are :" + str(len(list_of_mismatch))


    #     for i, j in dict1.items():
    #         for l, m in j.items():
    #             if 'value' in m.keys():
    #                 for key, value in dict2.items():
    #                     for x, z in value.items():
    #                         assert l == x, "mrids do not match "
    #                         if l == x:
    #                             if 'value' in z.keys():
    #                                 assert z.get("value") == m.get("value"), "Values do not match"
    #                                 print("values match")
    #                                 if 'measurement_mrid' in z.keys():
    #                                     print(m.get("measurement_mrid"), z.get("measurement_mrid"))
    #                                     assert z.get("measurement_mrid") == m.get(
    #                                         "measurement_mrid"), "MRIDS don't match"
    #                                     print("Alka")
    #                                     return False
    #     return True
    #
    # def test_angle(self):
    #     for i, j in dict1.items():
    #         for l, m in j.items():
    #             if 'value' in m.keys():
    #                 for key, value in dict2.items():
    #                     for x, z in value.items():
    #                         if l == x:
    #                             if 'angle' in m.keys():
    #                                 for key1, value1 in dict2.items():
    #                                     for x1, z1 in value1.items():
    #                                         if l == x1:
    #                                             assert (abs(z1.get("angle") - abs(m.get("angle")) <= 0.1)), "No match"
    #
    #                                             assert z1.get("measurement_mrid") == m.get(
    #                                                 "measurement_mrid"), "mRIDS match"
    #
    #                                             assert (abs(z1.get("magnitude")) - abs(
    #                                                 m.get("magnitude") <= 0.001)), "Magnitude do not match"

    # LOGGER.info('Angles match')
    # LOGGER.info('mRIDS match')
    # LOGGER.info('Magnitudes match')
    #
    # LOGGER.info('mRIDs match')

    #
    #
    #     assert m.get("angle") == n.get("angle"), "Angles do not match"
    #     # assert (abs(m.get("angle") - n.get("angle")) <= 0.1), "Angles don't match"
    #     LOGGER.info('Angles do not match')
    #     print("Angle")
    #
    # assert abs(m.get("magnitude") - n.get("magnitude")) <= 0.001, "Magnitudes do not match"
    # LOGGER.info('Magnitudes match')
