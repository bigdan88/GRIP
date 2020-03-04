import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
import random


def pub_value(component, subcomponent, value, topic):
    #print "%s/%s: %s" % (component, subcomponent, value)
    publish.single(topic + "/" + subcomponent, value, hostname="localhost")

def random_change(value):
    rander = random.uniform(-1,1)
    return rander + value

def parse_topic(topic):
    i = topic.rfind("/")
    result = topic[i+1:-1]
    return(result)

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):

    if("POST" in msg.payload):
        # print("GOT A POST MESSAGE")
        # global_value = 999999399
        # print(topic)
        # print(msg.topic)
        #
        # if(parse_topic(msg.topic) == subcomponent):
        if(writeable == True):
            value = msg.payload.split()[1]
            print("Post success")
        else:
            publish.single(msg.topic, "Ah ah ah, you didn't say the magic word", hostname="localhost")
            print("Ah ah ah, you didn't say the magic word")


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def does_this_even_work(newtopic, newmsg):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)

def run_payload(topic, component, subcomponent, value, sample_rate, writeable):

    mqttc = mqtt.Client(client_id = "", clean_session = True, userdata = None, transport = "tcp")
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe

    # Uncomment to enable debug messages
    # mqttc.on_log = on_log
    mqttc.connect("localhost", 1883, 60)
    mqttc.reconnect_delay_set(min_delay=1, max_delay=120)
    hash_topic = topic + '/#'
    mqttc.subscribe(hash_topic, 0)


    mqttc.loop_start()

    print "Starting " + component + "/" + subcomponent


    while 1:
    #for i in range(0, 10):
        time.sleep(sample_rate)
        value = random_change(value)
        pub_value(component, subcomponent, value, topic)

    print "Exiting " + component + "/" + subcomponent
