if ($network.wifi.ssid) {
    var match = ($persistentStore.read("bypass_wifi") === "true");
}
else {
    var match = ($persistentStore.read("bypass_cellular") === "true");
}

$done({matched: match});
