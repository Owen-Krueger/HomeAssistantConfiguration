<div align="center">
<h1>Owen's Home Assistant Configuration</h1>
<a href="https://github.com/Owen-Krueger/HomeAssistantConfiguration/commits/master"><img src="https://img.shields.io/github/last-commit/Owen-Krueger/HomeAssistantConfiguration.svg"/></a>
</div>

This is my personal [Home Assistant](https://www.home-assistant.io/) configuration, running on a Proxmox VM. Most of what I learned was inspired from Home Assistant's documentation or by exploring the configuration examples provided by [Awesome Home Assistant](https://www.awesome-ha.com/).

## Devices

### Home Assistant
| Device | Link | Notes |
| ---  | :---: | --- |
| SkyConnect Controller | [Link](https://www.home-assistant.io/skyconnect/) | Controller for ZigBee and Matter devices |
| Aeotec Z-Stick 7 Plus Gateway | [Link](https://www.amazon.com/Controller-SmartStart-Raspberry-Compatible-Assistant/dp/B094NW5B68) | Controller for Z-Wave devices |

### Lighting
| Device | Link | Use |
| --- | :---: | --- |
| Enbrighten Z-Wave Switch | [Link](https://www.amazon.com/GE-Enbrighten-SimpleWire-SmartThings-46201/dp/B07RRBT6W5) | Z-Wave in-wall light switch |
| Enbrighten Z-Wave Dimmable Switch | [Link](https://www.amazon.com/GE-Enbrighten-SimpleWire-SmartThings-46203/dp/B07RRD92T8) | Z-Wave in-wall dimmable light switch |
| Enbrighten Z-Wave Motion Sensing Switch | [Link](https://www.amazon.com/GE-Occupancy-Required-SmartThings-26931/dp/B07226MG2T) | Z-Wave in-wall light switch with motion sensing |
| Enbrighten Add-On Switch | [Link](https://www.amazon.com/dp/B07RQ8K25S) | Used in 3-way light switch situations |
| Phillips Hue A19 White Bulbs | [Link](https://www.amazon.com/Philips-Hue-Bluetooth-compatible-Assistant/dp/B07QV9XLTK) | Lightbulbs that can be controlled via Home Assistant or voice. Temperature adjustable and dimmable. |

### Climate
| Device | Link | Use |
| --- | :---: | --- |
| Honeywell T6 Pro (Z-Wave) | [Link](https://a.co/d/hZ3jWm6) | Z-Wave thermostat that can be controlled locally. |

### Switches
| Device | Link | Use |
| --- | :---: | --- |
| Phillips Hue Smart Dimmer Switch | [Link](https://www.amazon.com/Philips-Dimmer-Switch-Installation-Free-Exclusively/dp/B076MGKTGS) | Light switch for controlling the Phillips Hue lights. Can be mounted to the wall or used wirelessly as a remote. |
| TP-Link Kasa HS103P2 | [Link](https://www.amazon.com/TP-LINK-HS103P2-Required-Google-Assistant/dp/B07B8W2KHZ) | Two outlet outdoor smart switch. Can be controlled from the device and through Home Assistant.
| TP-Link Kasa KP400 | [Link](https://www.amazon.com/Kasa-Smart-Outlet-Outdoor-TP-Link/dp/B07M6RS2LC) | Two outlet outdoor smart switch. Can be controlled from the device and through Home Assistant. |
| CloudFree Smart Plug 2 | [Link](https://cloudfree.shop/product/cloudfree-smart-plug-runs-tasmota/) | Wifi connected smart plugs. Flashed with ESPHome and offers power monitoring. |
| Sonoff S31 Smart Plug | [Lin](https://cloudfree.shop/product/sonoff-s31/) | Wifi connect smart plugs. Flashed with ESPHome and offers power monitoring. |

### Echos
| Device | Link | Use |
| --- | :---: | --- |
| Amazon Echo Show (10.1") | [Link](https://www.amazon.com/All-new-Echo-Show-2nd-Gen/dp/B077SXWSRP) | Amazon Echo device that can be used via voice commands or touch. Interacts with Home Assistant components and scripts via voice commands. |
| Amazon Echo (Second Gen) | [Link](https://www.amazon.com/all-new-amazon-echo-speaker-with-wifi-alexa-dark-charcoal/dp/B06XCM9LJ4) | Amazon Echo device that can be used via voice commands. Interacts with Home Assistant components and scripts via voice commands. |
| Amazon Echo Dot (Third Gen) | [Link](https://www.amazon.com/dp/B07FZ8S74R) | Amazon Echo device that can be used viea voice commands. Interacts with Home Assistant components and scripts via voice commands. |
| Amazon Echo Sub | [Link](https://www.amazon.com/gp/product/B0798KPH5X) | Amazon Echo device that connects wirelessly with another Echo device to create a sonud system. Interacts with Home Assistant components and scripts via voice commands. |

### Network
| Device | Link | Use |
| --- | :---: | --- |
| Unifi Dream Machine | [Link](https://store.ui.com/collections/unifi-network-routing-switching/products/unifi-dream-machine) | Unifi Router by Ubiquiti. Contains an access point, a four port switch, and the Unifi manage software. |
| Unifi Switch 24 PoE | [Link](https://store.ui.com/collections/unifi-network-switching/products/usw-24-poe) | Rack-mountable, Power over Ethernet, Layer 2 switch. 16 PoE ports. |
| Unifi Switch 8 60W | [Link](https://store.ui.com/collections/unifi-network-routing-switching/products/unifi-switch-8-60w) | 8 ethernet port switch. 4 PoE ports. |
| Unifi USW Flex Mini | [Link](https://store.ui.com/collections/unifi-network-routing-switching/products/usw-flex-mini) | 4 ethernet port switch. Powered via PoE. |

### Security
| Device | Link | Use |
| --- | :---: | --- |
| Unifi NVR | [Link](https://store.ui.com/us/en/category/all-cameras-nvrs/products/unvr) | Network Video Recorder |
| Unifi G4 Doorbell Pro | [Link](https://store.ui.com/us/en/category/cameras-doorbells/collections/pro-store-doorbells-chimes/products/uvc-g4-doorbell-pro?variant=uvc-g4+doorbell+pro-us) | Smart doorbell tied into Unifi Protect |
| Schlage Connect Smart Deadbolt (Z-Wave) | [Link](https://a.co/d/aT5H8hc) | Z-Wave enabled smart deadbolt. |