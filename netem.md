## Netem Commands

sudo tc qdisc add dev lo root netem delay 100ms

sudo tc qdisc del dev lo root

sudo tc qdisc add dev lo root netem delay 100ms 10ms (Adds a delay of 100+-10 ms)

sudo tc qdisc add dev lo root netem delay 100ms 10ms 25% (next random element
depending 25 percent on the last one)

## Delay Distribution

sudo tc qdisc add dev lo root netem delay 100ms 20ms distribution normal

## Packet loss

sudo tc qdisc add dev lo root netem loss 0.1%

sudo tc qdisc add dev lo root netem loss 0.1% 25%

## Packet duplication

sudo tc qdisc add dev lo root netem duplicate 1%

## Packet corruption

sudo tc qdisc add dev lo root netem corrupt 0.1%

## Packet re-ordering

sudo tc qdisc add dev lo root netem gap 5 delay 10ms

sudo tc qdisc add dev lo root netem delay 10ms reorder 25% 50% (25% of packets with 50% percent correlation will get sent immediately and others will get 10 ms delay)

## For localhost

sudo tc qdisc add dev lo root handle 1:0 netem delay 100msec

sudo tc qdisc del dev lo root
