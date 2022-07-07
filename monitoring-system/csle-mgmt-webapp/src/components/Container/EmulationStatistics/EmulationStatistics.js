import React, {useState, useEffect, useCallback} from 'react';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import Select from 'react-select'
import ConditionalHistogramDistribution from "./ConditionalHistogramDistribution/ConditionalHistogramDistribution";
import './EmulationStatistics.css';
import DataCollection from './DataCollection.png'
import Collapse from 'react-bootstrap/Collapse'
import Card from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table'
import fileDownload from 'react-file-download'
import {useDebouncedCallback} from 'use-debounce';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';

const EmulationStatistics = () => {
    const [emulationStatisticIds, setEmulationStatisticIds] = useState([]);
    const [filteredEmulationStatisticIds, setFilteredEmulationStatisticIds] = useState([]);
    const [selectedEmulationStatistic, setSelectedEmulationStatistic] = useState(null);
    const [selectedEmulationStatisticId, setSelectedEmulationStatisticId] = useState(null);
    const [conditionals, setConditionals] = useState([]);
    const [selectedConditionals, setSelectedConditionals] = useState(null);
    const [metrics, setMetrics] = useState([]);
    const [selectedMetric, setSelectedMetric] = useState(null);
    const [loading, setLoading] = useState(true);
    const [loadingSelectedEmulationStatistic, setLoadingSelectedEmulationStatistic] = useState(true);
    const [animationDuration, setAnimationDuration] = useState(5);
    const animationDurationFactor = 50000
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [deltaCountsOpen, setDeltaCountsOpen] = useState(false);
    const [initialCountsOpen, setInitialCountsOpen] = useState(false);
    const [deltaProbsOpen, setDeltaProbsOpen] = useState(false);
    const [initialProbsOpen, setInitialProbsOpen] = useState(false);
    const [descriptiveStatsOpen, setDescriptiveStatsOpen] = useState(false);
    const [searchString, setSearchString] = useState("");

    const ip = "localhost"
    // const ip = "172.31.212.92"

    const resetState = () => {
        setEmulationStatisticIds([])
        setSelectedEmulationStatistic(null)
        setConditionals([])
        setSelectedConditionals(null)
        setMetrics([])
        setSelectedMetric(null)
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload statistics from the backend
        </Tooltip>
    );

    const refresh = () => {
        setLoading(true)
        resetState()
        fetchEmulationStatisticsIds()
    }

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the statistics
        </Tooltip>
    );

    const renderRemoveStatisticTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove the selected statistics.
        </Tooltip>
    );

    const InfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="xl"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter">
                        Emulation statistics
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Emulation statistics</h4>
                    <p className="modalText">
                        The emulation statistics are collected by measuring log files and other metrics from
                        the emulated infrastructure under different system conditions, e.g. intrusion and no intrsion,
                        high load and low load etc.
                    </p>
                    <div className="text-center">
                        <img src={DataCollection} alt="Data collection from the emulation"/>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const updateEmulationStatistic = (stat) => {
        setSelectedEmulationStatistic(stat)
        const conditionalOptions = Object.keys(stat.value.conditionals_counts).map((conditionalName, index) => {
            return {
                value: conditionalName,
                label: conditionalName
            }
        })
        setConditionals(conditionalOptions)
        setSelectedConditionals([conditionalOptions[0]])
        const metricOptions = Object.keys(stat.value.conditionals_counts[
            Object.keys(stat.value.conditionals_counts)[0]]).map((metricName, index) => {
            return {
                value: metricName,
                label: metricName
            }
        })
        setMetrics(metricOptions)
        setSelectedMetric(metricOptions[0])
    }
    const updateSelectedConditionals = (selected) => {
        setSelectedConditionals(selected)
    }

    const updateMetric = (metricName) => {
        setSelectedMetric(metricName)
    }

    const getFirstTwoConditionals = () => {
        if (selectedConditionals.length >= 2) {
            return [selectedConditionals[0], selectedConditionals[1]]
        } else {
            return selectedConditionals
        }
    }

    const getNumSamples = (statistic) => {
        var num_samples = 0
        for (let i = 0; i < Object.keys(statistic.conditionals_counts).length; i++) {
            var metric = Object.keys(statistic.conditionals_counts[Object.keys(statistic.conditionals_counts)[i]])[0]
            for (let j = 0; j < Object.keys(statistic.conditionals_counts[Object.keys(statistic.conditionals_counts)[i]][metric]).length; j++) {
                var value = Object.keys(statistic.conditionals_counts[Object.keys(statistic.conditionals_counts)[i]][metric])[j]
                num_samples = num_samples + statistic.conditionals_counts[Object.keys(statistic.conditionals_counts)[i]][metric][value]
            }
        }
        return num_samples
    }

    const updateEmulationStatisticId = (emulationStatisticId) => {
        setSelectedEmulationStatisticId(emulationStatisticId)
        fetchEmulationStatistic(emulationStatisticId)
        setLoadingSelectedEmulationStatistic(true)
    }

    const fetchEmulationStatisticsIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/emulationstatisticsdataids',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                const statisticsIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: "ID: " + id_obj.id + ", emulation: " + id_obj.emulation
                    }
                })
                setEmulationStatisticIds(statisticsIds)
                setFilteredEmulationStatisticIds(statisticsIds)
                setLoading(false)
                if (statisticsIds.length > 0) {
                    setSelectedEmulationStatisticId(statisticsIds[0])
                    fetchEmulationStatistic(statisticsIds[0])
                    setLoadingSelectedEmulationStatistic(true)
                } else {
                    setLoadingSelectedEmulationStatistic(false)
                    setSelectedEmulationStatistic(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchEmulationStatisticsIds()
    }, [fetchEmulationStatisticsIds]);


    const fetchEmulationStatistic = useCallback((statistic_id) => {
        fetch(
            `http://` + ip + ':7777/emulationstatisticsdata/get/' + statistic_id.value,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSelectedEmulationStatistic(response)
                setLoadingSelectedEmulationStatistic(false)

                if (response !== null && response !== undefined && !(Object.keys(response).length === 0)) {
                    const conditionalOptions = Object.keys(response.conditionals_counts).map((conditionalName, index) => {
                        return {
                            value: conditionalName,
                            label: conditionalName
                        }
                    })
                    setConditionals(conditionalOptions)
                    setSelectedConditionals([conditionalOptions[0]])
                    const metricOptions = Object.keys(response.conditionals_counts[Object.keys(
                        response.conditionals_counts)[0]]).map((metricName, index) => {
                        return {
                            value: metricName,
                            label: metricName
                        }
                    })
                    setMetrics(metricOptions)
                    setSelectedMetric(metricOptions[0])
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeEmulationStatisticRequest = useCallback((statistic_id) => {
        fetch(
            `http://` + ip + ':7777/emulationstatisticsdata/remove/' + statistic_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchEmulationStatisticsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeStatistic = (stat) => {
        setLoading(true)
        resetState()
        removeEmulationStatisticRequest(stat.id)
        setSelectedEmulationStatistic(null)
    }

    const searchFilter = (statIdObj, searchVal) => {
        return (searchVal === "" || statIdObj.label.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const filteredEmStatsIds = emulationStatisticIds.filter(stat_id_obj => {
            return searchFilter(stat_id_obj, searchVal)
        });
        setFilteredEmulationStatisticIds(filteredEmStatsIds)
        setSearchString(searchVal)

        var selectedStatRemoved = false
        if (!loadingSelectedEmulationStatistic && filteredEmStatsIds.length > 0) {
            for (let i = 0; i < filteredEmStatsIds.length; i++) {
                if (selectedEmulationStatistic !== null && selectedEmulationStatistic !== undefined &&
                    selectedEmulationStatistic.id === filteredEmStatsIds[i].value) {
                    selectedStatRemoved = true
                }
            }
            if (!selectedStatRemoved) {
                setSelectedEmulationStatisticId(filteredEmStatsIds[0])
                fetchEmulationStatistic(filteredEmStatsIds[0])
                setLoadingSelectedEmulationStatistic(true)
            }
        } else {
            setSelectedEmulationStatistic(null)
        }
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

    const SelectEmulationStatisticDropdownOrSpinner = (props) => {
        if (!props.loading && props.emulationStatisticsIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No statistics are available</span>
                    <OverlayTrigger
                        placement="right"
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
                    <span className="spinnerLabel"> Fetching statistics... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="inline-block">
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderInfoTooltip}
                    >
                        <Button variant="button" onClick={() => setShowInfoModal(true)}>
                            <i className="fa fa-info-circle infoButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <OverlayTrigger
                        className="removeButton"
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveStatisticTooltip}
                    >
                        <Button variant="danger" className="removeButton"
                                onClick={() => removeStatistic(selectedEmulationStatistic)}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Statistic:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "400px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedEmulationStatisticId}
                                defaultValue={props.selectedEmulationStatisticId}
                                options={props.emulationStatisticsIds}
                                onChange={updateEmulationStatisticId}
                                placeholder="Select statistic"
                            />
                        </div>
                    </div>
                </div>
            )
        }
    }

    const SelectConditionalDistributionDropdownOrSpinner = (props) => {
        if (!props.loading && props.conditionals.length === 0) {
            return (
                <span>  </span>
            )
        }
        if (props.loading || props.selectedConditional === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div className="conditionalDist inline-block">
                    <h4>
                        <div className="conditionalDist inline-block conditionalLabel">
                            Conditionals:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "800px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedConditionals}
                                isMulti={true}
                                defaultValue={props.selectedConditionals}
                                options={props.conditionals}
                                onChange={updateSelectedConditionals}
                                placeholder="Select conditional distributions"
                            />
                        </div>
                    </h4>
                </div>
            )
        }
    }

    const SelectMetricDistributionDropdownOrSpinner = (props) => {
        if (!props.loading && props.metrics.length === 0) {
            return (
                <span>  </span>
            )
        }
        if (props.loading || props.selectedMetric === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div className="conditionalDist inline-block metricLabel">
                    <h4>
                        <div className="conditionalDist inline-block conditionalLabel">
                            Metric:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "500px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedMetric}
                                defaultValue={props.selectedMetric}
                                options={props.metrics}
                                onChange={updateMetric}
                                placeholder="Select metric"
                            />
                        </div>
                    </h4>
                </div>
            )
        }
    }

    const conditionalPairs = () => {
        if (selectedConditionals.length < 2) {
            return []
        } else {
            var conditionalPairs = []
            for (let i = 0; i < selectedConditionals.length; i++) {
                for (let j = 0; j < selectedConditionals.length; j++) {
                    if (selectedConditionals[i] !== selectedConditionals[j]) {
                        conditionalPairs.push({
                            "conditional_1": selectedConditionals[i].label,
                            "conditional_2": selectedConditionals[j].label
                        })
                    }
                }
            }
            return conditionalPairs
        }
    }

    const SelectedEmulationStatisticView = (props) => {
        if (props.loadingSelectedEmulationStatistic || props.selectedEmulationStatistic === null
            || props.selectedEmulationStatistic === undefined) {
            if (props.loadingSelectedEmulationStatistic) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching emulation statistic... </span>
                        <Spinner animation="border" role="status">
                            <span className="visually-hidden"></span>
                        </Spinner>
                    </h3>)
            } else {
                return (
                    <p></p>
                )
            }
        } else {
            return (
                <div>
                    <SelectConditionalDistributionDropdownOrSpinner conditionals={props.conditionals}
                                                                    selectedConditionals={props.selectedConditionals}
                                                                    loading={props.loading}/>
                    <SelectMetricDistributionDropdownOrSpinner metrics={props.metrics}
                                                               selectedMetric={props.selectedMetric}
                                                               loading={props.loading}/>

                    <StatisticDescriptionOrSpinner selectedEmulationStatistic={props.selectedEmulationStatistic}
                                                   loading={props.loading}/>

                    <ConditionalChartsOrSpinner key={props.animationDuration}
                                                selectedEmulationStatistic={props.selectedEmulationStatistic}
                                                selectedConditionals={props.selectedConditionals}
                                                animationDurationFactor={props.animationDurationFactor}
                                                animationDuration={props.animationDuration}
                                                conditionals={props.conditionals}
                                                selectedMetric={props.selectedMetric}
                                                metrics={props.metrics}
                                                loading={props.loading}
                    />
                </div>
            )
        }
    }

    const StatisticDescriptionOrSpinner = (props) => {
        if (props.loading || props.selectedEmulationStatistic === null ||
            props.selectedEmulationStatistic === undefined) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div>
                    <p className="statisticDescription">
                        Statistic description: {props.selectedEmulationStatistic.descr}
                        <span className="numSamples">
                        Number of samples: {getNumSamples(props.selectedEmulationStatistic)}
                    </span>
                    </p>
                </div>
            )
        }
    }

    const ConditionalChartsOrSpinner = (props) => {
        if (props.selectedEmulationStatistic === null || props.selectedEmulationStatistic === undefined) {
            return (
                <p className></p>
            )
        }
        if (!props.loading && props.selectedConditionals !== null && props.selectedConditionals !== undefined &&
            props.selectedConditionals.length === 0) {
            return (
                <p className="statisticDescription">Select a conditional distribution from the dropdown list.</p>
            )
        }
        if (props.loading || props.selectedConditionals === null || props.selectedConditionals.length === 0
            || props.selectedMetric === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div>
                    <div className="row chartsRow">
                        <Card className="col-sm-12">
                            <Card.Header>
                                <Button
                                    onClick={() => setDeltaCountsOpen(!deltaCountsOpen)}
                                    aria-controls="deltaCountsBody"
                                    aria-expanded={deltaCountsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">Delta value count distributions</h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={deltaCountsOpen}>
                                <div id="deltaCountsBody" className="cardBodyHidden">
                                    <div className="col-sm-12 conditionalHisto">
                                        <ConditionalHistogramDistribution
                                            data={props.selectedEmulationStatistic.conditionals_counts}
                                            selectedConditionals={getFirstTwoConditionals()}
                                            selectedMetric={props.selectedMetric}
                                            title1={"Delta counts: " + props.selectedMetric.value}
                                            title2={"Delta counts: " + props.selectedMetric.value}
                                            animationDuration={props.animationDuration}
                                            animationDurationFactor={props.animationDurationFactor}
                                            yAxisLabel={"Count"}
                                        />
                                    </div>
                                </div>
                            </Collapse>
                        </Card>

                        <Card className="col-sm-12">
                            <Card.Header>
                                <Button
                                    onClick={() => setInitialCountsOpen(!initialCountsOpen)}
                                    aria-controls="initialCountsBody"
                                    aria-expanded={initialCountsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">Initial value count distributions</h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={initialCountsOpen}>
                                <div id="initialCountsBody" className="cardBodyHidden">
                                    <div className="col-sm-12 conditionalHisto">
                                        <ConditionalHistogramDistribution
                                            data={props.selectedEmulationStatistic.initial_distributions_counts}
                                            selectedConditionals={[]}
                                            selectedMetric={props.selectedMetric}
                                            title1={"Initial counts of::" + props.selectedMetric.value}
                                            title2={"Initial counts of:" + props.selectedMetric.value}
                                            animationDuration={props.animationDuration}
                                            animationDurationFactor={props.animationDurationFactor}
                                            yAxisLabel={"Count"}
                                        />
                                    </div>
                                </div>
                            </Collapse>
                        </Card>

                        <Card className="col-sm-12">
                            <Card.Header>
                                <Button
                                    onClick={() => setDeltaProbsOpen(!deltaProbsOpen)}
                                    aria-controls="deltaProbsBody"
                                    aria-expanded={deltaProbsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">Delta value probability distributions</h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={deltaProbsOpen}>
                                <div id="deltaProbsBody" className="cardBodyHidden">
                                    <div className="col-sm-12 conditionalHisto">
                                        <ConditionalHistogramDistribution
                                            data={props.selectedEmulationStatistic.conditionals_probs}
                                            selectedConditionals={getFirstTwoConditionals()}
                                            selectedMetric={props.selectedMetric}
                                            title1={"Delta probabilities: " + props.selectedMetric.value}
                                            title2={"Delta probabilities: " + props.selectedMetric.value}
                                            animationDuration={props.animationDuration}
                                            animationDurationFactor={props.animationDurationFactor}
                                            yAxisLabel={"Probability"}
                                        />
                                    </div>
                                </div>
                            </Collapse>
                        </Card>

                        <Card className="col-sm-12">
                            <Card.Header>
                                <Button
                                    onClick={() => setInitialProbsOpen(!initialProbsOpen)}
                                    aria-controls="initialProbsBody"
                                    aria-expanded={initialProbsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">
                                        Initial value probability distributions
                                    </h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={initialProbsOpen}>
                                <div id="initialProbsBody" className="cardBodyHidden">
                                    <div className="col-sm-12 conditionalHisto">
                                        <ConditionalHistogramDistribution
                                            data={props.selectedEmulationStatistic.initial_distributions_probs}
                                            selectedConditionals={[]}
                                            selectedMetric={props.selectedMetric}
                                            title1={"Initial counts of::" + props.selectedMetric.value}
                                            title2={"Initial counts of:" + props.selectedMetric.value}
                                            animationDuration={props.animationDuration}
                                            animationDurationFactor={props.animationDurationFactor}
                                            yAxisLabel={"Probability"}
                                        />
                                    </div>
                                </div>
                            </Collapse>
                        </Card>

                        <Card className="col-sm-12">
                            <Card.Header>
                                <Button
                                    onClick={() => setDescriptiveStatsOpen(!descriptiveStatsOpen)}
                                    aria-controls="descriptiveStatsBody"
                                    aria-expanded={descriptiveStatsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">
                                        Descriptive statistics
                                    </h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={descriptiveStatsOpen}>
                                <div id="descriptiveStatsBody" className="cardBodyHidden">
                                    <div className="table-responsive">
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>Attribute</th>
                                                <th> Value</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            {props.selectedConditionals.map((conditional, index) => {
                                                return (
                                                    <tr key={conditional.label + "-" + index}>
                                                        <td>{conditional.label} mean</td>
                                                        <td>{props.selectedEmulationStatistic.means[conditional.label][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}
                                            {props.selectedConditionals.map((conditional, index) => {
                                                return (
                                                    <tr key={conditional.label + "-" + index}>
                                                        <td>{conditional.label} standard deviation</td>
                                                        <td>{props.selectedEmulationStatistic.stds[conditional.label][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}

                                            {props.selectedConditionals.map((conditional, index) => {
                                                return (
                                                    <tr key={conditional.label + "-" + index}>
                                                        <td>{conditional.label} minimum value</td>
                                                        <td>{props.selectedEmulationStatistic.mins[conditional.label][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}

                                            {props.selectedConditionals.map((conditional, index) => {
                                                return (
                                                    <tr key={conditional.label + "-" + index}>
                                                        <td>{conditional.label} maximum value</td>
                                                        <td>{props.selectedEmulationStatistic.maxs[conditional.label][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}
                                            <tr>
                                                <td>Initial value mean</td>
                                                <td>{props.selectedEmulationStatistic.initial_means[props.selectedMetric.label]}</td>
                                            </tr>
                                            <tr>
                                                <td>Initial value standard deviation</td>
                                                <td>{props.selectedEmulationStatistic.initial_stds[props.selectedMetric.label]}</td>
                                            </tr>
                                            <tr>
                                                <td>Initial minimum value</td>
                                                <td>{props.selectedEmulationStatistic.initial_mins[props.selectedMetric.label]}</td>
                                            </tr>
                                            <tr>
                                                <td>Initial maximum value</td>
                                                <td>{props.selectedEmulationStatistic.initial_maxs[props.selectedMetric.label]}</td>
                                            </tr>
                                            {conditionalPairs().map((conditionalPair, index) => {
                                                return (
                                                    <tr key={conditionalPair.conditional_1 + "-" +
                                                        conditionalPair.conditional_2 + "-" + index}>
                                                        <td>Kullback-Leibler divergence between conditional
                                                            "{conditionalPair.conditional_1}" and
                                                            "{conditionalPair.conditional_2}"
                                                        </td>
                                                        <td>{props.selectedEmulationStatistic.conditionals_kl_divergences[conditionalPair.conditional_1][conditionalPair.conditional_2][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}
                                            <tr>
                                                <td>Data</td>
                                                <td>
                                                    <Button variant="link"
                                                            onClick={() => fileDownload(JSON.stringify(props.selectedEmulationStatistic), "config.json")}>
                                                        data.json
                                                    </Button>
                                                </td>
                                            </tr>
                                            </tbody>
                                        </Table>
                                    </div>
                                </div>
                            </Collapse>
                        </Card>
                    </div>
                </div>
            )
        }
    }


    return (
        <div className="emulationStatistics">
            <div className="row">
                <div className="col-sm-6">
                    <h4>
                        <SelectEmulationStatisticDropdownOrSpinner
                            emulationStatisticsIds={filteredEmulationStatisticIds}
                            selectedEmulationStatisticId={selectedEmulationStatisticId}
                            loading={loading}
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
            <SelectedEmulationStatisticView conditionals={conditionals}
                                            selectedConditionals={selectedConditionals}
                                            loading={loadingSelectedEmulationStatistic}
                                            metrics={metrics}
                                            selectedMetric={selectedMetric}
                                            loadingSelectedEmulationStatistic={loadingSelectedEmulationStatistic}
                                            selectedEmulationStatistic={selectedEmulationStatistic}
                                            animationDuration={animationDuration}
                                            animationDurationFactor={animationDurationFactor}
            />
        </div>
    );
}

EmulationStatistics.propTypes = {};
EmulationStatistics.defaultProps = {};
export default EmulationStatistics;