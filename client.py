from prefix_encoding import encode_label_to_prefixes
from Bloom import Bloom
from OTRecv import OTRecv

client_data = [("A", "cat"), ("B", "dig"), ("C", "bird")]
encoded_prefixes = []
key_label_map = {}
for key, label in client_data:
    prefixes = encode_label_to_prefixes(label, flip_last_bit=True)
    key_label_map[key] = prefixes
    encoded_prefixes.extend([key + ":" + p for p in prefixes])

bloom = Bloom(encoded_prefixes, m=512)
bloom.generateBloom()
BFc = bloom.getBloom()
lam = bloom.getLambda()

generator = 2045999832912957017696899038249723031652808586302786492701737751786256859920910559231421909153586598647911069920255352007045971901844488687357123721071418415
prime = 3989530240576982954905516988490555817184633741429235826809988606295372830739893893426271188667859430615399162320627698099477463527541398969175342947764145393
q = 4889130196785518327090094348640387030863521741947592925012240939087466704338105261551802927289043419871812698922337865317987087656300734030852135965397237

OTc = OTRecv(generator, prime, q)
GBFi = OTc.obliviouslyReceive(BFc, len(BFc), lam)

misclassified_keys = []
for key, prefixes in key_label_map.items():
    match_count = sum(1 for p in prefixes if bloom.queryGarbled(key + ":" + p, GBFi))
    if match_count != len(prefixes):
        misclassified_keys.append((key, match_count, len(prefixes)))

print("[Client] Misclassified keys:", misclassified_keys)
