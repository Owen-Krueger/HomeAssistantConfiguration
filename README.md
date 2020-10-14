<div align="center">
<h1>Owen's Home Assistant Configuration</h1>
<a href="https://github.com/Owen-Krueger/HomeAssistantConfiguration/commits/master"><img src="https://img.shields.io/github/last-commit/Owen-Krueger/HomeAssistantConfiguration.svg"/></a>
</div>

This is my personal [Home Assistant](https://www.home-assistant.io/) configuration, running on a [Raspberry Pi 4 (4GB)](https://www.digikey.com/product-detail/en/raspberry-pi/RASPBERRY-PI-4B-4GB/1690-RASPBERRYPI4B-4GB-ND/10258781). Most of what I learned was inspired from Home Assistant's documentation or by exploring the configuration examples provided by [Awesome Home Assistant](https://www.awesome-ha.com/).

## Devices

### Home Assistant
| Device | Link | Use |
| --- | --- | --- |
| Raspberry Pi 4 (4GB) | [Link](https://www.digikey.com/product-detail/en/raspberry-pi/RASPBERRY-PI-4B-4GB/1690-RASPBERRYPI4B-4GB-ND/10258781) | Home Assistant |
| Samsung MicroSDKC Card (64 GB) | [Link](https://www.amazon.com/gp/product/B06XX29S9Q/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1) | Flashed with the Home Assistant image |
| USB C PoE Splitter | [Link](https://www.amazon.com/gp/product/B07TJ3ZNJ4/ref=ppx_yo_dt_b_asin_title_o09_s01?ie=UTF8&psc=1) | Power Raspberry Pi from PoE switch instead of standard charger |

### Lighting
| Device | Link | Use |
| --- | --- | --- |
| Phillips Hue Hub | [Link](https://www.amazon.com/Philips-Hue-Stand-Alone-Bridge/dp/B016H0QZ7I/ref=sr_1_1?dchild=1&keywords=hue+hub&qid=1592357638&sr=8-1) | For interacting with Phillips Hue bulbs and switches |
| Phillips Hue A19 White Bulbs x4 | [Link](https://www.amazon.com/Philips-Hue-Bluetooth-compatible-Assistant/dp/B07QV9XLTK/ref=sxin_7?ascsubtag=amzn1.osa.a8a468f6-73d4-49f2-97f5-6710e012ad6e.ATVPDKIKX0DER.en_US&creativeASIN=B07R2MQ2PY&cv_ct_cx=hue%2Bbulb&cv_ct_id=amzn1.osa.a8a468f6-73d4-49f2-97f5-6710e012ad6e.ATVPDKIKX0DER.en_US&cv_ct_pg=search&cv_ct_wn=osp-single-source&dchild=1&keywords=hue%2Bbulb&linkCode=oas&pd_rd_i=B07R2MQ2PY&pd_rd_r=1f8e07d5-b067-4ca5-8b38-4592a52e7664&pd_rd_w=sPn1q&pd_rd_wg=IUkzj&pf_rd_p=cfb8425e-590e-436e-8f8b-e7ed672784e6&pf_rd_r=G1PPVJY4P6885M9ERC6B&qid=1592357723&sr=1-1-72d6bf18-a4db-4490-a794-9cd9552ac58d&tag=bgr0a0-20&th=1) | Lightbulbs that can be controlled via Home Assistant or voice |

### Switches
| Device | Link | Use |
| --- | --- | --- |
| Phillips Hue Smart Dimmer Switch | [Link](https://www.amazon.com/Philips-Dimmer-Switch-Installation-Free-Exclusively/dp/B076MGKTGS/ref=sr_1_4?dchild=1&keywords=hue+switch&qid=1592357808&s=hi&sr=1-4) | For controlling the Phillips Hue lights |

### Echos
| Device | Link | Use |
| --- | --- | --- |
| Amazon Echo Show (10.1") | [Link](https://www.amazon.com/All-new-Echo-Show-2nd-Gen/dp/B077SXWSRP/ref=sr_1_3?dchild=1&keywords=echo+show&qid=1592357887&sr=8-3) | Interacts with Home Assistant components and scripts via voice commands |
| Amazon Echo (Second Gen) | [Link](https://www.amazon.com/all-new-amazon-echo-speaker-with-wifi-alexa-dark-charcoal/dp/B06XCM9LJ4/ref=sr_1_3?dchild=1&keywords=2nd+gen+echo&qid=1592357936&sr=8-3) | Interacts with Home Assistant components and scripts via voice commands |
| Amazon Echo Dot (Third Gen) | [Link](https://www.amazon.com/dp/B07FZ8S74R?ref=MarsFS_AUCC_ct) | Interacts with Home Assistant components and scripts via voice commands |
| Amazon Echo Sub | [Link](https://www.amazon.com/gp/product/B0798KPH5X/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) | Interacts with Home Assistant components and scripts via voice commands |

### Network
| Device | Link | Use |
| --- | --- | --- |
| Unifi Dream Machine | [Link](https://store.ui.com/collections/unifi-network-routing-switching/products/unifi-dream-machine) | Unifi Router |
| Unifi Switch 8 60W | [Link](https://store.ui.com/collections/unifi-network-routing-switching/products/unifi-switch-8-60w) | 8 ethernet ports (4 POE) |
| Unifi USW Flex Mini x2 | [Link](https://store.ui.com/collections/unifi-network-routing-switching/products/usw-flex-mini) | 4 ethernet ports |