from wit import Wit
import controller.led_controller as led_controller
import controller.ir_controller as ir_controller
import os
import config

client = Wit(os.environ["API_WIT"])

def test(message):
    resp = client.message(message)
    print(str(resp))
    #Check for possibilities
    #try:
    body = resp['entities'].get('message_body', None)
    sub = resp['entities'].get('message_subject', None)
    ordinal = resp['entities'].get('ordinal', None)
    number = resp['entities'].get('number', None)
    val = resp['entities']['on_off'][0]['value']
    text = resp["_text"]
    if('II' in text):
        resp['entities']['ordinal'].append({'type': 'value', 'value': 2, 'confidence': 1})
    if(sub and "AC" in sub[0]['value']):
        print("Setting AC")
        if(val=='on'):
            ir_controller.turnOn()
        else:
            ir_controller.turnOff()
        config.wittyIR = True
    elif(ordinal or number):
        print("Setting LEDs")
        if(ordinal):
            for led_ in range(len(ordinal)):
                if(number and led_<(len(number))):
                    led_controller.turnLED((ordinal[led_]['value'], number[led_]['value']))
                else:
                    if(val=='on'):
                        led_controller.turnLED((ordinal[led_]['value'], 100))
                    else:
                        led_controller.turnLED((ordinal[led_]['value'], 0))
        else:
            #Turn all to a particular percent
            for i in range(1,4):
                led_controller.turnLED((i, number[0]['value']))
    elif(val):
        if(val=='on'):
            print("Turned all ON")
            led_controller.turnAllOn()
        else:
            print("Turned all OFF")
            led_controller.turnAllOff()
    else:
        print("Cannot decide :/ I still need to learn!")
    #except Exception as e:
    #    print(e)
