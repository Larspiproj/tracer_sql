#!/home/pi/tracer_sql/venv/bin/python3

import serial
from sqlalchemy import Column, DateTime, Integer, Float, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tracer import Tracer, TracerSerial

fake = None
# A sample response, to show what this demo does. Uncomment to use.
#fake = bytearray(b'\xEB\x90\xEB\x90\xEB\x90\x16\xA0\x18\xD2\x04\xD3\x04\x00\
#\x00\x0E\x00\x53\x04\xA5\x05\x01\x00\x00\x1F\x00\x00\x00\x01\x33\x0A\x0A\x00\
#\x9A\x38\x7F')

Base = declarative_base()

class Parameters(Base):
    __tablename__ = 'parameters'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, index=True, default=func.now())
    batt_voltage = Column(Float)
    batt_full_voltage = Column(Float)
    batt_overdischarge_voltage =Column(Float)
    batt_temp = Column(Float)
    pv_voltage = Column(Float)
    charge_current = Column(Float)
    load_on = Column(Boolean)
    load_amps = Column(Float)
    load_overload = Column(Boolean)
    load_short = Column(Boolean)
    batt_overdischarge = Column(Boolean)
    batt_full = Column(Boolean)
    batt_overload = Column(Boolean)
    batt_charging = Column(Boolean)

    def __repr__(self): 
        return '{0} {1}\n    Battery Voltage={2} Battery Full Voltage={3} \
Battery Overdischarge Voltage={4} Battery Temp={5} Solar Panel(PV) Voltage={6} \
Charge Current={7}\n    Load On={8} Load Current={9} Load Overloaded={10} \
Load Short={11} Battery Overloaded={12} Battery Overdischarged={13} \
Battery Full={14}\n    Battery Charging={15}\n'.format(self.id, self.timestamp,
                    self.batt_voltage, self.batt_full_voltage,
                    self.batt_overdischarge_voltage, self.batt_temp,
                    self.pv_voltage, self.charge_current, self.load_on,
                    self.load_amps, self.load_overload, self.load_short,
                    self.batt_overdischarge, self.batt_full,
                    self.batt_overload, self.batt_charging)

engine = create_engine('sqlite:////home/pi/tracer_sql/solar.sqlite')
Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(engine)
session = Session()

class FakePort(object):
    def __init__(self, data):
        self.data = data
    read_idx = 0
    def read(self, count=1):
        result = self.data[self.read_idx:self.read_idx+count]
        self.read_idx += count
        return result
    def write(self, data):
        return len(data)

"""
if not fake:
    port = serial.Serial('/dev/ttyAMA0', 9600, timeout = 1)
else:
    port = FakePort(fake)
"""

def get_data():
    if not fake:
        port = serial.Serial('/dev/ttyAMA0', 9600, timeout = 1)
    else:
        port = FakePort(fake)
    #port = FakePort(fake)
    tracer = Tracer(0x16)
    t_ser = TracerSerial(tracer, port)
    t_ser.send_command(0xA0)
    data = t_ser.receive_result()
    port.close()

        # operating parameters
    p = Parameters(
        batt_voltage =  data.batt_voltage,
        batt_full_voltage = data.batt_full_voltage,
        batt_overdischarge_voltage = data.batt_overdischarge_voltage,
        batt_temp = data.batt_temp,
        pv_voltage = data.pv_voltage,
        charge_current = data.charge_current,
        load_on = data.load_on,
        load_amps = data.load_amps,
        load_overload = data.load_overload,
        load_short = data.load_short,
        batt_overdischarge = data.batt_overdischarge,
        batt_full = data.batt_full,
        batt_overload = data.batt_overload,
        batt_charging = data.batt_charging)
    session.add(p)
    #session.query(Parameters).delete()
    session.commit()
    session.close()


if (__name__) == ('__main__'):
    get_data()
    session.close()
    p = session.query(Parameters).all()
    print("Latest Reading:\n{}".format(p[-1]), end="")
    #parameters = open("/home/pi/tracer_sql/parameters.log", "w")
    with open("/home/pi/tracer_sql/parameters.log", "w") as f:
        for p in p:
            #parameters.write(str(p))
            f.write(str(p))
    """
    for p in p:
        parameters.write('{0} {1}\n    Battery Voltage={2} Battery Full Voltage={3} \
Battery Overdischarge Voltage={4} Battery Temp={5} Solar Panel(PV) Voltage={6} \
Charge Current={7}\n    Load On={8} Load Current={9} Load Overloaded={10} \
Load Short={11} Battery Overloaded={12} Battery Overdischarged={13} \
Battery Full={14}\n    Battery Charging={15}\n'.format(p.id, p.timestamp,
                    p.batt_voltage, p.batt_full_voltage,
                    p.batt_overdischarge_voltage, p.batt_temp, p.pv_voltage,
                    p.charge_current, p.load_on, p.load_amps, p.load_overload,
                    p.load_short, p.batt_overdischarge, p.batt_full,
                    p.batt_overload, p.batt_charging))
    """
    #parameters.close()
