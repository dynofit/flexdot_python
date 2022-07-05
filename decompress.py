
def get_nybble(packet, nybble):
    ch = packet[nybble // 2]
    if nybble % 2 == 0:
        return (ch // 16) & 0xf
    else:
        return ch & 0xf


def decompress(packet):


    v_0 = packet[0]
    ret = [v_0]
    
    # Exclude the first byte (no encoding) and last (sequence number)
    nybbles = (len(packet)-1)*2
    n_ind = 2
    while n_ind < nybbles:
        nybble = get_nybble(packet, n_ind)
        n_ind +=1

        dv = 0
        if nybble == 0xf:
            if not (n_ind + 1 < nybbles):
                break

            v_h = get_nybble(packet, n_ind)
            n_ind += 1
            v_l = get_nybble(packet, n_ind)
            n_ind += 1

            dv = v_h * 16 + v_l
        else:
            if nybble <= 7:
                dv = nybble
            else:
                dv = nybble -8 + 249


        v_0  = (v_0 + dv) & 0xff
        ret.append(v_0)

    return ret


if __name__ == "__main__":
    raw = []
    compressed = []

    with open("sample.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            s = line.split()
            if s[0] == "Original":
                raw.append(int(s[1]))
            elif s[0] == "Packet":
                compressed.append(bytearray([int(i) for i in s[1:]]))

    decompressed = []
    for p in compressed:
       decompressed += decompress(p)

    print(len(decompressed))
    print(len(raw))

    if raw[:len(decompressed)] != decompressed:
        raise Exception();

    print("Tests passed")
