# cpu_model_features
This is a script to find the intersection features of CPU model for qemu-kvm

For example on an ivybridge platform, you can get the follow result:

$ python libvirt_model_features.py -m haswell,kvm32 -f "avx_unspport,sse"

================================================================================
All features of model kvm32 defined in libvirt are supported by qemu.
**** libvirt does not support 1 featurs:
    ['avx_unspport']
**** qemu does not support 1 featurs:
    ['avx_unspport']

================================================================================
These features defined in libvirt for model Haswell are not supported by qemu:
    avx2, rtm, bmi1, invpcid, bmi2, movbe, hle, fma
**** libvirt does not support 1 featurs:
    ['avx_unspport']
**** qemu does not support 1 featurs:
    ['avx_unspport']

# libvirt_model_features.py
This is a script  to get the features of a model defined in libvirt are not
supported by qemu.

For example on an ivybridge platform, you can get the follow result:

$ python intersection_features.py -m haswell,kvm32 -f "avx_unspport,sse"

================================================================================
model: kvm32
    support 55 featurs: ['kvmclock', 'pge', 'avx', 'clflush', 'sep', 'syscall', 'tsc-deadline', 'kvm_pv_eoi', 'fsgsbase', 'xsave', 'msr', 'vmx', 'kvm_pv_unhalt', 'erms', 'cmov', 'f16c', 'smep', 'ssse3', 'tsc', 'fxsr', 'pae', 'mce', 'vme', 'mmx', 'cx8', 'rdtscp', 'mca', 'pse', 'popcnt', 'apic', 'sse', 'pat', 'kvm_steal_time', 'kvm_asyncpf', 'lahf_lm', 'aes', 'sse2', 'ss', 'hypervisor', 'pcid', 'de', 'fpu', 'cx16', 'pse36', 'mtrr', 'rdrand', 'kvm_nopiodelay', 'x2apic', 'sse4.2|sse4_2', 'sse4.1|sse4_1', 'pclmulqdq|pclmuldq', 'pni|sse3', 'lm|i64', 'fxsr_opt|ffxsr', 'nx|xd']
    **** do not support 1 featurs: ['avx_unspport']

================================================================================
model: Haswell
    support 55 featurs: ['kvmclock', 'pge', 'avx', 'clflush', 'sep', 'syscall', 'tsc-deadline', 'kvm_pv_eoi', 'fsgsbase', 'xsave', 'msr', 'vmx', 'kvm_pv_unhalt', 'erms', 'cmov', 'f16c', 'smep', 'ssse3', 'tsc', 'fxsr', 'pae', 'mce', 'vme', 'mmx', 'cx8', 'rdtscp', 'mca', 'pse', 'popcnt', 'apic', 'sse', 'pat', 'kvm_steal_time', 'kvm_asyncpf', 'lahf_lm', 'aes', 'sse2', 'ss', 'hypervisor', 'pcid', 'de', 'fpu', 'cx16', 'pse36', 'mtrr', 'rdrand', 'kvm_nopiodelay', 'x2apic', 'sse4.2|sse4_2', 'sse4.1|sse4_1', 'pclmulqdq|pclmuldq', 'pni|sse3', 'lm|i64', 'fxsr_opt|ffxsr', 'nx|xd']
    **** do not support 1 featurs: ['avx_unspport']
