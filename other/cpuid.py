import struct
import cpuid_native

def cpuid(leaf):
    _, a, b, c, d = cpuid_native.get_cpuid(leaf)
    return (a, b, c, d)
print cpuid(0)




