function getSensorId() {
    return sessionStorage.sensorId || 1;
}

function setSensorId(id) {
    sessionStorage.sensorId = id;
}
