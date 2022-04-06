import base64
from flask import Flask, jsonify, request
import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.controllers.container_manager import ContainerManager
from csle_common.util.read_emulation_statistics import ReadEmulationStatistics
from csle_common.controllers.emulation_env_manager import EmulationEnvManager
from csle_common.controllers.monitor_tools_controller import MonitorToolsController
from waitress import serve

app = Flask(__name__, static_url_path='', static_folder='../build/')


@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')


@app.route('/nodeexporter', methods=['GET', 'POST'])
def node_exporter():
    running = MonitorToolsController.is_node_exporter_running()
    port = constants.COMMANDS.NODE_EXPORTER_PORT
    node_exporter_dict = {
        "running": running,
        "port": port,
        "url": f"http://localhost:{port}/"
    }
    response = jsonify(node_exporter_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/prometheus', methods=['GET', 'POST'])
def prometheus():
    running = MonitorToolsController.is_prometheus_running()
    port = constants.COMMANDS.PROMETHEUS_PORT
    if request.method == "POST":
        if running:
            MonitorToolsController.stop_prometheus()
            running = False
        else:
            MonitorToolsController.start_prometheus()
            running = True
    prometheus_dict = {
        "running": running,
        "port": port,
        "url": f"http://localhost:{port}/"
    }
    response = jsonify(prometheus_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/cadvisor', methods=['GET', 'POST'])
def cadvisor():
    running = MonitorToolsController.is_cadvisor_running()
    port = constants.COMMANDS.CADVISOR_PORT
    if request.method == "POST":
        if running:
            MonitorToolsController.stop_cadvisor()
            running = False
        else:
            MonitorToolsController.start_cadvisor()
            running = True
    cadvisor_dict = {
        "running": running,
        "port": port,
        "url": f"http://localhost:{port}/"
    }
    response = jsonify(cadvisor_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/grafana', methods=['GET', 'POST'])
def grafana():
    running = MonitorToolsController.is_grafana_running()
    port = constants.COMMANDS.GRAFANA_PORT
    if request.method == "POST":
        if running:
            MonitorToolsController.stop_grafana()
            running = False
        else:
            MonitorToolsController.start_grafana()
            running = True
    grafana_dict = {
        "running": running,
        "port": port,
        "url": f"http://localhost:{port}/"
    }
    response = jsonify(grafana_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/images', methods=['GET'])
def images():
    images=ContainerManager.list_all_images()
    images_dicts = []
    for img in images:
        images_dicts.append(
            {
                "name": img[0],
                "size": img[4]
            }
        )
    response = jsonify(images_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/emulations', methods=['GET'])
def emulations():
    all_emulations = MetastoreFacade.list_emulations()
    all_images = MetastoreFacade.list_emulation_images()
    rc_emulations = ContainerManager.list_running_emulations()
    for em in all_emulations:
        if em.name in rc_emulations:
            em.running = True
        else:
            em.running = False
        for em_name_img in all_images:
            em_name, img = em_name_img
            if em_name == em.name:
                em.image = base64.b64encode(img).decode()
    emulations_dicts = list(map(lambda x: x.to_dict(), all_emulations))
    response = jsonify(emulations_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/monitor/<emulation>/<minutes>', methods=['GET'])
def monitor_emulation(emulation: str, minutes: int):
    minutes = int(minutes)
    em = MetastoreFacade.get_emulation(name=emulation)
    if em is None:
        time_series = None
    else:
        time_series = ReadEmulationStatistics.read_all(emulation_env_config=em, time_window_minutes=minutes).to_dict()
    response = jsonify(time_series)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/emulations/<emulation>', methods=['GET', 'POST'])
def emulation(emulation_name: str):
    em = MetastoreFacade.get_emulation(name=emulation_name)
    rc_emulations = ContainerManager.list_running_emulations()
    if em is not None:
        if em.name in rc_emulations:
            em.running = True
        if request.method == "POST":
            if em.running:
                EmulationEnvManager.stop_containers(emulation_env_config=em)
                EmulationEnvManager.rm_containers(emulation_env_config=em)
                try:
                    ContainerManager.stop_docker_stats_thread(log_sink_config=em.log_sink_config,
                                                              containers_config=em.containers_config,
                                                              emulation_name=em.name)
                except Exception as e:
                    pass
                EmulationEnvManager.delete_networks_of_emulation_env_config(emulation_env_config=em)
                em.running = False
            else:
                EmulationEnvManager.run_containers(emulation_env_config=em)
                EmulationEnvManager.apply_emulation_env_config(emulation_env_config=em)
                em.running = True
    if em is None:
        em_dict = {}
    else:
        em_name, img = MetastoreFacade.get_emulation_img(emulation_name=em.name)
        em.image = base64.b64encode(img).decode()
        em_dict = em.to_dict()
    response = jsonify(em_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/emulationtraces', methods=['GET'])
def emulation_traces():
    emulation_trcs = MetastoreFacade.list_emulation_traces()
    traces_dicts = list(map(lambda x: x.to_dict(), emulation_trcs))
    response = jsonify(traces_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/simulationtraces', methods=['GET'])
def simulation_traces():
    simulation_trcs = MetastoreFacade.list_emulation_traces()
    traces_dicts = list(map(lambda x: x.to_dict(), simulation_trcs))
    response = jsonify(traces_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/dynamicsmodels', methods=['GET'])
def dynamics_models():
    models = MetastoreFacade.list_emulation_statistics()
    models_dicts = list(map(lambda x: x.to_dict(), models))
    response = jsonify(models_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=7777, threads=100)
    #app.run(port=7777,host='0.0.0.0')
