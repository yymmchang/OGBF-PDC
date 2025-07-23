def encode_label_to_prefixes(label: str, flip_last_bit=False):
    bin_label = ''.join(f'{ord(c):08b}' for c in label)
    prefixes = []
    for i in range(1, len(bin_label) + 1):
        prefix = bin_label[:i]
        if flip_last_bit and len(prefix) > 0:
            prefix = prefix[:-1] + ('1' if prefix[-1] == '0' else '0')
        prefixes.append(prefix)
    return prefixes