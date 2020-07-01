from contextlib import contextmanager
import json
import logging
import yaml
import os
from dictdiffer import diff
from time import sleep, time
import sys
import pandas as pd
import pytest
from numbers import Number
from math import isclose

from gridappsd import GridAPPSD
# tm: added for run_simulation workaround
from gridappsd.simulation import Simulation
from gridappsd_docker import docker_up, docker_down
from gridappsd import topics as t

LOGGER = logging.getLogger(__name__)


@contextmanager
def startup_containers(spec=None):
    LOGGER.info('Starting gridappsd containers')
    docker_up(spec)
    LOGGER.info('Containers started')

    yield

    LOGGER.info('Stopping gridappsd containers')
    docker_down()
    LOGGER.info('Containers stopped')


@contextmanager
def gappsd() -> GridAPPSD:
    gridappsd = GridAPPSD()
    LOGGER.info('Gridappsd connected')

    yield gridappsd

    gridappsd.disconnect()
    LOGGER.info('Gridappsd disconnected')

json_msg = []


def on_message(self, message):
    # message = {}
    global json_msg
    try:
        print(f"ON PLATFORM MESSAGE: {message}")

        # message_str = 'received message ' + str(message)
        #
        # json_msg = yaml.safe_load(str(message))
        # print(json_msg)
        #
        # with open("./platform.txt", 'a') as fp:
        #     fp.write(json.dumps(json_msg))
        #
        # if "pause" in json_msg["logMessage"]:
        #     with open("./pause.txt", 'w') as f:
        #         f.write(json.dumps(json_msg))

    except Exception as e:
        message_str = "An error occurred while trying to translate the  message received" + str(e)


@pytest.mark.parametrize("sim_config_file, sim_result_file", [
    # ("9500-config.json", "9500-simulation.output")
    #("123-config.json", "123-simulation.output"),
    ("13-new.json", "13-node-sim.output"),
   ])
def test_simulation_output(sim_config_file, sim_result_file):
    sim_config_file = os.path.join(os.path.dirname(__file__), f"simulation_config_files/{sim_config_file}")
    sim_result_file = os.path.join(os.path.dirname(__file__), f"simulation_baseline_files/{sim_result_file}")
    assert os.path.exists(sim_config_file), f"File {sim_config_file} must exist to run simulation test"
    # assert os.path.exists(sim_result_file), f"File {sim_result_file} must exist to run simulation test"

    with startup_containers():
        # Allow proven to come up
        sleep(30)
        starttime = int(time())
        with gappsd() as gapps:
            os.makedirs("/tmp/output", exist_ok=True)
            with open("/tmp/output/simulation.output", 'w') as outfile:
                LOGGER.info('Configuring simulation')
                sim_complete = False
                rcvd_measurement = False
                rcvd_first_measurement = 0

                def onmeasurement(sim, timestep, measurements):
                    LOGGER.info('Measurement received at %s', timestep)
                    nonlocal rcvd_measurement
                    nonlocal rcvd_first_measurement

                    if rcvd_first_measurement == 0:
                        rcvd_first_measurement = timestep

                    elif rcvd_first_measurement + 15 == timestep:
                    #if timestep == 10 and rcvd_measurement == True:
                        print("Alkaaaa")
                        LOGGER.info('Pausing simulation')
                        sim.pause()
                        LOGGER.info('Paused simulation')

                    #elif rcvd_first_measurement + 114 == timestep:
                    elif rcvd_measurement and rcvd_first_measurement + 14 == timestep:
                        LOGGER.info('Resuming simulation')
                        sim.resume()
                        LOGGER.info('Resumed simulation')

                    if not rcvd_measurement:
                        print(f"A measurement happened at {timestep}")
                        # outfile.write(f"{timestep}|{json.dumps(measurements)}\n")
                        data = {"data": measurements}
                        outfile.write(json.dumps(data))
                        rcvd_measurement = True

                def ontimestep(sim, timestep):
                    print("Timestamp: {}".format(timestep))

                def onfinishsimulation(sim):
                    nonlocal sim_complete
                    sim_complete = True
                    LOGGER.info('Simulation Complete')

                LOGGER.info(f"Start time is {starttime}")
                LOGGER.info('Loading config')
                with open(sim_config_file) as fp:
                    LOGGER.info('Reading config')
                    run_config = json.load(fp)
                    run_config["simulation_config"]["start_time"] = str(starttime)

                sim = Simulation(gapps, run_config)

                # tm: typo in add_onmesurement
                LOGGER.info('sim.add_onmesurement_callback')
                sim.add_onmesurement_callback(onmeasurement)
                sim.add_ontimestep_callback(ontimestep)

                # sim.add_ontimestep_callback()
                LOGGER.info('sim.add_oncomplete_callback')
                sim.add_oncomplete_callback(onfinishsimulation)
                LOGGER.info('Starting sim')
                sim.start_simulation()
                print(sim.simulation_id)
                #gapps.subscribe(t.platform_log_topic(), on_message)
                gapps.subscribe(t.simulation_log_topic(sim.simulation_id),on_message)
                while not sim_complete:
                    LOGGER.info('Sleeping')
                    sleep(5)


# file1 = "/tmp/output/simulation.output"
# file2 = "./simulation_baseline_files/13-node-sim.output"
# with open(file1, 'r') as f1:
#     with open(file2, 'r') as f2:
#         dict1 = json.load(f1)
#
#         dict2 = json.load(f2)
#
#
# def test_dictsAlmostEqual():
#     assert len(dict1) == len(dict2), "Lengths do not match"
#     print("Lengths of the dictionaries are same")
#
#
# def test_mRIDs():
#     list_of_mismatch = []  # {"i":[],"j":[]}
#
#     for i in dict1["data"].keys():
#         if i in dict2["data"].keys():
#             for j in dict1["data"][i].keys():
#                 if j in dict2["data"][i].keys():
#                     if j == "measurement_mrid":
#                         if dict2["data"][i][j] != dict1["data"][i][j]:  # ,"mRIDS do not match"
#                             list_of_mismatch.append(i + "_" + j + "_value")
#                     elif j == "value":
#                         if dict2["data"][i][j] != dict1["data"][i][j]:  # , "Values do not match"
#                             list_of_mismatch.append(i + "_" + j + "_value")
#                     elif j == "angle":
#                         if (abs(dict2["data"][i][j]) - abs(dict1["data"][i][j])) > 0.1 or 0:
#                             print(abs(dict2["data"][i][j]), abs(dict1["data"][i][j]),
#                                   abs(dict2["data"][i][j]) - abs(dict1["data"][i][j]))
#                             list_of_mismatch.append(i + "_" + j + "_value")
#                     else:
#                         if (abs(dict2["data"][i][j]) - abs(
#                                 dict1["data"][i][j])) >= 0.0001:  # "Values do not match for" + j
#                             list_of_mismatch.append(i + "_" + j + "_value")
#                 else:
#                     list_of_mismatch.append(i + "_" + j)
#                     print(j + "does not exist in" + i)
#
#         else:
#             print(i + " mRID not present in simulation output")
#             list_of_mismatch.append(i)
#             print("Failed")
#     # print("list of mRIDS not present are" + str(list_of_mismatch))
#     assert len(list_of_mismatch) == 0, "Number of mismatches are :" + str(len(list_of_mismatch))
#
# # def test_pause():
# #     global json_msg
# #     assert "pause" in json_msg['logMessage'], 'Pause command not called'
