import PiGPIO

function read()
    return PiGPIO.read(p, btn_pin)
end

btn_pin = 18
p= PiGPIO.Pi()

PiGPIO.set_mode(p, btn_pin, PiGPIO.INPUT)

println(PiGPIO.read(p, btn_pin))
#read()

while true
    #read()
    println(PiGPIO.read(p, btn_pin))
end
