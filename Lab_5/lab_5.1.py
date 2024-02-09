import time
import sys
from SX127x.LoRa import *
from SX127x.board_config import BOARD

BOARD.setup()
BOARD.reset()

class myLora(LoRa):
    def __init__(self, verbose=False):
        super(myLora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.set_pa_config(pa_select=1)

    def on_rx_done(self):
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        mens = bytes(payload).decode("utf-8", 'ignore')
        mens = mens[2: -1] # To discard \x00 in the beginning and \x00 in the end
        print("Receive from LoRa2: ", mens, "\n")

        time.sleep(2)

    def on_tx_done(self):
        print("TxDone\n")
        print(self.clear_irq_flags())

    def start(self):
        while True:
            info = input("Enter your name: ")
            self.val = self.val + 1
            print("Sending: ", info, "\n")

            word1 = list(info)
            word2 = []
            for f in word1:
                word2.append(ord(f))
            data = [0, 0] + word2 + [0]
            self.write_payload(data) # Send INF
            self.set_mode(MODE.TX)
            time.sleep(3)
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCONT)
            time.sleep(10)

lora = myLora(verbose=False)

lora.set_pa_config(pa_select=1, max_power=21, output_power=15)
lora.set_freq(421.2) # From 420.0 to 480.0
lora.set_bw(BW.BW250)
lora.set_coding_rate(CODING_RATE.CR4_5)
lora.set_spreading_factor(7)
lora.set_rx_crc(True)
lora.set_low_data_rate_optim(True)

assert(lora.get_agc_auto_on() == 1)

try:
    print("Start LoRA 1 \n")
    lora.start()

except KeyboardInterrupt:
    sys.stdout.flush()
    print("Exit")
    sys.stderr.write("KeyboardInterrupt\n")

finally:
    sys.stdout.flush()
    print("Exit")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()