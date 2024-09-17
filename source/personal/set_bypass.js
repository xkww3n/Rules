const GLOBAL_WIFI = [
    "BOCHK-WiFi",
    "HSBC-Guest",
    "MTR-WIFI",
    "McDonald's"
];

var bypass;

if ($network.wifi.ssid) {
    if (GLOBAL_WIFI.includes($network.wifi.ssid)) {
        bypass = 1;
    }
    else {
        bypass = 0;
    };
    $persistentStore.write(bypass, "bypass");
    $done();
}
else {
    try {
        if ($indent.parameter === "内地") {
            bypass = 0;
        }
        else {
            bypass = 1;
        }
        $persistentStore.write(bypass, "bypass");
        $done();
    }
    catch (err) {
        $done();
    }
}
