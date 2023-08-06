# File & Folder setup

from AoE2ScenarioParser.aoe2_scenario import AoE2Scenario

# Define paths to scenario
from AoE2ScenarioParser.datasets.players import Player
from AoE2ScenarioParser.helper.retriever import get_retriever_by_name
from AoE2ScenarioParser.objects.triggers_obj import TS, GroupBy

scenario_folder = "C:/Users/Kerwin Sneijders/Games/Age of Empires 2 DE/76561198140740017/resources/_common/scenario/"

# read_file = scenario_folder + "4_Genghis_2.aoe2scenario"
# read_file = scenario_folder + "1_Wallace_2_test.aoe2scenario"


read_file = scenario_folder + "1_Wallace_2.aoe2scenario"
scenario = AoE2Scenario.from_file(read_file)


trigger_manager = scenario.trigger_manager
trigger_manager.copy_trigger_tree(TS.index(0))


trigger_manager.copy_trigger_tree_per_player(
    from_player=Player.ONE,
    trigger_select=TS.index(0),
    group_triggers_by=GroupBy.PLAYER,
)



scenario.write_to_file(scenario_folder + "1_Wallace_2_test2.aoe2scenario")
