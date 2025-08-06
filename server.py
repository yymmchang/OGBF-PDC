from prefix_encoding import encode_label_to_prefixes
from Bloom import Bloom
from OTSender import OTSender
import random


# 讀取 nameC.txt 並解析成 (key, label) 格式
def load_data_from_txt(filepath):
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) == 2:
                key = parts[0].strip()
                label = parts[1].strip()
                data.append((key, label))
    return data

server_data = load_data_from_txt("nameS.txt")
prefix_inputs = []
for key, label in server_data:
    prefixes = encode_label_to_prefixes(label)
    prefix_inputs.extend([key + ":" + p for p in prefixes])

bloom = Bloom(prefix_inputs, m=512)
bloom.generateGarbledBloom()
GBFs = bloom.getGarbledBloom()
lam = bloom.getLambda()
M0 = [random.getrandbits(lam) for _ in range(len(GBFs))]

generator = 2045999832912957017696899038249723031652808586302786492701737751786256859920910559231421909153586598647911069920255352007045971901844488687357123721071418415
prime = 3989530240576982954905516988490555817184633741429235826809988606295372830739893893426271188667859430615399162320627698099477463527541398969175342947764145393
q = 4889130196785518327090094348640387030863521741947592925012240939087466704338105261551802927289043419871812698922337865317987087656300734030852135965397237

OTs = OTSender(generator, prime, q)
OTs.Obliviously_Send(M0, GBFs, len(GBFs), lam)
print("[Server] GBF and OT transfer complete.")
