# Adaptive Data Rate

Adaptive Data Rate (ADR) is a mechanism for optimizing data rates, airtime and energy consumption in the network.
The ADR mechanism controls the following transmission parameters of an end device.
* Spreading factor
* Bandwidth
* Transmission power

ADR can optimize device power consumption while ensuring that messages are still received at gateways. When ADR is in use, the network server will indicate to the end device that it should reduce transmission power or increase data rate. End devices which are close to gateways should use a lower spreading factor and higher data rate, while devices further away should use a high spreading factor because they need a higher link budget.
ADR should be enabled whenever an end device has sufficiently stable RF conditions. This means that it can generally be enabled for static devices. If the static end device can determine that RF conditions are unstable (for example, when a car is parked on top of a parking sensor), ADR should (temporarily) be disabled.
Mobile end devices should be able to detect when they are stationary for a longer times, and enable ADR during those times. End devices decide if ADR should be used or not, not the application or the network.
## ADR in The Things Stack

##### Info:

 Check [The Things Stack documentation](https://www.thethingsindustries.com/docs/reference/adr/#how-adr-works) for more specifics on how ADR works on the The Things Stack.

To determine the optimal data rate, the network needs some measurements (uplink messages). Currently The Things Stack takes the 20 most recent uplinks, starting at the moment the ADR bit is set. These measurements contains the frame counter, signal-to-noise ratio (SNR) and number of gateways that received each uplink. When a device unsets the ADR bit (because it knows it is moving or it knows RF conditions are unstable), previous measurements are discarded. As soon as the ADR bit is set again, the network starts measuring again.
For each of these measurements, we take the SNR of the best gateway, and we calculate the so-called “margin”, which is the measured SNR minus the required SNR to demodulate a message given the data rate. This margin is used to determine how much we can increase the data rate or lower the transmit power. For example, when the network receives a message with data rate SF12BW125 and SNR 5.0 , that message has a margin of 25 dB. This is a waste of valuable airtime and energy. If we would increase the data rate to SF7BW125 we would still have a margin of 12.5 dB, but that would be many times more airtime- and energy efficient. We could even lower the transmit power to save even more energy and cause less interference.
There are a several moments when an ADR request is scheduled or sent:

ADR requests are no longer scheduled or sent if the device refused several ADR requests. This could either mean a bad implementation of the device, or a version mismatch between the device and the server.
The algorithm used in The Things Network is based on Semtech’s recommended algorithm for rate adaptation. The following diagram outlines the ADR flow as implemented in The Things Stack:

1. The Adaptive Data Rate is suitable for
	* Static end devices
	* Mobile end devices
2. The end devices located close to a gateway should use a
	* Lower data rate
	* Higher data rate
3. The end devices located several kilometers from a gateway should use a
	* Lower data rate
	* Higher data rate
4. A higher data rate means,
	* A lower spreading factor
	* A higher spreading factor
5. Which of the following end devices should not implement ADR?
	* Environmental sensor
	* Water leakage detector
	* Pet tracker
	* Gas detector