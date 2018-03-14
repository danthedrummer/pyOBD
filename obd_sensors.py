 #!/usr/bin/env python
###########################################################################
# obd_sensors.py
#
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)
# Copyright 2009 Secons Ltd. (www.obdtester.com)
#
# This file is part of pyOBD.
#
# pyOBD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pyOBD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyOBD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###########################################################################

def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if( (val&(1<<(bits-1))) != 0 ):
        val = val - (1<<bits)
    return val

def twos_to_int(hex):
    if hex != '':
        twos_comp(hex_to_int(hex), 32);
    return 0

def hex_to_int(str):
    if str != '':
        return int(str, 16)
    return 0


def ab(hex):
    return hex_to_int(hex[0:3]) # == (A*256)+B)

def cd(hex):
    return hex_to_int(hex[4:7]) # == (C*256)+D)

def abcd(hex):
    return hex_to_int(hex)

def a(hex):
    return hex_to_int(hex[0:1])

def b(hex):
    return hex_to_int(hex[2:3])  

def c(hex):
    return hex_to_int(hex[4:5]) 

def d(hex):
    return hex_to_int(hex[6:7])

def e(hex):
    return hex_to_int(hex[8:9])

def twos_ab(hex):
    return twos_to_int(hex[0:3]) # == (A*256)+B)

def twos_cd(hex):
    return twos_to_int(hex[4:7]) # == (C*256)+D)

def twos_abcd(hex):
    return twos_to_int(hex)

def twos_a(hex):
    return twos_to_int(hex[0:1])

def twos_b(hex):
    return twos_to_int(hex[2:3])  

def twos_c(hex):
    return twos_to_int(hex[4:5]) 

def twos_d(hex):
    return twos_to_int(hex[6:7])

def split_code(code):
    return a(code), b(code), c(code), d(code)

def twos_split_code(code):
    return twos_a(code), twos_b(code), twos_c(code), twos_d(code)

def maf(code):
    return ab(code) / 100

def throttle_pos(code):
    return a(code) * 100.0 / 255.0

def intake_m_pres(code): # in kPa
    code = hex_to_int(code)
    return code / 0.14504
    
def rpm(code):
    return ab(code)/4

def speed_short(code):
    return a(code)

def speed(code):
    return ab(code)

def fuel_preasure(code): # in kPa
    return a(code) * 3

def rail_preasure(code): # in kPa
    return ab(code) * 0.079

def rail_preasure_direct_injection(code): # in kPa
    return ab(code) * 10

def percent_scale(code):
    return a(code) * 100.0 / 255.0

def timing_advance(code):
    return (a(code) - 128) / 2.0

def sec_to_min(code):
    return ab(code) / 60

def temp_short(code):
    return a(code) - 40

def temp(code):
    return ab(code) / 10 - 40

def cpass(code):
    #fixme
    return code

def fuel_trim_percent(code):
    return (a(code) - 128.0) * 100.0 / 128.0

def fuel_pressure(code):
    return a(code) * 3

def control_module_voltage(code):
    return ab(code) / 1000.0

def o_sensor_lambda(code):
    na    = ab(code) * 2.0 / 65535.0 
    volts = cd(code) * 8.0 / 65535.0
    return str(na) + ', ' + str(volts)

def o_sensor_lambda_current(code):
    na    = ab(code) / 32768.0 
    amps  = cd(code) / 256.0 - 128.0
    return str(na) + ', ' + str(amps)

def sensor_fuel_trim_volts_percent(code):
    if code != 'FF':
        percent = (b(code) - 128.0) * 100.0 / 128.0
        volts = a(code) / 200.0
        return str(volts) + ', ' + str(percent)
    return 'NA'

def evap_system_vapor_pressure(code):
    return ((twos_a(code) * 256) + twos_b(code)) / 4

def absolute_load_value(code):
    return ab(code) * 100.0 / 255.0

def command_equivalence_ratio(code):
    return ab(code) / 32768

def max_values(code):
    return str(a(code)) + ', ' + str(b(code)) + ', ' + str(c(code)) + ', ' + str(d(code) * 10)

def max_values_air_flow(code):
    return str(a(code) * 10) + ', ' + str(b(code)) + ', ' + str(c(code)) + ', ' + str(d(code))

def absolute_evap_vapor_pres(code):
    return ab(code) / 200.0

def evap_vapor_pres(code):
    return ab(code) - 32767

def secondary_oxygen_sensor_trim(code):
    p1 = (a(code) - 128.0) * 100.0 / 128.0
    p2 = (b(code) - 128.0) * 100.0 / 128.0
    return str(p1) + ', ' + str(p2)

def fuel_injection_timing(code):
    return (ab(code) - 26880.0) / 128.0

def engine_fuel_rate(code):
    return ab(code) * 0.05

def engine_torque_precent(code):
    return a(code) - 125

def engine_percent_torque_data(code):
    return str(a(code) - 125) + ', ' + str(b(code) - 125) + ', ' + str(c(code) - 125) + ', ' + str(d(code) - 125)

def dtc_decrypt(code):
    #first byte is byte after PID and without spaces
    num = a(code[:2]) #A byte
    res = []

    if num & 0x80: # is mil light on
        mil = 1
    else:
        mil = 0
        
    # bit 0-6 are the number of dtc's. 
    num = num & 0x7f
    
    res.append(num)
    res.append(mil)
    
    numB = b(code[2:4]) #B byte
      
    for i in range(0,3):
        res.append(((numB>>i)&0x01)+((numB>>(3+i))&0x02))
    
    numC = c(code[4:6]) #C byte
    numD = d(code[6:8]) #D byte
       
    for i in range(0,7):
        res.append(((numC>>i)&0x01)+(((numD>>i)&0x01)<<1))
    
    res.append(((numD>>7)&0x01)) #EGR SystemC7  bit of different 
    
    return res

def hex_to_bitstring(str):
    bitstring = ""
    for i in str:
        # silly type safety, we don't want to eval random stuff
        if type(i) == type(''): 
            v = eval("0x%s" % i)
            if v & 8 :
                bitstring += '1'
            else:
                bitstring += '0'
            if v & 4:
                bitstring += '1'
            else:
                bitstring += '0'
            if v & 2:
                bitstring += '1'
            else:
                bitstring += '0'
            if v & 1:
                bitstring += '1'
            else:
                bitstring += '0'                
    return bitstring

class Sensor:
    def __init__(self, sensorName, sensorcommand, sensorValueFunction, unit, shortname="unknown"):
        self.name = sensorName
        self.cmd  = sensorcommand
        self.value= sensorValueFunction
        self.unit = unit
        self.shortname = shortname

SENSORS = [
    Sensor("           PIDs supported [01 - 20]", "0100", hex_to_bitstring              ,"",        "pids_a"),
    Sensor("           Status Since DTC Cleared", "0101", dtc_decrypt                   ,"",        "dtc_status"),
    Sensor("           DTC Causing Freeze Frame", "0102", cpass                         ,"",        "dtc_ff"),
    Sensor("                 Fuel System Status", "0103", cpass                         ,"",        "fuel_status"),
    Sensor("              Calculated Load Value", "0104", percent_scale                 ,"%",       "load"),
    Sensor("                Coolant Temperature", "0105", temp_short                    ,"C",       "temp"),
    Sensor("               Short Term Fuel Trim", "0106", fuel_trim_percent             ,"%",       "short_term_fuel_trim_1"),
    Sensor("                Long Term Fuel Trim", "0107", fuel_trim_percent             ,"%",       "long_term_fuel_trim_1"),
    Sensor("               Short Term Fuel Trim", "0108", fuel_trim_percent             ,"%",       "short_term_fuel_trim_2"),
    Sensor("                Long Term Fuel Trim", "0109", fuel_trim_percent             ,"%",       "long_term_fuel_trim_2"),
    Sensor("                 Fuel Rail Pressure", "010A", fuel_pressure                 ,"kPa",     "fuel_pressure"),
    Sensor("           Intake Manifold Pressure", "010B", a                             ,"kPa",     "manifold_pressure"),
    Sensor("                         Engine RPM", "010C", rpm                           ,"rpm",     "rpm"),
    Sensor("                      Vehicle Speed", "010D", speed_short                   ,"km/h",    "speed"),
    Sensor("                     Timing Advance", "010E", timing_advance                ,"degrees", "timing_advance"),
    Sensor("                    Intake Air Temp", "010F", temp_short                    ,"C",       "intake_air_temp"),
    Sensor("                Air Flow Rate (MAF)", "0110", maf                           ,"g/s",     "maf"),
    Sensor("                  Throttle Position", "0111", throttle_pos                  ,"%",       "throttle_pos"),
    Sensor("               Secondary Air Status", "0112", cpass                         ,"",        "secondary_air_status"),
    Sensor("             Location of O2 sensors", "0113", cpass                         ,"",        "o2_sensor_positions"),
    Sensor("                   O2 Sensor: 1 - 1", "0114", sensor_fuel_trim_volts_percent,"v, %",    "o211"),
    Sensor("                   O2 Sensor: 1 - 2", "0115", sensor_fuel_trim_volts_percent,"v, %",    "o212"),
    Sensor("                   O2 Sensor: 1 - 3", "0116", sensor_fuel_trim_volts_percent,"v, %",    "o213"),
    Sensor("                   O2 Sensor: 1 - 4", "0117", sensor_fuel_trim_volts_percent,"v, %",    "o214"),
    Sensor("                   O2 Sensor: 2 - 1", "0118", sensor_fuel_trim_volts_percent,"v, %",    "o221"),
    Sensor("                   O2 Sensor: 2 - 2", "0119", sensor_fuel_trim_volts_percent,"v, %",    "o222"),
    Sensor("                   O2 Sensor: 2 - 3", "011A", sensor_fuel_trim_volts_percent,"v, %",    "o223"),
    Sensor("                   O2 Sensor: 2 - 4", "011B", sensor_fuel_trim_volts_percent,"v, %",    "o224"),
    Sensor("                    OBD Designation", "011C", cpass                         ,"",        "obd_standard"),
    Sensor("             Location of O2 sensors", "011D", cpass                         ,"",        "o2_sensor_position_b"),
    Sensor("                   Aux input status", "011E", cpass                         ,"",        "aux_input"),
    Sensor("            Time Since Engine Start", "011F", sec_to_min                    ,"min",     "engine_time"),
    Sensor("           PIDs supported [21 - 40]", "0120", hex_to_bitstring              ,"",        "pids_b"),
    Sensor("                 Distance w/ MIL on", "0121", speed                         ,"km",      "distance_w_mil"),
    Sensor("                 Fuel Rail Pressure", "0122", rail_preasure                 ,"kPa",     "fuel_rail_pressure_vac"),
    Sensor("              Fuel Rail Pressure DI", "0123", rail_preasure_direct_injection,"kPa",     "fuel_rail_pressure_direct"),
    Sensor("                     O2S1_WR_lambda", "0124", o_sensor_lambda               ,"NA, V",    "o2_s1_wr_voltage"),
    Sensor("                     O2S2_WR_lambda", "0125", o_sensor_lambda               ,"NA, V",   "o2_s2_wr_voltage"),
    Sensor("                     O2S3_WR_lambda", "0126", o_sensor_lambda               ,"NA, V",   "o2_s3_wr_voltage"),
    Sensor("                     O2S4_WR_lambda", "0127", o_sensor_lambda               ,"NA, V",   "o2_s2_wr_voltage"),
    Sensor("                     O2S5_WR_lambda", "0128", o_sensor_lambda               ,"NA, V",   "o2_s5_wr_voltage"),
    Sensor("                     O2S6_WR_lambda", "0129", o_sensor_lambda               ,"NA, V",   "o2_s6_wr_voltage"),
    Sensor("                     O2S7_WR_lambda", "012A", o_sensor_lambda               ,"NA, V",   "o2_s7_wr_voltage"),
    Sensor("                     O2S8_WR_lambda", "012B", o_sensor_lambda               ,"NA, V",   "o2_s8_wr_voltage"),
    Sensor("                      Commanded EGR", "012C", percent_scale                 ,"%",       "commanded_egr"),
    Sensor("                          EGR Error", "012D", fuel_trim_percent             ,"%",       "egr_error"),
    Sensor("               Commanded evap purge", "012E", percent_scale                 ,"%",       "evaporative_purge"),
    Sensor("                   Fuel Level Input", "012F", percent_scale                 ,"%",       "fuel_level"),
    Sensor("           Warm-ups Since Codes CLD", "0130", a                             ,"",        "warmups_since_dtc_clear"),
    Sensor("           Distance Since Codes CLD", "0131", speed                         ,"km",      "distance_since_dtc_clear"),
    Sensor("            Evap. System Vapor Pres", "0132", evap_system_vapor_pressure    ,"Pa",      "evap_vapor_pressure"),
    Sensor("                Barometric pressure", "0133", a                             ,"kPa",     "barometric_pressure"),
    Sensor("                     O2S1_WR_lambda", "0134", o_sensor_lambda_current       ,"NA, mA",  "o2_s1_wr_current"),
    Sensor("                     O2S2_WR_lambda", "0135", o_sensor_lambda_current       ,"NA, mA",  "o2_s2_wr_current"),
    Sensor("                     O2S3_WR_lambda", "0136", o_sensor_lambda_current       ,"NA, mA",  "o2_s3_wr_current"),
    Sensor("                     O2S4_WR_lambda", "0137", o_sensor_lambda_current       ,"NA, mA",  "o2_s4_wr_current"),
    Sensor("                     O2S5_WR_lambda", "0138", o_sensor_lambda_current       ,"NA, mA",  "o2_s5_wr_current"),
    Sensor("                     O2S6_WR_lambda", "0139", o_sensor_lambda_current       ,"NA, mA",  "o2_s6_wr_current"),
    Sensor("                     O2S7_WR_lambda", "013A", o_sensor_lambda_current       ,"NA, mA",  "o2_s7_wr_current"),
    Sensor("                     O2S8_WR_lambda", "013B", o_sensor_lambda_current       ,"NA, mA",  "o2_s8_wr_current"),
    Sensor("                 Catalyst Temp B1S1", "013C", temp                          ,"C",       "catalyst_temp_b1s1"),
    Sensor("                 Catalyst Temp B2S1", "013D", temp                          ,"C",       "catalyst_temp_b1s2"),
    Sensor("                 Catalyst Temp B1S2", "013E", temp                          ,"C",       "catalyst_temp_b2s1"),
    Sensor("                 Catalyst Temp B2S2", "013F", temp                          ,"C",       "catalyst_temp_b2s2"),
    Sensor("           PIDs supported [41 - 60]", "0140", hex_to_bitstring              ,"",        "pids_c"),
    Sensor("           Monitor status drive cyc", "0141", cpass                         ,"",        "status_drive_cycle"),
    Sensor("             Control Module Voltage", "0142", control_module_voltage        ,"V",       "control_module_voltage"),
    Sensor("                Absolute Load Value", "0143", absolute_load_value           ,"%",       "absolute_load"),
    Sensor("           Command Equivalence Rati", "0144", command_equivalence_ratio     ,"",        "commanded_equiv_ratio"),
    Sensor("              Relative Throttle Pos", "0145", percent_scale                 ,"%",       "relative_throttle_pos"),
    Sensor("            Ambient Air Temperature", "0146", temp_short                    ,"C",       "ambient_air_temp"),
    Sensor("            Absolute throttle pos B", "0147", percent_scale                 ,"%",       "throttle_pos_b"),
    Sensor("            Absolute throttle pos C", "0148", percent_scale                 ,"%",       "throttle_pos_c"),
    Sensor("            Absolute throttle pos D", "0149", percent_scale                 ,"%",       "throttle_pos_d"),
    Sensor("            Absolute throttle pos E", "014A", percent_scale                 ,"%",       "throttle_pos_e"),
    Sensor("            Absolute throttle pos F", "014B", percent_scale                 ,"%",       "throttle_pos_f"),
    Sensor("           CommandedThrottleActutor", "014C", percent_scale                 ,"%",       "throttle_actuator"),
    Sensor("               Time run with MIL on", "014D", ab                            ,"min",     "run_time_mil"),
    Sensor("             Time since trb cds cld", "014E", ab                            ,"min",     "time_since_dtc_cleared"),
    Sensor("           Max Val eqRat, O2, InPre", "014F", max_values                    ,"na, V, mA, kPa", "max_values"),
    Sensor("             Max Vals mass air flow", "0150", max_values_air_flow           ,"g/s, g/s, g/s, g/s", "max_maf"),
    Sensor("                          Fuel Type", "0151", cpass                         ,"",        "fuel_type"),
    Sensor("                       Ethanol Fuel", "0152", percent_scale                 ,"%",       "ethanol_percent"),
    Sensor("           Absolute Evap Vapor Pres", "0153", absolute_evap_vapor_pres      ,"kPa",     "evap_vapor_pressure_abs"),
    Sensor("                    Evap vapor Pres", "0154", absolute_evap_vapor_pres      ,"Pa",      "evap_vapor_pressure_alt"),
    Sensor("Short term secondary O2 trim b(1&3)", "0155", secondary_oxygen_sensor_trim  ,"%, %",    "short_02_trim_b1"),
    Sensor(" Long term secondary O2 trim b(1&3)", "0156", secondary_oxygen_sensor_trim  ,"%, %",    "long_02_trim_b1"),
    Sensor("Short term secondary O2 trim b(2&4)", "0157", secondary_oxygen_sensor_trim  ,"%, %",    "short_02_trim_b2"),
    Sensor(" Long term secondary O2 trim b(2&4)", "0158", secondary_oxygen_sensor_trim  ,"%, %",    "long_02_trim_b2"),
    Sensor("      Fuel rail pressure (absolute)", "0159", rail_preasure_direct_injection,"kPa",     "fuel_rail_pressure_abs"),
    Sensor("Relative accelerator pedal position", "015A", percent_scale                 ,"%",       "relative_accel_pos"),
    Sensor(" Hybrid battery pack remaining life", "015B", percent_scale                 ,"%",       "hybrid_battery_remaining"),
    Sensor("             Engine oil temperature", "015C", temp_short                    ,"C",       "oil_temp"),
    Sensor("              Fuel injection timing", "015D", fuel_injection_timing         ,"degrees", "fuel_inject_timing"),
    Sensor("                   Engine fuel rate", "015E", engine_fuel_rate              ,"L/h",     "fuel_rate"),
    Sensor("          Emission vehicle designed", "015F", cpass                         ,"",        "emission_req"),
    Sensor("           PIDs supported [61 - 80]", "0160", hex_to_bitstring              ,"",        "pids_c"),    
    Sensor("      Driver's demand engine torque", "0161", engine_torque_precent         ,"%"),    
    Sensor("               Actual engine torque", "0162", engine_torque_precent         ,"%"),    
    Sensor("            Engine reference torque", "0163", ab                            ,"Nm"),    
    Sensor("         Engine percent torque data", "0164", engine_percent_torque_data    ,"%idle, %p1, %p2, %p3, %p4"),    
    Sensor(" Auxiliary input / output supported", "0165", cpass                          ,""),    
    Sensor("               Mass air flow sensor", "0166", cpass                          ,""),    
    Sensor("         Engine coolant temperature", "0167", cpass                          ,""),    
    Sensor("      Intake air temperature sensor", "0168", cpass                          ,""),    
    Sensor("        Commanded EGR and EGR Error", "0169", cpass                          ,""),    
    Sensor("Commanded and relative air flow pos", "016A", cpass                          ,""),    
    Sensor("     Exhaust gas recirculation temp", "016B", cpass                          ,""),    
    Sensor("Commanded throttle and relative pos", "016C", cpass                          ,""),    
    Sensor("       Fuel pressure control system", "016D", cpass                          ,""),    
    Sensor("  Injection pressure control system", "016E", cpass                          ,""),    
    Sensor(" Turbocharger compressor inlet pres", "016F", cpass                          ,""),    
    Sensor("             Boost pressure control", "0170", cpass                          ,""),    
    Sensor("      Variable Geometry turbo (VGT)", "0171", cpass                          ,""),    
    Sensor("                  Wastegate control", "0172", cpass                          ,""),    
    Sensor("                   Exhaust pressure", "0173", cpass                          ,""),    
    Sensor("                   Turbocharger RPM", "0174", cpass                          ,""),    
    Sensor("           Turbocharger temperature", "0175", cpass                          ,""),    
    Sensor("           Turbocharger temperature", "0176", cpass                          ,""),    
    Sensor("      Charge air cooler temp (CACT)", "0177", cpass                          ,""),    
    Sensor("      Exhaust Gas temp (EGT) Bank 1", "0178", cpass                          ,""),    
    Sensor("      Exhaust Gas temp (EGT) Bank 2", "0179", cpass                          ,""),    
    Sensor("    Diesel particulate filter (DPF)", "017A", cpass                          ,""),    
    Sensor("    Diesel particulate filter (DPF)", "017B", cpass                          ,""),    
    Sensor("    Diesel particulate filter (DPF)", "017C", cpass                          ,""),    
    Sensor("        NOx NTE control area status", "017D", cpass                          ,""),    
    Sensor("         PM NTE control area status", "017E", cpass                          ,""),    
    Sensor("                    Engine run time", "017F", cpass                          ,""),    
    Sensor("           PIDs supported [81 - A0]", "0180", hex_to_bitstring               ,"",       "pids_d"),    
    Sensor("   Engine run time for Aux Emis Ctl", "0181", cpass                          ,""),    
    Sensor("   Engine run time for Aux Emis Ctl", "0182", cpass                          ,""),    
    Sensor("                         NOx sensor", "0183", cpass                          ,""),    
    Sensor("       Manifold surface temperature", "0184", cpass                          ,""),    
    Sensor("                 NOx reagent system", "0185", cpass                          ,""),    
    Sensor("  Intake manifold absolute pressure", "0186", cpass                          ,""),    
    Sensor("                     Unknown (0187)", "0187", cpass                          ,""),    
    Sensor("                     Unknown (0188)", "0188", cpass                          ,""),    
    Sensor("                     Unknown (0189)", "0189", cpass                          ,""),    
    Sensor("                     Unknown (018A)", "018A", cpass                          ,""),    
    Sensor("                     Unknown (018B)", "018B", cpass                          ,""),    
    Sensor("                     Unknown (018C)", "018C", cpass                          ,""),    
    Sensor("                     Unknown (018D)", "018D", cpass                          ,""),    
    Sensor("                     Unknown (018E)", "018E", cpass                          ,""),    
    Sensor("                     Unknown (018F)", "018F", cpass                          ,""),    
    Sensor("                     Unknown (0190)", "0190", cpass                          ,""),    
    Sensor("                     Unknown (0191)", "0191", cpass                          ,""),    
    Sensor("                     Unknown (0192)", "0192", cpass                          ,""),    
    Sensor("                     Unknown (0193)", "0193", cpass                          ,""),    
    Sensor("                     Unknown (0194)", "0194", cpass                          ,""),    
    Sensor("                     Unknown (0195)", "0195", cpass                          ,""),    
    Sensor("                     Unknown (0196)", "0196", cpass                          ,""),    
    Sensor("                     Unknown (0197)", "0197", cpass                          ,""),    
    Sensor("                     Unknown (0198)", "0198", cpass                          ,""),    
    Sensor("                     Unknown (0199)", "0199", cpass                          ,""),    
    Sensor("                     Unknown (019A)", "019A", cpass                          ,""),    
    Sensor("                     Unknown (019B)", "019B", cpass                          ,""),    
    Sensor("                     Unknown (019C)", "019C", cpass                          ,""),    
    Sensor("                     Unknown (019D)", "019D", cpass                          ,""),    
    Sensor("                     Unknown (019E)", "019E", cpass                          ,""),    
    Sensor("                     Unknown (019F)", "019F", cpass                          ,""),    
    Sensor("           PIDs supported [A1 - C0]", "01A0", hex_to_bitstring               ,"",       "pids_e"),    
    Sensor("                     Unknown (01A1)", "01A1", cpass                          ,""),    
    Sensor("                     Unknown (01A2)", "01A2", cpass                          ,""),    
    Sensor("                     Unknown (01A3)", "01A3", cpass                          ,""),    
    Sensor("                     Unknown (01A4)", "01A4", cpass                          ,""),    
    Sensor("                     Unknown (01A5)", "01A5", cpass                          ,""),    
    Sensor("                     Unknown (01A6)", "01A6", cpass                          ,""),    
    Sensor("                     Unknown (01A7)", "01A7", cpass                          ,""),    
    Sensor("                     Unknown (01A8)", "01A8", cpass                          ,""),    
    Sensor("                     Unknown (01A9)", "01A9", cpass                          ,""),    
    Sensor("                     Unknown (01AA)", "01AA", cpass                          ,""),    
    Sensor("                     Unknown (01AB)", "01AB", cpass                          ,""),    
    Sensor("                     Unknown (01AC)", "01AC", cpass                          ,""),    
    Sensor("                     Unknown (01AD)", "01AD", cpass                          ,""),    
    Sensor("                     Unknown (01AE)", "01AE", cpass                          ,""),    
    Sensor("                     Unknown (01AF)", "01AF", cpass                          ,""),    
    Sensor("                     Unknown (01B0)", "01B0", cpass                          ,""),    
    Sensor("                     Unknown (01B1)", "01B1", cpass                          ,""),    
    Sensor("                     Unknown (01B2)", "01B2", cpass                          ,""),    
    Sensor("                     Unknown (01B3)", "01B3", cpass                          ,""),    
    Sensor("                     Unknown (01B4)", "01B4", cpass                          ,""),    
    Sensor("                     Unknown (01B5)", "01B5", cpass                          ,""),    
    Sensor("                     Unknown (01B6)", "01B6", cpass                          ,""),    
    Sensor("                     Unknown (01B7)", "01B7", cpass                          ,""),    
    Sensor("                     Unknown (01B8)", "01B8", cpass                          ,""),    
    Sensor("                     Unknown (01B9)", "01B9", cpass                          ,""),    
    Sensor("                     Unknown (01BA)", "01BA", cpass                          ,""),    
    Sensor("                     Unknown (01BB)", "01BB", cpass                          ,""),    
    Sensor("                     Unknown (01BC)", "01BC", cpass                          ,""),    
    Sensor("                     Unknown (01BD)", "01BD", cpass                          ,""),    
    Sensor("                     Unknown (01BE)", "01BE", cpass                          ,""),    
    Sensor("                     Unknown (01BF)", "01BF", cpass                          ,""),    
    Sensor("           PIDs supported [C1 - E0]", "01C0", hex_to_bitstring               ,"",       "pids_f"),    
    Sensor("                     Unknown (01C1)", "01C1", cpass                          ,""),    
    Sensor("                     Unknown (01C2)", "01C2", cpass                          ,""),    
    Sensor("                     Unknown (01C3)", "01C3", cpass                          ,""),    
    Sensor("                     Unknown (01C4)", "01C4", cpass                          ,""),    
    Sensor("                     Unknown (01C5)", "01C5", cpass                          ,""),    
    Sensor("                     Unknown (01C6)", "01C6", cpass                          ,""),    
    Sensor("                     Unknown (01C7)", "01C7", cpass                          ,""),    
    Sensor("                     Unknown (01C8)", "01C8", cpass                          ,""),    
    Sensor("                     Unknown (01C9)", "01C9", cpass                          ,""),    
    Sensor("                     Unknown (01CA)", "01CA", cpass                          ,""),    
    Sensor("                     Unknown (01CB)", "01CB", cpass                          ,""),    
    Sensor("                     Unknown (01CC)", "01CC", cpass                          ,""),    
    Sensor("                     Unknown (01CD)", "01CD", cpass                          ,""),    
    Sensor("                     Unknown (01CE)", "01CE", cpass                          ,""),    
    Sensor("                     Unknown (01CF)", "01CF", cpass                          ,""),    
    Sensor("                     Unknown (01D0)", "01D0", cpass                          ,""),    
    Sensor("                     Unknown (01D1)", "01D1", cpass                          ,""),    
    Sensor("                     Unknown (01D2)", "01D2", cpass                          ,""),    
    Sensor("                     Unknown (01D3)", "01D3", cpass                          ,""),    
    Sensor("                     Unknown (01D4)", "01D4", cpass                          ,""),    
    Sensor("                     Unknown (01D5)", "01D5", cpass                          ,""),    
    Sensor("                     Unknown (01D6)", "01D6", cpass                          ,""),    
    Sensor("                     Unknown (01D7)", "01D7", cpass                          ,""),    
    Sensor("                     Unknown (01D8)", "01D8", cpass                          ,""),    
    Sensor("                     Unknown (01D9)", "01D9", cpass                          ,""),    
    Sensor("                     Unknown (01DA)", "01DA", cpass                          ,""),    
    Sensor("                     Unknown (01DB)", "01DB", cpass                          ,""),    
    Sensor("                     Unknown (01DC)", "01DC", cpass                          ,""),    
    Sensor("                     Unknown (01DD)", "01DD", cpass                          ,""),    
    Sensor("                     Unknown (01DE)", "01DE", cpass                          ,""),    
    Sensor("                     Unknown (01DF)", "01DF", cpass                          ,""),    
    Sensor("           PIDs supported [E1 - FF]", "01C0", hex_to_bitstring               ,"",       "pids_g"),    
    Sensor("                     Unknown (01E1)", "01E1", cpass                          ,""),    
    Sensor("                     Unknown (01E2)", "01E2", cpass                          ,""),    
    Sensor("                     Unknown (01E3)", "01E3", cpass                          ,""),    
    Sensor("                     Unknown (01E4)", "01E4", cpass                          ,""),    
    Sensor("                     Unknown (01E5)", "01E5", cpass                          ,""),    
    Sensor("                     Unknown (01E6)", "01E6", cpass                          ,""),    
    Sensor("                     Unknown (01E7)", "01E7", cpass                          ,""),    
    Sensor("                     Unknown (01E8)", "01E8", cpass                          ,""),    
    Sensor("                     Unknown (01E9)", "01E9", cpass                          ,""),    
    Sensor("                     Unknown (01EA)", "01EA", cpass                          ,""),    
    Sensor("                     Unknown (01EB)", "01EB", cpass                          ,""),    
    Sensor("                     Unknown (01EC)", "01EC", cpass                          ,""),    
    Sensor("                     Unknown (01ED)", "01ED", cpass                          ,""),    
    Sensor("                     Unknown (01EE)", "01EE", cpass                          ,""),    
    Sensor("                     Unknown (01EF)", "01EF", cpass                          ,""),    
    Sensor("                     Unknown (01F0)", "01F0", cpass                          ,""),    
    Sensor("                     Unknown (01F1)", "01F1", cpass                          ,""),    
    Sensor("                     Unknown (01F2)", "01F2", cpass                          ,""),    
    Sensor("                     Unknown (01F3)", "01F3", cpass                          ,""),    
    Sensor("                     Unknown (01F4)", "01F4", cpass                          ,""),    
    Sensor("                     Unknown (01F5)", "01F5", cpass                          ,""),    
    Sensor("                     Unknown (01F6)", "01F6", cpass                          ,""),    
    Sensor("                     Unknown (01F7)", "01F7", cpass                          ,""),    
    Sensor("                     Unknown (01F8)", "01F8", cpass                          ,""),    
    Sensor("                     Unknown (01F9)", "01F9", cpass                          ,""),    
    Sensor("                     Unknown (01FA)", "01FA", cpass                          ,""),    
    Sensor("                     Unknown (01FB)", "01FB", cpass                          ,""),    
    Sensor("                     Unknown (01FC)", "01FC", cpass                          ,""),    
    Sensor("                     Unknown (01FD)", "01FD", cpass                          ,""),    
    Sensor("                     Unknown (01FE)", "01FE", cpass                          ,""),    
    Sensor("                     Unknown (01FF)", "01FF", cpass                          ,""),    

    ]
     

#___________________________________________________________

def test():
    for i in SENSORS:
        print i.name, i.value("F")

if __name__ == "__main__":
    test()
