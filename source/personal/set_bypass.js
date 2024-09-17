const GLOBAL_WIFI = [
    "BOCHK-WiFi",
    "HSBC-Guest",
    "MTR-WIFI",
    "McDonald's"
];

var bypass_cellular = true;
var bypass_wifi = true;

try {
    if ($intent.parameter === "内地") {
        bypass_cellular = false;
    }
    else {
        bypass_cellular = true;
    }
    $persistentStore.write(bypass_cellular, "bypass_cellular");
}
catch (err) { // triggered by network-changed event, no `$intent` passed in
    if ($network.wifi.ssid) {
        if (GLOBAL_WIFI.includes($network.wifi.ssid)){
            bypass_wifi = true;
        }
        else {
            bypass_wifi = false;
        }
        $persistentStore.write(bypass_wifi, "bypass_wifi");
    }
}
finally {
    $done();
}
