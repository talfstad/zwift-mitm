#### Connecting Zwift to a Fake Companion App
Goal: Fool Zwift App into thinking a computer on the local network is actually the Zwift companion app.

Communication:
- TCP port: **21587**
- Messages sent and received using Protobuf. The first 4 bytes are the message length in hex

Research Goals:
1. I want to know exactly what API calls are made from a ZC app to tell Zwift the companion app is ready
2. I want to verify this by spoofing these calls and receiving data on my computer

If I can do this, I can man in the middle the Zwift Companion App, and send whatever calls I want to Zwift.
Also, it will make it possible to keep internal state of the app to create new potential functionality.



API Calls:
To capture API calls from Zwift Companion, I set up an SSL HTTP Proxy using [Charles Proxy](https://www.charlesproxy.com/).

**PUT - https://us-or-rly101.zwift.com/relay/profiles/me/phone**
```
{
	"protocol": "TCP",
	"mobileEnvironment": {
		"systemHardware": "iPad6,3",
		"appBuild": 553,
		"systemOSVersion": "12.1.1",
		"appVersion": "3.1.1",
		"systemOS": "iOS",
		"appDisplayName": "Companion"
	},
	"phoneAddress": "192.168.0.18",
	"port": 21587
}
```

1. Run a local server on my local machine to capture traffic.

2. Seamlessly forward traffic to actual ZC
  1. launch Zwift Companion
  2. launch my server
  3. launch Zwift App


1. The Zwift Companion App will save the IP to the zwift endpoint,
2. my server will jack it and use it as the address to forward info to
3. I will tell zwift to connect to me


So, we need to have a box that does the MITM and is connected to wifi.
Then we have a switch just like before. We can still have an app that
can re-program the button via iPhone app.

- box is plugged into wall
- iPhone connects via BLE
- configure wifi on machine via app
- button connects to box via app
- button is configured in app

Box gets updates on launch with latest code. Box connected to the BLE button which goes on the bike
