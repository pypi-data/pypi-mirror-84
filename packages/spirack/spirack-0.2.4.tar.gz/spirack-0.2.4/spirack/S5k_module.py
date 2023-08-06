"""AWG module S5k interface

SPI Rack interface code for the S5k AWG module.

Example use : ::
    S5k = S5k_module(SPI_rack1, 3)

Todo:
    *Add readback from DAC ICs
"""

from .spi_rack import SPI_rack
from .chip_mode import AD9106_MODE, AD9106_SPEED, LMK01010_MODE, LMK01010_SPEED, BICPINS_SPEED, BICPINS_MODE
import numpy as np

class S5k_module(object):
    """S5k module interface class

    This class does the low level interfacing with the S5k module. When creating
    an instance it requires a SPI_rack object passed as a parameter.

    The DACs can run in multiple modes: DC-value, sawtooth, noise and AWG. Each
    mode has its own parameters and requirements described by the function.

    Attributes:
        module (int): module number set by the user (must coincide with hardware)
        reference (str): set to either internal or external reference
        DAC_waveform_mode (list(str)): list containing the current functions settings per DAC
        DAC_DC_val (list(int)): list containing the DC values per DAC
        DAC_dgain (list(int)): list containing the (digital) gain settings per DAC
        DAC_doffset (list(int)): list containing the (digital) offsets per DAC
        DAC_clock_div (list(int)): list containing the clock division per DAC (IC)
        module_running (bool): True or False if the module is running
    """

    #Maps the DACs, as numbered at module front plate, to the DAC IC SPI address
    #and internal DAC
    #So DAC 1 maps to DAC IC with SPI addres 3 and internal DAC 4
    DAC_mapping = {1:[3,4], 2:[3,3], 3:[3,1], 4:[3,2], 5:[1,4], 6:[1,3], 7:[1,1], 8:[1,2],
                   9:[4,4], 10:[4,3], 11:[4,1], 12:[4,2], 13:[0,4], 14:[0,3], 15:[0,1], 16:[0,2]}

    def __init__(self, spi_rack, module):
        """Inits S5k module class

        Initialises the S5k module. At initialization the clock source will be
        set to internal and the clock to all DAC ICs will be activated at the
        undivided clock speed.

        Args:
            spi_rack (SPI_rack object): SPI_rack class object via which the communication runs
            module (int): module number set at hardware
        """
        self.spi_rack = spi_rack
        self.module = module

        self.write_LMK_data(0, (1<<31)) #Reset clock distribution
        self.write_LMK_data(0, 1<<16 | 0<<17 | 0b0<<8) #Enable channel 0, undivided
        self.write_LMK_data(1, 1<<16 | 0<<17 | 0b0<<8) #Enable channel 1, undivided
        self.write_LMK_data(6, 1<<16 | 0<<17 | 0b0<<8) #Enable channel 6, undivided
        self.write_LMK_data(7, 1<<16 | 0<<17 | 0b0<<8) #Enable channel 7, undivided

        self.DAreg = AD9106_registers #DAreg contains all AD9106 register addresses
        self.DAC_waveform_mode = 16*[None]
        self.DAC_DC_val = 16*[None]
        self.DAC_dgain = 16*[None]
        self.DAC_doffset = 16*[None]
        self.DAC_clock_div = 16*[1]

        self.module_running = False
        self.reference = None
        self.set_clock_source('internal')
        self.run_module(False)

    def set_waveform_mode(self, DAC, waveform):
        """Sets the selected DAC to a certain waveform mode

        Changes the the mode of the selected DAC to either: DC, sawtooth,
        noise or AWG.

        Args:
            DAC (int: 1-16): DAC of which to change the mode
            waveform (string): waveform type to set
        """
        possible_values = {'DC': 1, 'sawtooth': 0b10001, 'noise': 0b100001, 'AWG': 0}
        if waveform not in possible_values:
            raise ValueError('Value {} does not exist. Possible values are: {}'.format(waveform, possible_values))

        self.DAC_waveform_mode[DAC-1] = waveform

        DAC_IC = S5k_module.DAC_mapping[DAC][0]
        DAC_internal = S5k_module.DAC_mapping[DAC][1]

        if DAC_internal == 1:
            data = self.read_AD9106(self.DAreg.WAV2_1CONFIG, DAC_IC)
            data &= 0xFF00
            data |= possible_values[waveform]
            register = self.DAreg.WAV2_1CONFIG
        elif DAC_internal == 2:
            data = self.read_AD9106(self.DAreg.WAV2_1CONFIG, DAC_IC)
            data &= 0x00FF
            data |= possible_values[waveform]<<8
            register = self.DAreg.WAV2_1CONFIG
        elif DAC_internal == 3:
            data = self.read_AD9106(self.DAreg.WAV4_3CONFIG, DAC_IC)
            data &= 0xFF00
            data |= possible_values[waveform]
            register = self.DAreg.WAV4_3CONFIG
        else:
            data = self.read_AD9106(self.DAreg.WAV4_3CONFIG, DAC_IC)
            data &= 0x00FF
            data |= possible_values[waveform]<<8
            register = self.DAreg.WAV4_3CONFIG

        self.write_AD9106(register, data, DAC_IC)

    def set_sawtooth_parameters(self, DAC, sawtooth_type, stepsize):
        """Set the parameters for sawtooth mode

        Set the type of sawtooth and the stepsize of the sawtooth for a
        specific DAC. DAC needs to be in sawtooth mode to output. The sawtooth
        is generated by a 2^14 counter running at clk/stepsize. The counter is
        fixed but the stepsize can be adjusted from 1 to 63.

        Args:
            DAC (int: 1-16): DAC of which sawtooth settings to change
            sawtooth_type (str): type of sawtooth to output
            stepsize (int: 1-63): clock cycles per counter step
        """
        if self.DAC_waveform_mode[DAC-1] != 'sawtooth':
            print('DAC {} is not set to sawtooth mode!'.format(DAC))

        possible_values = {'ramp_up': 0, 'ramp_down': 1, 'triangle': 2, 'no_wave': 3}
        if sawtooth_type not in possible_values:
            raise ValueError('Value {} does not exist. Possible values are: {}'.format(sawtooth_type, possible_values))

        # Decode which IC and internal DAC is being addressed
        DAC_IC = S5k_module.DAC_mapping[DAC][0]
        DAC_internal = S5k_module.DAC_mapping[DAC][1]

        # Depending on the internal DAC, choose correct registers
        if DAC_internal == 1:
            data = self.read_AD9106(self.DAreg.SAW2_1CONFIG, DAC_IC)
            data &= 0xFF00
            data |= (stepsize<<2) | possible_values[sawtooth_type]
            register = self.DAreg.SAW2_1CONFIG
        elif DAC_internal == 2:
            data = self.read_AD9106(self.DAreg.SAW2_1CONFIG, DAC_IC)
            data &= 0x00FF
            data |= (stepsize<<10) | (possible_values[sawtooth_type]<<8)
            register = self.DAreg.SAW2_1CONFIG
        elif DAC_internal == 3:
            data = self.read_AD9106(self.DAreg.SAW4_3CONFIG, DAC_IC)
            data &= 0xFF00
            data |= (stepsize<<2) | possible_values[sawtooth_type]
            register = self.DAreg.SAW4_3CONFIG
        else:
            data = self.read_AD9106(self.DAreg.SAW4_3CONFIG, DAC_IC)
            data &= 0x00FF
            data |= (stepsize<<10) | (possible_values[sawtooth_type]<<8)
            register = self.DAreg.SAW4_3CONFIG

        self.write_AD9106(register, data, DAC_IC)

    def set_DC_value(self, DAC, value):
        """Set the DC value

        This sets the DC value for when the DAC is in DC mode. This value is
        also output when the DAC is in any other mode, but the module is not
        running.

        Args:
            DAC (int: 1-16): DAC of which DC value to change
            value (float): Voltage within range -2.875 -> 2.857
        """
        if self.DAC_waveform_mode[DAC-1] != 'DC':
            #raise ValueError('DAC {} needs to be set to DC to set DC value'.format(DAC))
            print("Warning! DAC will only output this DC level when the module is NOT running/triggered!")

        Vmax = 2.857
        Vmin = -2.875
        Vdif = Vmax - Vmin

        if value > Vmax:
            print('Warning! Value too high, set to: {}'.format(Vmax))
            value = Vmax
        elif value < Vmin:
            print('Warning! Value too low, set to: {}'.format(Vmin))
            value = Vmin

        self.DAC_DC_val[DAC-1] = value
        intval = int((-4096/Vdif * value) - 7) #Calculate int value from float
        data = intval << 4

        DAC_IC = S5k_module.DAC_mapping[DAC][0]
        DAC_internal = S5k_module.DAC_mapping[DAC][1]

        if DAC_internal == 1:
            register = self.DAreg.DAC1_CST
        elif DAC_internal == 2:
            register = self.DAreg.DAC2_CST
        elif DAC_internal == 3:
            register = self.DAreg.DAC3_CST
        else:
            register = self.DAreg.DAC4_CST

        self.write_AD9106(register, data, DAC_IC)

    def set_digital_gain(self, DAC, gain):
        """Set the digital gain

        Sets the digital gain of the DAC.

        Args:
            DAC (int: 1-16): DAC of which DC value to change
            gain (float): value between -1.99 and 2.0
        """
        gain = -gain # Compensate for inverting amplifier
        self.DAC_dgain[DAC-1] = gain
        data = int(gain*(1<<14))

        DAC_IC = S5k_module.DAC_mapping[DAC][0]
        DAC_internal = S5k_module.DAC_mapping[DAC][1]

        if DAC_internal == 1:
            register = self.DAreg.DAC1_DGAIN
        elif DAC_internal == 2:
            register = self.DAreg.DAC2_DGAIN
        elif DAC_internal == 3:
            register = self.DAreg.DAC3_DGAIN
        else:
            register = self.DAreg.DAC4_DGAIN

        self.write_AD9106(register, data, DAC_IC)

    def set_digital_offset(self, DAC, offset):
        """Set the digital offset

        Sets the digital offset of the DAC.

        Args:
            DAC (int: 1-16): DAC of which DC value to change
            offset (float): value between -2.85 and 2.85
        """
        #12 bit offset
        Vmax = 2.857
        Vmin = -2.875
        Vdif = Vmax - Vmin

        if offset > Vmax:
            print('Warning! Value too high, set to: {}'.format(Vmax))
            offset = Vmax
        elif offset < Vmin:
            print('Warning! Value too low, set to: {}'.format(Vmin))
            offset = Vmin

        self.DAC_doffset[DAC-1] = offset
        intval = int((-4096/Vdif * offset) - 7)
        data = intval << 4

        DAC_IC = S5k_module.DAC_mapping[DAC][0]
        DAC_internal = S5k_module.DAC_mapping[DAC][1]

        if DAC_internal == 1:
            register = self.DAreg.DAC1DOF
        elif DAC_internal == 2:
            register = self.DAreg.DAC2DOF
        elif DAC_internal == 3:
            register = self.DAreg.DAC3DOF
        else:
            register = self.DAreg.DAC4DOF

        self.write_AD9106(register, data, DAC_IC)

    def run_module(self, run):
        """Starts the module

        Set all DAC outputs to run and start outputting a trigger. Can also
        be done by an external trigger in on the front of the module.

        Args:
            run (bool): Set module running True or False
        """
        self.module_running = run

        for i in [0, 1, 3, 4]:
            self.write_AD9106(self.DAreg.PAT_STATUS, run, i)

        # Check to see if internal oscillator needs to be disabled
        if self.reference == 'internal':
            reference = 1
        else:
            reference = 0

        self.spi_rack.write_data(self.module, 5, BICPINS_MODE, BICPINS_SPEED, bytearray([reference | 2 | (run<<7)]))

    def upload_waveform(self, DAC, waveform, start_addr, set_pattern_length=True):
        """Upload waveform to selected DAC

        Args:
            DAC (int: 1-16): DAC which to upload to
            waveform (int array): integer array containing values between -2048 and 2047
            start_addr (int): location of first address to upload to
            set_pattern_length (bool): set the pattern length of the DAC to the uploaded waveform length
        """
        if len(waveform) + start_addr > 4096:
            raise ValueError('Waveform length + starting address exceeds RAM size! Max 4096.')

        # Make sure values don't exceed min or max
        new_waveform = np.zeros_like(waveform)
        np.clip(waveform, a_min=-2048, a_max=2047, out=new_waveform)

        if not np.array_equal(waveform, new_waveform):
            print("Warning! Values in the waveform exceed the minimum ({}) or ".format(-2048),
                  "maximum values ({}) and have been clipped.".format(2047))

        DAC_IC = S5k_module.DAC_mapping[DAC][0]

        # Shift into correct place for registers
        new_waveform = new_waveform<<4
        # Reverse waveform order, register in IC gets updated in Reverse
        new_waveform = np.flipud(new_waveform)

        # Create new array to fit all the bytes
        # Waveform data is 16-bit, but SPI data is 8-bit
        ordered_data = np.zeros(2*len(new_waveform), dtype=np.uint8)
        ordered_data[0::2] = (new_waveform >> 8) & 0xFF
        ordered_data[1::2] = new_waveform & 0xFF

        # Can send maximum of 60 data bytes (+ 2 registers bytes) at a timeout
        # Split up data array into groups of ~60 for maximum data transfer
        s_data = np.split(ordered_data, np.arange(60, len(ordered_data), 60))

        # Start addres. Is traversed in reverse direction so need to start
        # at the end
        start_addr += (0x6000 + len(new_waveform) - 1)

        self.run_module(False)
        self.write_AD9106(self.DAreg.PAT_STATUS, 1<<2, DAC_IC)

        # Write data points in groups of 30 (2 bytes each)
        for group in s_data:
            addr_bytes = bytearray([(start_addr >> 8) & 0xFF, start_addr & 0xFF])
            self.spi_rack.write_data(self.module, DAC_IC, AD9106_MODE, AD9106_SPEED,
                                     addr_bytes + group.tobytes())
            start_addr -= int(len(group)/2)

        self.write_AD9106(self.DAreg.PAT_STATUS, 0, DAC_IC)

        if set_pattern_length is True:
            self.set_pattern_length_DAC(DAC, len(waveform))

    def set_RAM_address(self, DAC, start_pos, stop_pos):
        """Set addresses for AWG mode

        Sets the start and stop address for the selected DAC in AWG mode. When the
        DAC is running it will output data from this address range.

        Args:
            DAC (int: 1-16): DAC of which to set the addresses
            start_pos (int): start address of waveform
            stop_pos (int): stop address of waveform
        """
        #start and stop both 12 bit
        if stop_pos > 4096:
            raise ValueError('Stop address {} is larger than max value 4096!'.format(stop_pos))
        elif start_pos > stop_pos:
            raise ValueError('Start address {} is larger than stop address {}!'. format(start_pos, stop_pos))

        DAC_IC = S5k_module.DAC_mapping[DAC][0]
        DAC_internal = S5k_module.DAC_mapping[DAC][1]

        if DAC_internal == 1:
            start_register = self.DAreg.START_ADDR1
            stop_register = self.DAreg.STOP_ADDR1
        elif DAC_internal == 2:
            start_register = self.DAreg.START_ADDR2
            stop_register = self.DAreg.STOP_ADDR2
        elif DAC_internal == 3:
            start_register = self.DAreg.START_ADDR3
            stop_register = self.DAreg.STOP_ADDR3
        else:
            start_register = self.DAreg.START_ADDR4
            stop_register = self.DAreg.STOP_ADDR4

        data = start_pos << 4
        self.write_AD9106(start_register, data, DAC_IC)
        data = stop_pos << 4
        self.write_AD9106(stop_register, data, DAC_IC)

    def set_pattern_length_DAC(self, DAC, length):
        DAC_IC = S5k_module.DAC_mapping[DAC][0]
        self.write_AD9106(self.DAreg.PAT_PERIOD, length, DAC_IC)

    def set_pattern_length_trigger(self, length):
        if length not in range(10, 4095):
            raise ValueError('Value {} not allowed. Needs to be between 10 and 4095'.format(length))

        b1 = (length>>8) & 0xFF
        b2 = length & 0xFF
        s_data = bytearray([b1, b2])

        self.spi_rack.write_data(self.module, 7, BICPINS_MODE, BICPINS_SPEED, s_data)

    def set_clock_source(self, source):
        possible_values = {'internal':0, 'external':1}
        if source not in possible_values:
            raise ValueError('Value {} does not exist. Possible values are: {}'.format(source, possible_values))

        self.reference = source
        self.write_LMK_data(14, (1<<30) | (possible_values[source]<<29) |(1<<27))
        self.sync_clock()

    def sync_clock(self):
        # Check to see if internal oscillator needs to be disabled
        if self.reference == 'internal':
            reference = 1
        else:
            reference = 0

        # Toggles the sync pin on the clock distribution/divider IC to sync
        # up all the clocks. Necessary after any clock change
        self.spi_rack.write_data(self.module, 5, BICPINS_MODE, BICPINS_SPEED,
                                 bytearray([reference | 2 | (self.module_running<<7)]))
        self.spi_rack.write_data(self.module, 5, BICPINS_MODE, BICPINS_SPEED,
                                 bytearray([reference | 0 | (self.module_running<<7)]))
        self.spi_rack.write_data(self.module, 5, BICPINS_MODE, BICPINS_SPEED,
                                 bytearray([reference | 2 | (self.module_running<<7)]))

    def set_clock_division(self, DAC, divisor):
        allowed_values = [1] + list(range(2, 512, 2))
        if divisor not in allowed_values:
            raise ValueError('Allowed values are: 1, 2, 4, 6, 8, ..., 510')

        if divisor == 1:
            data = 1<<16 | 0<<17 | 0<<8
        else:
            data = 1<<16 | 1<<17 | int((divisor/2))<<8

        DAC_IC = S5k_module.DAC_mapping[DAC][0]
        # Connect each DAC_IC (SPI address) to the correct LMK register
        LMK_reg = {0:6, 1:7, 3:0, 4:1}
        self.write_LMK_data(LMK_reg[DAC_IC], data)

        # Update the values in the DAC_clock_div array for all affected DACs
        for i in range(0, 16, 4):
            if DAC-1 in range(i, i+4):
                self.DAC_clock_div[i:i+4] = 4*[divisor]

        # Update the clock to the BIC to be the slowest used clock at the moment
        # This is the clock with the largest divider
        max_divisor = max(self.DAC_clock_div)
        if max_divisor == 1:
            data = 1<<16 | 0<<17 | 0<<8
        else:
            data = 1<<16 | 1<<17 | int((max_divisor/2))<<8
        self.write_LMK_data(3, data)

        # Synchronise all the clocks
        self.sync_clock()

    def write_LMK_data(self, register, data):
        b1 = (data>>24) & 0xFF
        b2 = (data>>16) & 0xFF
        b3 = (data>>8) & 0xFF
        b4 = (data&0xFF) | (register & 0xF)

        s_data = bytearray([b1, b2, b3, b4])
        self.spi_rack.write_data(self.module, 2, LMK01010_MODE, LMK01010_SPEED, s_data)

    def write_AD9106(self, register, data, SPI_addr):
        b1 = (register>>8) & 0xFF
        b2 = register & 0xFF
        b3 = (data>>8) & 0xFF
        b4 = data&0xFF
        s_data = bytearray([b1, b2, b3, b4])
        self.spi_rack.write_data(self.module, SPI_addr, AD9106_MODE, AD9106_SPEED, s_data)

        #update
        s_data = bytearray([0, self.DAreg.RAMUPDATE, 0, 1])
        self.spi_rack.write_data(self.module, SPI_addr, AD9106_MODE, AD9106_SPEED, s_data)

    def read_AD9106(self, register, SPI_addr):
        b1 = 1<<7
        b2 = register
        s_data = bytearray([b1, b2, 0, 0])
        r_data = self.spi_rack.read_data(self.module, SPI_addr, AD9106_MODE, AD9106_SPEED, s_data)

        return int.from_bytes(r_data[2:4], byteorder='big')

class AD9106_registers:
    SPICONFIG = 0x00
    POWERCONFIG = 0x01
    CLOCKCONFIG = 0x02
    REFADJ = 0x03
    DAC4AGAIN = 0x04
    DAC3AGAIN = 0x05
    DAC2AGAIN = 0x06
    DAC1AGAIN = 0x07
    DACxRANGE = 0x08
    DAC4RSET = 0x09
    DAC3RSET = 0x0A
    DAC2RSET = 0x0B
    DAC1RSET = 0x0C
    CALCONFIG = 0x0D
    COMPOFFSET = 0x0E
    RAMUPDATE = 0x1D
    PAT_STATUS = 0x1E
    PAT_TYPE = 0x1F
    PATTERN_DLY = 0x20
    DAC4DOF = 0x22
    DAC3DOF = 0x23
    DAC2DOF = 0x24
    DAC1DOF = 0x25
    WAV4_3CONFIG = 0x26
    WAV2_1CONFIG = 0x27
    PAT_TIMEBASE = 0x28
    PAT_PERIOD = 0x29
    DAC4_3PATx = 0x2A
    DAC2_1PATx = 0x2B
    DOUT_START_DLY = 0x2C
    DOUT_CONFIG = 0x2D
    DAC4_CST = 0x2E
    DAC3_CST = 0x2F
    DAC2_CST = 0x30
    DAC1_CST = 0x31
    DAC4_DGAIN = 0x32
    DAC3_DGAIN = 0x33
    DAC2_DGAIN = 0x34
    DAC1_DGAIN = 0x35
    SAW4_3CONFIG = 0x36
    SAW2_1CONFIG = 0x37
    DDS_TW32 = 0x3E
    DDS_TW1 = 0x3F
    DDS4_PW = 0x40
    DDS3_PW = 0x41
    DDS2_PW = 0x42
    DDS1_PW = 0x43
    TRIG_TW_SEL = 0x44
    DDSx_CONFIG = 0x45
    TW_RAM_CONFIG = 0x47
    START_DLY4 = 0x50
    START_ADDR4 = 0x51
    STOP_ADDR4 = 0x52
    DDS_CYC4 = 0x53
    START_DLY3 = 0x54
    START_ADDR3 = 0x55
    STOP_ADDR3 = 0x56
    DDS_CYC3 = 0x57
    START_DLY2 = 0x58
    START_ADDR2 = 0x59
    STOP_ADDR2 = 0x5A
    DDS_CYC2 = 0x5B
    START_DLY1 = 0x5C
    START_ADDR1 = 0x5D
    STOP_ADDR1 = 0x5E
    DDS_CYC1 = 0x5F
    CFG_ERROR = 0x60
    SRAM_DATA = 0x6000
