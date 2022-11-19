import React, {useEffect, useState, useCallback} from 'react';
import './SDNController.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import fileDownload from 'react-file-download'
import Spinner from 'react-bootstrap/Spinner'
import Accordion from 'react-bootstrap/Accordion';
import Collapse from 'react-bootstrap/Collapse'
import serverIp from "../../../Common/serverIp";
import serverPort from "../../Common/serverPort";

/**
 * Component representing the /sdn-controllers/id resource
 */
const SDNController = (props) => {
    const [loading, setLoading] = useState(false);
    const [generalInfoOpen, setGeneralInfoOpen] = useState(false);
    const [switches, setSwitches] = useState([]);
    const [ovsSwitchesOpen, setOvsSwitchesOpen] = useState(false);
    const [activeSwitchesOpen, setActiveSwitchesOpen] = useState(false);
    const [flowsOpen, setFlowsOpen] = useState(false);
    const [groupsOpen, setGroupsOpen] = useState(false);
    const [metersOpen, setMetersOpen] = useState(false);
    const [queuesOpen, setQueuesOpen] = useState(false);
    const [rolesOpen, setRolesOpen] = useState(false);
    const [tablesOpen, setTablesOpen] = useState(false);
    const [portsOpen, setPortsOpen] = useState(false);
    const ip = serverIp
    // const ip = "172.31.212.92"


    const fetchSwitches = useCallback((emulation_id, exec_id) => {
        fetch(
            `http://` + ip + ':7777/emulations/' + emulation_id + "/executions/" + exec_id + "/switches",
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSwitches(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        fetchSwitches(props.emulation.id, props.emulation.execution_id)
    }, [fetchSwitches]);

    const getSpinnerOrCircle = (emulation) => {
        if (loading) {
            return (<Spinner
                as="span"
                animation="grow"
                size="sm"
                role="status"
                aria-hidden="true"
            />)
        }
        if (emulation.running) {
            return (
                <svg id="svg-1" height="15px" width="15px" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg"
                     version="1.1">
                    <circle r="15" cx="15" cy="15" fill="green"></circle>
                </svg>
            )
        } else {
            return (
                <svg id="svg-1" height="15px" width="15px" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg"
                     version="1.1">
                    <circle r="15" cx="15" cy="15" fill="red"></circle>
                </svg>
            )
        }
    }

    const getStatus = (emulation) => {
        if (emulation.running) {
            return "running"
        } else {
            return "stopped"
        }
    }

    const getIps = (ips_and_networks) => {
        const ips = []
        for (let i = 0; i < ips_and_networks.length; i++) {
            ips.push(ips_and_networks[i][0])
        }
        return ips
    }

    const getId = () => {
        return <span>{props.emulation.id}</span>
    }

    const SdnControllerConfig = (props) => {
        if (props.emulation.sdn_controller_config === null || props.emulation.sdn_controller_config === undefined) {
            return (<span> </span>)
        } else {
            return (
                <Card>
                    <Card.Header>
                        <Button
                            onClick={() => setGeneralInfoOpen(!generalInfoOpen)}
                            aria-controls="generalInfoBody"
                            aria-expanded={generalInfoOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle">General information</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={generalInfoOpen}>
                        <div id="generalInfoBody" className="cardBodyHidden">
                            <Table striped bordered hover>
                                <thead>
                                <tr>
                                    <th>Container name</th>
                                    <th>Container os</th>
                                    <th>IPs</th>
                                    <th>Controller module</th>
                                    <th>Port</th>
                                    <th>Web port</th>
                                    <th>Time step length (s)</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr>
                                    <td>{props.emulation.sdn_controller_config.container.full_name_str}</td>
                                    <td>{props.emulation.sdn_controller_config.container.os}</td>
                                    <td>{getIps(props.emulation.sdn_controller_config.container.ips_and_networks).join(", ")}</td>
                                    <td>{props.emulation.sdn_controller_config.controller_module_name}</td>
                                    <td>{props.emulation.sdn_controller_config.controller_port}</td>
                                    <td>{props.emulation.sdn_controller_config.controller_web_api_port}</td>
                                    <td>{props.emulation.sdn_controller_config.time_step_len_seconds}</td>
                                </tr>
                                </tbody>
                            </Table>
                        </div>
                    </Collapse>
                </Card>
            )
        }
    }

    return (
        <Card key={props.emulation.name} ref={props.wrapper}>
            <Card.Header>
                <Accordion.Toggle as={Button} variant="link" eventKey={props.emulation.name} className="mgHeader">
                    <span className="subnetTitle">ID: {getId()}, emulation name: {props.emulation.name}</span>
                    Controller
                    IPs: {getIps(props.emulation.sdn_controller_config.container.ips_and_networks).join(", ")},
                    Status: {getStatus(props.emulation)}
                    {getSpinnerOrCircle(props.emulation)}
                </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey={props.emulation.name}>
                <Card.Body>
                    <SdnControllerConfig emulation={props.emulation}/>
                    <Card>
                        <Card.Header>
                            <Button
                                onClick={() => setOvsSwitchesOpen(!ovsSwitchesOpen)}
                                aria-controls="ovsSwitchesBody"
                                aria-expanded={ovsSwitchesOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">Open vSwitch switches configurations </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={ovsSwitchesOpen}>
                            <div id="ovsSwitchesBody" className="cardBodyHidden">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Container name</th>
                                        <th>Controller ip</th>
                                        <th>Controller port</th>
                                        <th>Controller transport protocol</th>
                                        <th>IP</th>
                                        <th>OpenFlow protocols</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {props.emulation.ovs_config.switch_configs.map((switch_config, index) =>
                                        <tr key={switch_config.container_name + "-" + index}>
                                            <td>{switch_config.container_name}</td>
                                            <td>{switch_config.controler_ip}</td>
                                            <td>{switch_config.controller_port}</td>
                                            <td>{switch_config.controller_transport_protocol}</td>
                                            <td>{switch_config.ip}</td>
                                            <td>{switch_config.openflow_protocols.join(", ")}</td>
                                        </tr>
                                    )}
                                    </tbody>
                                </Table>
                            </div>
                        </Collapse>
                    </Card>

                    <Card>
                        <Card.Header>
                            <Button
                                onClick={() => setActiveSwitchesOpen(!activeSwitchesOpen)}
                                aria-controls="activeSwitchesBody"
                                aria-expanded={activeSwitchesOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">Active Open flow switches </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={activeSwitchesOpen}>
                            <div id="activeSwitchesBody" className="cardBodyHidden">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Datapath ID</th>
                                        <th>Manufacturer</th>
                                        <th>Hardware type</th>
                                        <th>Software version</th>
                                        <th>Serial number</th>
                                        <th>Datapath description</th>
                                        <th>Byte count</th>
                                        <th>Flow count</th>
                                        <th>Packet count</th>
                                        <th>Switch data</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {switches.map((switchDesc, index) =>
                                        <tr key={switchDesc + "-" + index}>
                                            <td>{switchDesc.dpid}</td>
                                            <td>{switchDesc.desc.mfr_desc}</td>
                                            <td>{switchDesc.desc.hw_desc}</td>
                                            <td>{switchDesc.desc.sw_desc}</td>
                                            <td>{switchDesc.desc.serial_num}</td>
                                            <td>{switchDesc.desc.dp_desc}</td>
                                            <td>{switchDesc.aggflows.byte_count}</td>
                                            <td>{switchDesc.aggflows.flow_count}</td>
                                            <td>{switchDesc.aggflows.packet_count}</td>
                                            <td>
                                                <Button variant="link"
                                                        onClick={() => fileDownload(JSON.stringify(switchDesc), switchDesc.dpid + ".json")}>
                                                    {switchDesc.dpid}.json
                                                </Button>
                                            </td>
                                        </tr>
                                    )}
                                    </tbody>
                                </Table>
                            </div>
                        </Collapse>
                    </Card>

                    <Card>
                        <Card.Header>
                            <Button
                                onClick={() => setFlowsOpen(!flowsOpen)}
                                aria-controls="activeFlowsBody"
                                aria-expanded={flowsOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">Flows</h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={flowsOpen}>
                            <div id="activeFlowsBody" className="cardBodyHidden">
                                {switches.map((switchDesc, index) =>
                                    <div key={switchDesc.dpid + "-" + index}>
                                        <p>Switch DPID: {switchDesc.dpid}</p>
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>Actions</th>
                                                <th>Byte count</th>
                                                <th>Cookie</th>
                                                <th>Duration (nsec)</th>
                                                <th>Duration (sec)</th>
                                                <th>Flags</th>
                                                <th>Hard timeout</th>
                                                <th>Idle timeout</th>
                                                <th>MAC source</th>
                                                <th>MAC destination</th>
                                                <th>Ethernet frame type</th>
                                                <th>In port</th>
                                                <th>VLAN ID</th>
                                                <th>VLAN PCP</th>
                                                <th>IP protocol</th>
                                                <th>IP type of service</th>
                                                <th>IP source</th>
                                                <th>IP destination</th>
                                                <th>UDP/TCP source port</th>
                                                <th>UDP/TCP destination port</th>
                                                <th>Packet count</th>
                                                <th>Priority</th>
                                                <th>Table id</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            {switchDesc.flows.map((flow, index2) =>
                                                <tr key={switchDesc.dpid + flow.duration_nsec + "-" + index + "-" + index2}>
                                                    <td>{flow.actions.join(", ")}</td>
                                                    <td>{flow.byte_count}</td>
                                                    <td>{flow.cookie}</td>
                                                    <td>{flow.duration_nsec}</td>
                                                    <td>{flow.duration_sec}</td>
                                                    <td>{flow.flags}</td>
                                                    <td>{flow.hard_timeout}</td>
                                                    <td>{flow.idle_timeout}</td>
                                                    <td>{flow.match.dl_src}</td>
                                                    <td>{flow.match.dl_dst}</td>
                                                    <td>{flow.match.dl_type}</td>
                                                    <td>{flow.match.in_port}</td>
                                                    <td>{flow.match.vlan}</td>
                                                    <td>{flow.match.vlan_pcp}</td>
                                                    <td>{flow.match.nw_proto}</td>
                                                    <td>{flow.match.nw_tos}</td>
                                                    <td>{flow.match.nw_src}</td>
                                                    <td>{flow.match.nw_dst}</td>
                                                    <td>{flow.match.tp_src}</td>
                                                    <td>{flow.match.tp_dst}</td>
                                                    <td>{flow.packet_count}</td>
                                                    <td>{flow.priority}</td>
                                                    <td>{flow.table_id}</td>
                                                </tr>
                                            )}
                                            </tbody>
                                        </Table>
                                    </div>
                                )}
                            </div>
                        </Collapse>
                    </Card>

                    <Card>
                        <Card.Header>
                            <Button
                                onClick={() => setGroupsOpen(!groupsOpen)}
                                aria-controls="activeGroupsBody"
                                aria-expanded={groupsOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">Groups</h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={groupsOpen}>
                            <div id="activeGroupsBody" className="cardBodyHidden">
                                {switches.map((switchDesc, index) =>
                                    <div key={switchDesc.dpid + "-" + index}>
                                        <p>Switch DPID: {switchDesc.dpid}</p>

                                        Group features
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>ALL actions</th>
                                                <th>SELECT actions</th>
                                                <th>INDIRECT actions</th>
                                                <th>FF actions</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            <tr>
                                                <td>{switchDesc.groupfeatures.actions[0]["ALL"].join(", ")}</td>
                                                <td>{switchDesc.groupfeatures.actions[1]["SELECT"].join(", ")}</td>
                                                <td>{switchDesc.groupfeatures.actions[2]["INDIRECT"].join(", ")}</td>
                                                <td>{switchDesc.groupfeatures.actions[3]["FF"].join(", ")}</td>
                                            </tr>
                                            </tbody>
                                        </Table>

                                        Groups
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>Group ID</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            {switchDesc.groups.map((group, index2) =>
                                                <tr key={switchDesc.dpid + group.id + "-" + index + "-" + index2}>
                                                    <td>{group.id}</td>
                                                </tr>
                                            )}
                                            </tbody>
                                        </Table>

                                        Groups descriptions
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>Group description</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            {switchDesc.groupdescs.map((groupdesc, index2) =>
                                                <tr key={switchDesc.dpid + "-" + index + "-" + index2}>
                                                    <td>{groupdesc}</td>
                                                </tr>
                                            )}
                                            </tbody>
                                        </Table>
                                    </div>
                                )}
                            </div>
                        </Collapse>
                    </Card>


                    <Card>
                        <Card.Header>
                            <Button
                                onClick={() => setMetersOpen(!metersOpen)}
                                aria-controls="activeMetersBody"
                                aria-expanded={metersOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">Meters</h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={metersOpen}>
                            <div id="activeMetersBody" className="cardBodyHidden">
                                {switches.map((switchDesc, index) =>
                                    <div key={switchDesc.dpid + "-" + index}>
                                        <p>Switch DPID: {switchDesc.dpid}</p>

                                        Meters features
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>Band types</th>
                                                <th>Capabilities</th>
                                                <th>MAX bands</th>
                                                <th>MAX color</th>
                                                <th>MAX meter</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            <tr>
                                                <td>{switchDesc.meter_features.band_types.join(", ")}</td>
                                                <td>{switchDesc.meter_features.capabilities.join(", ")}</td>
                                                <td>{switchDesc.meter_features.max_bands}</td>
                                                <td>{switchDesc.meter_features.max_color}</td>
                                                <td>{switchDesc.meter_features.max_meter}</td>
                                            </tr>
                                            </tbody>
                                        </Table>

                                        Meters
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>Meter ID</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            {switchDesc.meters.map((meter, index2) =>
                                                <tr key={switchDesc.dpid + meter.id + "-" + index + "-" + index2}>
                                                    <td>{meter.id}</td>
                                                </tr>
                                            )}
                                            </tbody>
                                        </Table>

                                        Meter configurations
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>Meter configuration</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            {switchDesc.meter_configs.map((meterConfig, index2) =>
                                                <tr key={switchDesc.dpid + "-" + index + "-" + index2}>
                                                    <td>{meterConfig}</td>
                                                </tr>
                                            )}
                                            </tbody>
                                        </Table>
                                    </div>
                                )}
                            </div>
                        </Collapse>
                    </Card>


                    <Card>
                        <Card.Header>
                            <Button
                                onClick={() => setQueuesOpen(!queuesOpen)}
                                aria-controls="activeQueuesBody"
                                aria-expanded={queuesOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">Queues</h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={queuesOpen}>
                            <div id="activeQueuesBody" className="cardBodyHidden">
                                {switches.map((switchDesc, index) =>
                                    <div key={switchDesc.dpid + "-" + index}>
                                        <p>Switch DPID: {switchDesc.dpid}</p>

                                        Queue configurations
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>Port</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            <tr>
                                                <td>{switchDesc.queueconfigs.port}</td>
                                            </tr>
                                            </tbody>
                                        </Table>

                                        Queues
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>Queue ID</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            {switchDesc.queues.map((queue, index2) =>
                                                <tr key={switchDesc.dpid + queue.id + "-" + index + "-" + index2}>
                                                    <td>{queue.id}</td>
                                                </tr>
                                            )}
                                            </tbody>
                                        </Table>
                                    </div>
                                )}
                            </div>
                        </Collapse>
                    </Card>

                    <Card>
                        <Card.Header>
                            <Button
                                onClick={() => setRolesOpen(!rolesOpen)}
                                aria-controls="activeRolesBody"
                                aria-expanded={rolesOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">Roles</h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={rolesOpen}>
                            <div id="activeRolesBody" className="cardBodyHidden">
                                {switches.map((switchDesc, index) =>
                                    <div key={switchDesc.dpid + "-" + index}>
                                        <p>Switch DPID: {switchDesc.dpid}</p>

                                        Role configurations
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>Role</th>
                                                <th>Generation id</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            <tr>
                                                <td>{switchDesc.roles.role}</td>
                                                <td>{switchDesc.roles.generation_id}</td>
                                            </tr>
                                            </tbody>
                                        </Table>
                                    </div>
                                )}
                            </div>
                        </Collapse>
                    </Card>

                    <Card>
                        <Card.Header>
                            <Button
                                onClick={() => setTablesOpen(!tablesOpen)}
                                aria-controls="activeTablesBody"
                                aria-expanded={tablesOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">Tables</h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={tablesOpen}>
                            <div id="activeTablesBody" className="cardBodyHidden">
                                {switches.map((switchDesc, index) =>
                                    <div key={switchDesc.dpid + "-" + index}>
                                        <p>Switch DPID: {switchDesc.dpid}</p>

                                        Tables
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>Table id</th>
                                                <th>Active flows count</th>
                                                <th>Lookup count</th>
                                                <th>Matched count</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            {switchDesc.tables.map((table, index2) =>
                                                <tr key={switchDesc.dpid + table.table_id + "-" + index + "-" + index2}>
                                                    <td>{table.table_id}</td>
                                                    <td>{table.active_count}</td>
                                                    <td>{table.lookup_count}</td>
                                                    <td>{table.matched_count}</td>
                                                </tr>
                                            )}
                                            </tbody>
                                        </Table>

                                        Table features
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>Config</th>
                                                <th>Max entries</th>
                                                <th>Metadata match</th>
                                                <th>Metadata write</th>
                                                <th>Name</th>
                                                <th>Table id</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            {switchDesc.tablefeatures.map((tablefeature, index2) =>
                                                <tr key={switchDesc.dpid + tablefeature.table_id + "-" + index + "-" + index2}>
                                                    <td>{tablefeature.config}</td>
                                                    <td>{tablefeature.max_entries}</td>
                                                    <td>{tablefeature.metadata_match}</td>
                                                    <td>{tablefeature.metadata_write}</td>
                                                    <td>{tablefeature.name}</td>
                                                    <td>{tablefeature.table_id}</td>
                                                </tr>
                                            )}
                                            </tbody>
                                        </Table>
                                    </div>
                                )}
                            </div>
                        </Collapse>
                    </Card>

                    <Card>
                        <Card.Header>
                            <Button
                                onClick={() => setPortsOpen(!portsOpen)}
                                aria-controls="activePortsBody"
                                aria-expanded={portsOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">Ports</h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={portsOpen}>
                            <div id="activePortsBody" className="cardBodyHidden">
                                {switches.map((switchDesc, index) =>
                                    <div key={switchDesc.dpid + "-" + index}>
                                        <p>Switch DPID: {switchDesc.dpid}</p>

                                        Ports
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>Name</th>
                                                <th>MAC address</th>
                                                <th>Advertised</th>
                                                <th>Config</th>
                                                <th>Current</th>
                                                <th>Current speed</th>
                                                <th>Max speed</th>
                                                <th>Peer</th>
                                                <th>Port number</th>
                                                <th>State</th>
                                                <th>Supported</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            {switchDesc.portdescs.map((port, index2) =>
                                                <tr key={switchDesc.dpid + port.name + "-" + index + "-" + index2}>
                                                    <td>{port.name}</td>
                                                    <td>{port.hw_addr}</td>
                                                    <td>{port.advertised}</td>
                                                    <td>{port.config}</td>
                                                    <td>{port.curr}</td>
                                                    <td>{port.curr_speed}</td>
                                                    <td>{port.max_speed}</td>
                                                    <td>{port.peer}</td>
                                                    <td>{port.port_no}</td>
                                                    <td>{port.state}</td>
                                                    <td>{port.supported}</td>
                                                </tr>
                                            )}
                                            </tbody>
                                        </Table>

                                        Port statistics
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>Port number</th>
                                                <th>Collisions</th>
                                                <th>Duration (nsec)</th>
                                                <th>Duration (sec)</th>
                                                <th>Received bytes</th>
                                                <th>Received CRC errors</th>
                                                <th>Received dropped</th>
                                                <th>Received errors</th>
                                                <th>Received frame errors</th>
                                                <th>Received overrun errors</th>
                                                <th>Received packets</th>
                                                <th>Transmitted bytes</th>
                                                <th>Transmission errors</th>
                                                <th>Transmitted packets</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            {switchDesc.portstats.map((portStat, index2) =>
                                                <tr key={switchDesc.dpid + portStat.port_no + "-" + index + "-" + index2}>
                                                    <td>{portStat.port_no}</td>
                                                    <td>{portStat.collisions}</td>
                                                    <td>{portStat.duration_nsec}</td>
                                                    <td>{portStat.duration_sec}</td>
                                                    <td>{portStat.rx_bytes}</td>
                                                    <td>{portStat.rx_crc_err}</td>
                                                    <td>{portStat.rx_dropped}</td>
                                                    <td>{portStat.rx_errors}</td>
                                                    <td>{portStat.rx_frame_err}</td>
                                                    <td>{portStat.rx_over_err}</td>
                                                    <td>{portStat.rx_packets}</td>
                                                    <td>{portStat.tx_bytes}</td>
                                                    <td>{portStat.tx_dropped}</td>
                                                    <td>{portStat.tx_errors}</td>
                                                    <td>{portStat.tx_packets}</td>
                                                </tr>
                                            )}
                                            </tbody>
                                        </Table>
                                    </div>
                                )}
                            </div>
                        </Collapse>
                    </Card>

                </Card.Body>
            </Accordion.Collapse>
        </Card>)
}

SDNController.propTypes = {};
SDNController.defaultProps = {};
export default SDNController;