if (
    ($network.wifi.ssid && $persistentStore.read("bypass_wifi") === "true") ||
    (!$network.wifi.ssid && $persistentStore.read("bypass_cellular") === "true")
) {
    $done({servers: [
        "https://cloudflare-dns.com/dns-query",
        "quic://ultralow.dns.nextdns.io"
    ]})
}
else {
    $done({servers: [
        "quic://dns.alidns.com",
        "https://dns.alidns.com/dns-query",
        "https://doh.pub/dns-query"
    ]})
}
