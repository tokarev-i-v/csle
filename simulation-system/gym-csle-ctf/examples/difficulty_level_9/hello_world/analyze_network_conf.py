from csle_common.dao.network.network_config import NetworkConfig

def merge_network_confs():
    conf1 = NetworkConfig.load(dir_path="/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world",
                               file_name="network_conf.pickle")
    conf2 = NetworkConfig.load(
        dir_path="/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world",
        file_name="network_conf2.pickle")
    conf1.merge(conf2)
    conf1.save(dir_path="/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world",
               file_name="network_conf10.pickle")


def test():
    conf1 = NetworkConfig.load(
        dir_path="/home/kim/csle/simulation-system/use_cases/intrusion_prevention/minigames/ctf/gym-csle-ctf/examples/difficulty_level_9/system_id",
        file_name="network_conf.pickle")
    for node in conf1.nodes:
        print("services:{}".format(node.services))
        for service in node.services:
            print(service)

    for node in conf1.nodes:
        for service in node.services:
            print("NODE SERVICES:{}".format(service))

if __name__ == '__main__':
    test()
    # merge_network_confs()