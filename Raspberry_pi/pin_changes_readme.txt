connect the pins accordingly
relayPin0 (GPIO17) -> Pin 11
relayPin1 (GPIO27) -> Pin 13
relayPin2 (GPIO22) -> Pin 15
relayPin3 (GPIO23) -> Pin 16
door (GPIO5) -> Pin 29
inlet2 (GPIO6) -> Pin 31
inlet1 (GPIO13) -> Pin 33
drain (GPIO19) -> Pin 35


#run compined2.py




#install the required librarys using the following command
pip install RPi.GPIO spidev hx711

or
pip3 install RPi.GPIO spidev hx711





# mcp3008 adc converter


https://www.dnatechindia.com/mcp-3008-breakout-board.html

https://www.indiamart.com/proddetail/mcp3008-breakout-board-with-mcp3008-ic-23333277291.html

https://www.flipkart.com/sciencelab-technosolutions-set-03-mcp3008-breakout-board-educational-electronic-hobby-kit/p/itm00ae566e8b898





#for adc converter install new libraries

sudo apt-get update
sudo apt-get install python3-smbus
sudo apt-get install i2c-tools
