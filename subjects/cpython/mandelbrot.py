import sys

def main(size):
    cout = sys.stdout.buffer.write
    xr_size = range(size)
    xr_iter = range(50)
    bit = 128
    byte_acc = 0

    cout(("P4\n%d %d\n" % (size, size)).encode('ascii'))

    size = float(size)
    for y in xr_size:
        fy = 2j * y / size - 1j
        for x in xr_size:
            z = 0j
            c = 2. * x / size - 1.5 + fy

            for i in xr_iter:
                z = z * z + c
                if abs(z) >= 2.0:
                    break
            else:
                byte_acc += bit

            if bit > 1:
                bit >>= 1
            else:
                print(byte_acc)
                bit = 128
                byte_acc = 0

        if bit != 128:
            print(byte_acc)
            bit = 128
            byte_acc = 0

if __name__ == '__main__':
  print(int(sys.argv[1]))
  main(int(sys.argv[1]))
