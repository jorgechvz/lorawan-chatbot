# Spreading Factors

LoRa is based on Chirp Spread Spectrum (CSS) technology, where chirps (also known as symbols) are the carrier of data.
The spreading factor controls the chirp rate, and thus controls the speed of data transmission. Lower spreading factors mean faster chirps and therefore a higher data transmission rate . For every increase in spreading factor, the chirp sweep rate is halved, and so the data transmission rate is halved.
For a visual explanation, see this video on LoRa chirps.
Lower spreading factors reduce the range of LoRa transmissions, because they reduce the processing gain and increase the bit rate. Changing spreading factor allows the network to increase or decrease data rate for each end device at the cost of range.
The network also uses spreading factors to control congestion. Spreading factors are orthogonal, so signals modulated with different spreading factors and transmitted on the same frequency channel at the same time do not interfere with each other.
### Influence of Spreading Factors

LoRa modulation has a total of 6 spreading factors from SF7 to SF12. Spreading factors influence data rate, time-on-air, battery life, and receiver sensitivity, as described here.
#### Data rate

Compared to a higher spreading factor, a lower spreading factor provides a higher bit rate for a fixed bandwidth and coding rate. For example, SF7 provides a higher bit rate than SF12.
Doubling the bandwidth also doubles the bit rate for a fixed spreading factor and coding rate.
The following table presents bit rates calculated with the SF7 and Coding Rate (CR) = 1 for bandwidths, 125, 250, and 500 kHz.

|  |  |  |
| --- | --- | --- |
| **Spreading Factor** | **Bandwidth** | **Bit rate (kbits/s)** |
| 7
  | 125
  | 5.5
  |
| 7
  | 250
  | 10.9
  |
| 7
  | 500
  | 21.9
  |

#### Distance

Larger spreading factors mean larger processing gain, and so a signal modulated with a larger spreading factor can be received with less errors compared to a signal with a lower spreading factor, and therefore travel a longer distance. For example, a signal modulated with the SF12 can travel a longer distance than a signal modulated with the SF7.
#### Time-On-Air

Compared to a lower spreading factor, sending a fixed amount of data (payload) with a higher Spreading Factor and a fixed bandwidth needs longer time-on-air.
The Things Network’s LoRaWAN airtime calculator can be used to calculate the time-on-air using input bytes (payload size), bandwidth, and spreading factor. TTN’s LoRaWAN airtime calculator can be accessed here .
#### Receiver Sensitivity

Higher spreading factors provide higher receiver sensitivity. Usually, LoRa uses higher spreading factors when the signal is weak.
The following table shows how spreading factors impact the receiver sensitivity.

|  |  |
| --- | --- |
| **Spreading factor** | **Receiver sensitivity for bandwidth fixed at 125 kHz** |
| SF7
  | -123 dBm
  |
| SF8
  | -126 dBm
  |
| SF9
  | -129 dBm
  |
| SF10
  | -132 dBm
  |
| SF11
  | -134.5 dBm
  |
| SF12
  | -137 dBm
  |

#### Battery Life

The battery life of an end device is highly dependent on the spreading factor used. Higher spreading factors result in longer active times for the radio transceivers and shorter battery life.

* SF9
* SF10
* SF11
* SF12

2. Which spreading factor provides the highest bit rate?

* SF7
* SF8
* SF9
* SF10

3. Which spreading factor provides the longest battery life for an end device?

* SF7
* SF8
* SF9
* SF10

4. For the same amount of data and bandwidth, which spreading factor results in the longest time-on-air?

* SF7
* SF8
* SF9
* SF10