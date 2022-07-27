import React, {useState, useEffect, useCallback, createRef} from 'react';
import Modal from 'react-bootstrap/Modal'
import Accordion from 'react-bootstrap/Accordion';
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Experiment from "./Experiment/Experiment";
import './TrainingResults.css';
import TrainingEnv from './RL_training_env.png'
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import Select from 'react-select'
import { useDebouncedCallback } from 'use-debounce';
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';

const TrainingResults = () => {
    const [experimentsIds, setExperimentsIds] = useState([]);
    const [selectedExperimentId, setSelectedExperimentId] = useState(null);
    const [selectedExperiment, setSelectedExperiment] = useState(null);
    const [loading, setLoading] = useState(true);
    const [loadingSelectedExperiment, setLoadingSelectedExperiment] = useState(true);
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [filteredExperimentsIds, setFilteredExperimentsIds] = useState([]);
    const [searchString, setSearchString] = useState("");

    const ip = "localhost"
    // const ip = "172.31.212.92"

    const fetchExperiments = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/experiments?ids=true',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                const experimentIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: "ID: " + id_obj.id + ", simulation: " + id_obj.simulation + ", emulation: " + id_obj.emulation
                    }
                })
                setExperimentsIds(experimentIds)
                setFilteredExperimentsIds(experimentIds)
                setLoading(false)
                if (experimentIds.length > 0) {
                    setSelectedExperimentId(experimentIds[0])
                    fetchExperiment(experimentIds[0])
                    setLoadingSelectedExperiment(true)
                } else {
                    setLoadingSelectedExperiment(false)
                    setSelectedExperiment(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchExperiments()
    }, [fetchExperiments]);

    const fetchExperiment = useCallback((experiment_id) => {
        fetch(
            `http://` + ip + ':7777/experiments/' + experiment_id.value,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSelectedExperiment(response)
                setLoadingSelectedExperiment(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeExperimentRequest = useCallback((experiment_id) => {
        fetch(
            `http://` + ip + ':7777/experiments/' + experiment_id,
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchExperiments()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllExperimentsRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/experiments',
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchExperiments()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeExperiment = (experiment) => {
        setLoading(true)
        removeExperimentRequest(experiment.id)
    }

    const refresh = () => {
        setLoading(true)
        fetchExperiments()
    }

    const info = () => {
        setShowInfoModal(true)
    }

    const removeAllExperiments = () => {
        setLoading(true)
        removeAllExperimentsRequest()
        setSelectedExperiment(null)
    }

    const updateSelectedExperimentId = (selectedId) => {
        setSelectedExperimentId(selectedId)
        fetchExperiment(selectedId)
        setLoadingSelectedExperiment(true)
    }

    const removeAllExperimentsConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all experiments? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllExperiments()
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({ onClose }) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete all experiments? this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllExperiments()
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete them.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removeExperimentConfirm = (experiment) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the experiment with ID: ' + experiment.id +
                "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeExperiment(experiment)
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({ onClose }) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete the experiment with ID {experiment.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeExperiment(experiment)
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete it.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const SelectExperimentOrSpinner = (props) => {
        if (!props.loading && props.experimentIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No training runs are available</span>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.loading) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching training runs... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Training run:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "600px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedExperimentId}
                                defaultValue={props.selectedExperimentId}
                                options={props.experimentIds}
                                onChange={updateSelectedExperimentId}
                                placeholder="Select training run"
                            />
                        </div>
                    </div>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderInfoTooltip}
                    >
                        <Button variant="button" onClick={info}>
                            <i className="fa fa-info-circle infoButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveAllExperimentsTooltip}
                    >
                        <Button variant="danger" onClick={removeAllExperimentsConfirm} size="sm">
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload training runs from the backend
        </Tooltip>
    );

    const renderRemoveAllExperimentsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all training runs
        </Tooltip>
    );

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the training runs
        </Tooltip>
    );

    const searchFilter = (experimentId, searchVal) => {
        return (searchVal === "" || experimentId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const fExpIds = experimentsIds.filter(exp => {
            return searchFilter(exp, searchVal)
        });
        setFilteredExperimentsIds(fExpIds)
        setSearchString(searchVal)

        var selectedExperimentRemoved = false
        if(!loadingSelectedExperiment && fExpIds.length > 0){
            for (let i = 0; i < fExpIds.length; i++) {
                if(selectedExperiment !== null && selectedExperiment !== undefined &&
                    selectedExperiment.id === fExpIds[i].value) {
                    selectedExperimentRemoved = true
                }
            }
            if(!selectedExperimentRemoved) {
                setSelectedExperimentId(fExpIds[0])
                fetchExperiment(fExpIds[0])
                setLoadingSelectedExperiment(true)
            }
        } else {
            setSelectedExperiment(null)
        }
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

    const InfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter">
                        Policy training
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Training policies using reinforcement learning</h4>
                    <p className="modalText">
                        Policies are trained through reinforcement learning in the simulation system.
                        Different reinforcement learning algorithms can be used, e.g. PPO, T-SPSA, DQN, etc.
                    </p>
                    <div className="text-center">
                        <img src={TrainingEnv} alt="Emulated infrastructures"/>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const wrapper = createRef();

    const TrainingRunAccordion = (props) => {
        if (props.loadingSelectedExperiment || props.selectedExperiment === null || props.selectedExperiment === undefined) {
            if(props.loadingSelectedExperiment) {
                return (
                    <Spinner animation="border" role="status">
                        <span className="visually-hidden"></span>
                    </Spinner>)
            } else {
                return (
                    <p></p>
                )
            }
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    <Experiment experiment={props.selectedExperiment} wrapper={wrapper}
                                key={props.selectedExperiment.id}
                                removeExperiment={removeExperimentConfirm}
                    />
                </Accordion>
            )
        }
    }

    return (
        <div className="TrainingResults">
            <div className="row">
                <div className="col-sm-6">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectExperimentOrSpinner loading={loading}
                                                   experimentIds={filteredExperimentsIds}
                                                   selectedExperimentId={selectedExperimentId}
                        />
                    </h4>
                </div>
                <div className="col-sm-4">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="basic-addon1" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="Search"
                                aria-describedby="basic-addon1"
                                onChange={searchHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2">
                </div>
            </div>
            <TrainingRunAccordion loadingSelectedExperiment={loadingSelectedExperiment}
                                  selectedExperiment={selectedExperiment}/>
        </div>
    );
}

TrainingResults.propTypes = {};
TrainingResults.defaultProps = {};
export default TrainingResults;
