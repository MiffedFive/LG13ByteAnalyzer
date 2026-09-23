from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame

# Correspondence table for pipe temperature bytes in c (Bytes 3–5 in More settings)
PIPE_TEMP_TABLE = {
    0x0A: 108, 0x0B: 104, 0x0C: 101, 0x0D: 100, 0x0E: 98,  0x0F: 95,
    0x10: 93,  0x11: 91,  0x12: 89,  0x13: 87,  0x14: 85,  0x15: 84,  0x16: 82,  0x17: 81,  0x18: 79,  0x19: 78,  0x1A: 76,  0x1B: 75,  0x1C: 74,  0x1D: 73,  0x1E: 72,  0x1F: 71,
    0x20: 70,  0x21: 68,  0x22: 68,  0x23: 67,  0x24: 66,  0x25: 65,  0x26: 64,  0x27: 63,  0x28: 62,  0x29: 61,  0x2A: 60,  0x2B: 60,  0x2C: 59,  0x2D: 58,  0x2E: 57,  0x2F: 57,
    0x30: 56,  0x31: 55,  0x32: 55,  0x33: 54,  0x34: 53,  0x35: 53,  0x36: 52,  0x37: 52,  0x38: 51,  0x39: 50,  0x3A: 50,  0x3B: 49,  0x3C: 49,  0x3D: 48,  0x3E: 47,  0x3F: 47,
    0x40: 46,  0x41: 46,  0x42: 45,  0x43: 45,  0x44: 44,  0x45: 44,  0x46: 43,  0x47: 43,  0x48: 42,  0x49: 42,  0x4A: 41,  0x4B: 41,  0x4C: 40,  0x4D: 40,  0x4E: 39,  0x4F: 39,
    0x50: 39,  0x51: 38,  0x52: 38,  0x53: 37,  0x54: 37,  0x55: 36,  0x56: 36,  0x57: 36,  0x58: 35,  0x59: 35,  0x5A: 34,  0x5B: 34,  0x5C: 33,  0x5D: 33,  0x5E: 33,  0x5F: 32,
    0x60: 32,  0x61: 31,  0x62: 31,  0x63: 31,  0x64: 30,  0x65: 30,  0x66: 30,  0x67: 29,  0x68: 29,  0x69: 29,  0x6A: 28,  0x6B: 28,  0x6C: 27,  0x6D: 27,  0x6E: 27,  0x6F: 26,
    0x70: 26,  0x71: 26,  0x72: 25,  0x73: 25,  0x74: 24,  0x75: 24,  0x76: 24,  0x77: 23,  0x78: 23,  0x79: 23,  0x7A: 22,  0x7B: 22,  0x7C: 22,  0x7D: 21,  0x7E: 21,  0x7F: 21,
    0x80: 20,  0x81: 20,  0x82: 20,  0x83: 19,  0x84: 19,  0x85: 19,  0x86: 18,  0x87: 18,  0x88: 18,  0x89: 17,  0x8A: 17,  0x8B: 17,  0x8C: 16,  0x8D: 16,  0x8E: 16,  0x8F: 15,
    0x90: 15,  0x91: 15,  0x92: 14,  0x93: 14,  0x94: 14,  0x95: 13,  0x96: 13,  0x97: 13,  0x98: 12,  0x99: 12,  0x9A: 12,  0x9B: 11,  0x9C: 11,  0x9D: 11,  0x9E: 10,  0x9F: 10,
    0xA0: 10,  0xA1: 9,   0xA2: 9,   0xA3: 9,   0xA4: 8,   0xA5: 8,   0xA6: 8,   0xA7: 7,   0xA8: 7,   0xA9: 6,   0xAA: 6,   0xAB: 6,   0xAC: 5,   0xAD: 5,   0xAE: 5,   0xAF: 4,
    0xB0: 4,   0xB1: 4,   0xB2: 3,   0xB3: 3,   0xB4: 3,   0xB5: 2,   0xB6: 2,   0xB7: 2,   0xB8: 1,   0xB9: 1,   0xBA: 0,   0xBB: 0,   0xBC: 0,   0xBD: 0,   0xBE: 0,   0xBF: -1,
    0xC0: -1,  0xC1: -2,  0xC2: -2,  0xC3: -2,  0xC4: -3,  0xC5: -3,  0xC6: -4,  0xC7: -4,  0xC8: -5,  0xC9: -5,  0xCA: -5,  0xCB: -6,  0xCC: -6,  0xCD: -7,  0xCE: -7,  0xCF: -8,
    0xD0: -8,  0xD1: -9,  0xD2: -9,  0xD3: -9,  0xD4: -10, 0xD5: -10, 0xD6: -11, 0xD7: -11, 0xD8: -12, 0xD9: -12, 0xDA: -13, 0xDB: -14, 0xDC: -14, 0xDD: -15, 0xDE: -15, 0xDF: -16,
    0xE0: -16, 0xE1: -17, 0xE2: -18, 0xE3: -18, 0xE4: -19, 0xE5: -20, 0xE6: -20, 0xE7: -21, 0xE8: -22, 0xE9: -22, 0xEA: -23, 0xEB: -24, 0xEC: -25, 0xED: -26, 0xEE: -27, 0xEF: -28,
    0xF0: -29
}

SOURCES = {1: "Slave", 5: "Master", 6: "Unit"}
PRODUCT_TYPES = {0: "Ventilation", 1: "AC", 2: "HeatExchanger"}

MODES = {0: "Cool", 1: "Dehumidify", 2: "Fan", 3: "Auto", 4: "Heat"}
FAN_SPEEDS = {
    0: "Low", 1: "Med", 2: "High", 3: "Auto",
    4: "Slow", 5: "Low-Med", 6: "Med-High", 7: "Power"
}
RESERVATIONS = {
    0: "None", 1: "Turn-On", 2: "Turn-Off",
    3: "Sleep", 4: "Clear All", 5: "Simple Timer"
}


class LG13ByteAnalyzer(HighLevelAnalyzer):
    # Output formatting
    result_types = {
        'status': {
            'format': '[{{data.src}}] Status: {{data.summary}}'
        },
        'capabilities': {
            'format': '[{{data.src}}] Capabilities: {{data.summary}}'
        },
        'settings': {
            'format': '[{{data.src}}] Settings: {{data.summary}}'
        },
        'more_settings': {
            'format': '[{{data.src}}] Advanced: {{data.summary}}'
        },
        'more_status': {
            'format': '[{{data.src}}] Status Ext: {{data.summary}}'
        },
        'extended': {
            'format': '[{{data.src}}] Extended: {{data.summary}}'
        },
        'power_info': {
            'format': '[{{data.src}}] Power: {{data.summary}}'
        },
        'unknown': {
            'format': '[{{data.src}}] Msg Type {{data.msg_type}}: {{data.summary}}'
        },
        'checksum_error': {
            'format': 'ERROR: Bad Checksum! Raw: {{data.raw}}'
        }
    }

    def __init__(self):
        self.buffer = bytearray()
        self.frame_start_time = None
        self.last_byte_end_time = None
        # At 102 baud, one byte (8, N, 1) takes approximately 98 ms to transmit.
        # The inter-packet interval is usually >= 500 ms. A 350 ms timeout resets the buffer if data is lost.
        self.packet_timeout_s = 0.35

    def decode(self, frame: AnalyzerFrame):
        if frame.type != 'data':
            return None

        byte_val = frame.data['data'][0]
        current_start = frame.start_time
        current_end = frame.end_time

        # Buffer flush on inter-byte timeout
        if self.last_byte_end_time is not None:
            if float(current_start - self.last_byte_end_time) > self.packet_timeout_s:
                self.buffer.clear()
                self.frame_start_time = None

        if len(self.buffer) == 0:
            self.frame_start_time = current_start

        self.buffer.append(byte_val)
        self.last_byte_end_time = current_end

        if len(self.buffer) < 13:
            return None

        # Exactly 13 bytes collected — processing packet
        raw_packet = bytes(self.buffer)
        start_time = self.frame_start_time
        end_time = current_end

        self.buffer.clear()
        self.frame_start_time = None

        # Checksum verification: (sum(bytes[0:12]) & 0xFF) ^ 0x55
        calculated_csum = (sum(raw_packet[:12]) & 0xFF) ^ 0x55
        received_csum = raw_packet[12]

        raw_hex = raw_packet.hex(' ')

        if calculated_csum != received_csum:
            return AnalyzerFrame('checksum_error', start_time, end_time, {
                'raw': raw_hex,
                'calc': hex(calculated_csum),
                'recv': hex(received_csum)
            })

        return self.parse_packet(raw_packet, start_time, end_time, raw_hex)

    def parse_packet(self, pkt: bytes, start_time, end_time, raw_hex: str):
        b0 = pkt[0]
        src_id = (b0 >> 5) & 0x07
        prod_id = (b0 >> 3) & 0x03
        msg_type = b0 & 0x07

        src_str = SOURCES.get(src_id, f"Src:{src_id}")
        prod_str = PRODUCT_TYPES.get(prod_id, f"Prod:{prod_id}")

        data = {
            'src': src_str,
            'product': prod_str,
            'msg_type': str(msg_type),
            'raw': raw_hex
        }

        # Type 0: Status message
        if msg_type == 0:
            power = "ON" if (pkt[1] & 0x02) else "OFF"
            mode = MODES.get((pkt[1] >> 2) & 0x07, "Unknown")
            fan = FAN_SPEEDS.get((pkt[1] >> 5) & 0x07, "Unknown")

            # Byte 6 + Byte 5: Temperature setpoint
            setpoint_raw = pkt[6] & 0x0F
            if mode == "Auto": # In AI mode, this offset ranges from -2 to +2.
                setpoint_str = f"{setpoint_raw - 2:+d}"
            else:
                setpoint_val = setpoint_raw + 15.0
                if pkt[5] & 0x01:
                    setpoint_val += 0.5
                setpoint_str = f"{setpoint_val:.1f}°C"

            # Byte 7: Room temperature
            room_temp = ((pkt[7] & 0x3F) / 2.0) + 10.0

            flags = []
            if pkt[1] & 0x01: flags.append("SettingChanged")
            
            # Byte 2
            if pkt[2] & 0x01: flags.append("FilterSign")
            if pkt[2] & 0x04: flags.append("Plasma")
            if pkt[2] & 0x08: flags.append("Humidifier")
            if pkt[2] & 0x10: flags.append("Heater")
            if pkt[2] & 0x20: flags.append("Swirl")
            if pkt[2] & 0x40: flags.append("H-Swing")
            if pkt[2] & 0x80: flags.append("V-Swing")

            # Byte 3
            if pkt[3] & 0x01: flags.append("ExtVent")
            if pkt[3] & 0x02: flags.append("FanAuto")
            if pkt[3] & 0x04: flags.append("Defrost")
            if pkt[3] & 0x08: flags.append("Preheat")
            grill_state = (pkt[3] >> 5) & 0x03
            if grill_state != 0:
                flags.append(f"Grill:{['Def', 'Stop', 'Up', 'Down'][grill_state]}")

            # Byte 5
            if pkt[5] & 0x02: flags.append("Eco")
            if pkt[5] & 0x04: flags.append("OutdoorActive")
            
            # Zones (Byte 5 n Byte 10)
            active_zones = []
            for z_idx, bit in enumerate([0x40, 0x20, 0x10, 0x08], start=1):
                if pkt[5] & bit: active_zones.append(str(z_idx))
            for z_idx, bit in enumerate([0x10, 0x08, 0x04, 0x02], start=5):
                if pkt[10] & bit: active_zones.append(str(z_idx))
            if active_zones:
                flags.append(f"Zones:[{','.join(active_zones)}]")

            # Byte 10
            if pkt[10] & 0x10 and not active_zones: flags.append("AutoClean")
            if pkt[10] & 0x08 and not active_zones: flags.append("RobotClean")

            # Timer / Reserved (Bytes 8 and 9)
            res_type_id = (pkt[8] >> 3) & 0x07
            res_minutes = ((pkt[8] & 0x07) << 8) | pkt[9]
            res_str = ""
            if res_type_id != 0 or res_minutes != 0:
                res_type_str = RESERVATIONS.get(res_type_id, f"Type_{res_type_id}")
                res_str = f", Timer: [{res_type_str}: {res_minutes}m]"

            # Errors (Byte 11)
            error_code = pkt[11]
            err_str = f", Error: CH{error_code}" if error_code != 0 else ""

            flags_str = f" ({', '.join(flags)})" if flags else ""
            summary = f"{power}, {mode}, Set: {setpoint_str}, Room: {room_temp:.1f}°C, Fan: {fan}{flags_str}{res_str}{err_str}"
            data['summary'] = summary
            return AnalyzerFrame('status', start_time, end_time, data)

# Type 1: Capabilities message (0xC9)
        elif msg_type == 1:
            unit_kind_map = {1: "Cassette", 2: "Duct", 4: "Wall"}
            unit_kind = unit_kind_map.get(pkt[1] & 0x07, f"Type_{pkt[1] & 0x07}")

            features = []
            # Bytes 1-2: Basic modes and shutters
            if pkt[1] & 0x80: features.append("V-Swing")
            if pkt[1] & 0x40: features.append("H-Swing")
            if pkt[1] & 0x20: features.append("Swirl")
            if pkt[2] & 0x80: features.append("Dehum")
            if pkt[2] & 0x40: features.append("Fan")
            if pkt[2] & 0x20: features.append("Heat")
            if pkt[2] & 0x10: features.append("AI")
            if pkt[2] & 0x08: features.append("Auto")
            if pkt[2] & 0x04: features.append("Humidifier")
            if pkt[2] & 0x02: features.append("Plasma")
            if pkt[2] & 0x01: features.append("FanAuto")

            # Byte 3: Supported fan speeds
            fans = []
            if pkt[3] & 0x01: fans.append("Auto")
            if pkt[3] & 0x02: fans.append("Power")
            if pkt[3] & 0x04: fans.append("High")
            if pkt[3] & 0x08: fans.append("Med")
            if pkt[3] & 0x10: fans.append("Low")
            if pkt[3] & 0x20: fans.append("Slow")
            if pkt[6] & 0x08: fans.append("Low-Med")
            if pkt[6] & 0x10: fans.append("Med-High")
            if pkt[3] & 0x80: fans.append("Heat-Power")

            # Bytes 4-5: Equipment and vanes
            vanes = "2 Vanes" if (pkt[5] & 0x80) else ("1 Vane" if (pkt[5] & 0x40) else "Default Vanes")
            if pkt[4] & 0x01: features.append("VaneCtrl")
            if pkt[4] & 0x80: features.append("AutoClean")
            if pkt[4] & 0x40: features.append("RobotClean")
            if pkt[5] & 0x01: features.append("Eco")
            if pkt[6] & 0x20: features.append("MinCool16C")

            # Bytes 7-11: Installer and special functions
            if pkt[7] & 0x04: features.append("AuxHeater")
            if pkt[8] & 0x08: features.append("Zones5-8")
            if pkt[8] & 0x10: features.append("EmergHeater")
            if pkt[10] & 0x01: features.append("DRED")
            if pkt[10] & 0x04: features.append("WifiAP")
            if pkt[11] & 0x04: features.append("HimalayaCool")
            if pkt[11] & 0x10: features.append("MosquitoAway")
            if pkt[11] & 0x20: features.append("ComfortCooling")
            if pkt[11] & 0x80: features.append("DryContact")

            summary = f"Kind: {unit_kind} ({vanes}), Fans: [{','.join(fans)}], Features: [{','.join(features)}]"
            data['summary'] = summary
            return AnalyzerFrame('capabilities', start_time, end_time, data)

        # Type 2: Settings (0xAA/0xCA)
        elif msg_type == 2:
            addr = pkt[1]
            
            # Bytes 2-6: Fan speeds (0 = default)
            fan_cfg = []
            speeds = [("Slow", pkt[2]), ("Low", pkt[3]), ("Med", pkt[4]), ("High", pkt[5]), ("Power", pkt[6])]
            for name, val in speeds:
                if val != 0:
                    fan_cfg.append(f"{name}:{val}")
            fan_str = f", FanCal: [{','.join(fan_cfg)}]" if fan_cfg else ""

            # Bytes 7-8: Vane positions (1-4)
            v1, v2 = pkt[7] & 0x0F, (pkt[7] >> 4) & 0x0F
            v3, v4 = pkt[8] & 0x0F, (pkt[8] >> 4) & 0x0F
            vanes_str = f"Vanes: [1:{v1}, 2:{v2}"
            if v3 != 0 or v4 != 0:
                vanes_str += f", 3:{v3}, 4:{v4}"
            vanes_str += "]"

            # Byte 9: Auto Change and auxiliary heater
            auto_change = pkt[9] & 0x07
            aux_heater = "AuxHeater:ON" if (pkt[9] & 0x80) else ""

            # Byte 10: Temperature limits
            min_sp = (pkt[10] & 0x0F) + 15
            max_sp = ((pkt[10] >> 4) & 0x0F) + 15

            # Byte 11: Installer flags
            flags = []
            if pkt[11] & 0x01: flags.append("DryContact:Auto")
            if pkt[11] & 0x02: flags.append("ZoneState:Fixed")
            if pkt[11] & 0x04: flags.append("RobotCleanAuto")
            if pkt[11] & 0x08: flags.append("AutoDryEnabled")
            if aux_heater: flags.append(aux_heater)
            if auto_change > 0: flags.append(f"AutoChangeTemp:{auto_change}")

            flags_str = f", Flags: [{', '.join(flags)}]" if flags else ""
            summary = f"Addr: {addr}, Range: {min_sp}°C-{max_sp}°C, {vanes_str}{fan_str}{flags_str}"
            data['summary'] = summary
            return AnalyzerFrame('settings', start_time, end_time, data)

        # Type 3: More settings & pipe temperatures
        elif msg_type == 3:
            t_in = PIPE_TEMP_TABLE.get(pkt[3], None)
            t_out = PIPE_TEMP_TABLE.get(pkt[4], None)
            t_mid = PIPE_TEMP_TABLE.get(pkt[5], None)

            tin_str = f"{t_in}°C" if t_in is not None else f"raw(0x{pkt[3]:02X})"
            tout_str = f"{t_out}°C" if t_out is not None else f"raw(0x{pkt[4]:02X})"
            tmid_str = f"{t_mid}°C" if t_mid is not None else f"raw(0x{pkt[5]:02X})"

            dred = pkt[1] & 0x03
            wifi_ap = "ON" if (pkt[7] & 0x40) else "OFF"
            req = " (Request)" if (pkt[1] & 0x80) else ""

            summary = f"Pipe Temps: [In: {tin_str}, Out: {tout_str}, Mid: {tmid_str}], DRED: {dred}, AP: {wifi_ap}{req}"
            data['summary'] = summary
            return AnalyzerFrame('more_settings', start_time, end_time, data)

        # Type 4: More status information
        elif msg_type == 4:
            filter_hours = pkt[1] | ((pkt[2] & 0x0F) << 8)
            # Power Consumption BCD (example 64.91.29 => 64912.9 kWh)
            power_kwh = f"{pkt[3]:02X}{pkt[4]:02X}{pkt[5] >> 4:X}.{pkt[5] & 0x0F} kWh"
            room_t = pkt[9] / 2.0
            dual_sp = "DualSP" if (pkt[2] & 0x80) else "SingleSP"

            summary = f"Filter: {filter_hours}h left, PowerTotal: {power_kwh}, Room: {room_t:.1f}°C, Mode: {dual_sp}"
            data['summary'] = summary
            return AnalyzerFrame('more_status', start_time, end_time, data)

        # Type 6: Extended status / settings
        elif msg_type == 6:
            sub_type = pkt[1]
            if sub_type == 0x80:
                humidity = pkt[2]
                fan_time = (pkt[3] << 8) | pkt[4]
                idu_time = (pkt[6] << 8) | pkt[7]
                temp_ext = pkt[10] + (pkt[11] / 10.0)
                summary = f"Humidity: {humidity}%, FanTime: {fan_time}h, IDUTime: {idu_time}h, Precision Room: {temp_ext:.1f}°C"
            elif sub_type == 0x10:
                summary = f"Setting Command: {raw_hex[6:]}"
            else:
                summary = f"Sub-type 0x{sub_type:02X}, Data: {raw_hex[6:]}"
            data['summary'] = summary
            return AnalyzerFrame('extended', start_time, end_time, data)

        # Type 7: Power usage
        elif msg_type == 7:
            # Power format (CF 00 XX XX XX ...)
            summary = f"Current Power Usage Raw: {raw_hex[6:17]}"
            data['summary'] = summary
            return AnalyzerFrame('power_info', start_time, end_time, data)

        # Other types (Type 5 and reserved types)
        else:
            summary = f"Raw: {raw_hex}"
            data['summary'] = summary
            return AnalyzerFrame('unknown', start_time, end_time, data)