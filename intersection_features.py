#!/usr/bin/python

"""
This is a script to find the intersection features of CPU model for qemu-kvm
"""

import commands
import re
import sys

FLAGS_DELIMITER = "Recognized CPUID flags:"
PATTERN = re.compile(
    r'CPU feature (.*?) not found'
    '|warning:.*support requested feature: CPUID\..*:.*\.(.*?) \[.*\]')


def usage():
    print "usage:"
    print "# %s [qemu-binary]" % sys.argv[0]
    print "      default qemu-binary is qemu-system-x86_64"


def varify_binary(binary):
    status, output = commands.getstatusoutput("which %s" % binary)
    if status != 0:
        print "can not find qemu binary: %s" % binary
        usage()
    return status


def get_models_and_features(binary):
    status, output = commands.getstatusoutput('%s -cpu help' % binary)

    models = None
    if status == 0:
        models, features = output.split(FLAGS_DELIMITER)

    models = [model.split()[1] for model in models.splitlines() if
              len(model) > 1] if models else models

    error_model = ["GLib-WARNING"]
    models = list(set(models) - set(error_model))
    return models, features


def get_model_features(binary, model, features, pattern=PATTERN):
    def dup_and_alias_features(features):
        # alias_pattern = re.compile(r'\s.*\|.*\s')
        dup_features = features.replace("|", " ")
        alias_features = [f for f in features.split() if "|" in f]
        return dup_features, alias_features

    dup, aliases = dup_and_alias_features(features)
    feature_args = ",+".join(dup.split())
    status, output = commands.getstatusoutput(
        'DISPLAY=fake.host.display:n.0 %s -cpu %s,+%s,check' %
        (binary, model, feature_args))
    filters = pattern.findall(output)
    filters = [ f[0] or f[1] for f in filters]
    support_f = list(set(dup.split()) - set(filters))

    for alias in aliases:
        a1, a2 = alias.split("|")
        if a1 in support_f and a2 in support_f:
            support_f.remove(a1)
            support_f.remove(a2)
            support_f.append(alias)

    return support_f


def main():
    QEMU_BINARY = "qemu-system-x86_64  -enable-kvm"
    if len(sys.argv) > 1:
        if "--help" in sys.argv or "-h" in sys.argv:
            usage()
        else:
            QEMU_BINARY = sys.argv[1]
    
    binary = QEMU_BINARY.split()[0]
    if varify_binary(binary) != 0:
        exit()

    models, features = get_models_and_features(QEMU_BINARY)

    model_feature = {}
    for model in models:
        support_f = get_model_features(QEMU_BINARY, model, features)
        model_feature[model] = support_f

    for k, v in model_feature.items():
        print "=" * 80
        print "model: %s" % k
        print "    support %s featurs: %s" % (len(v), v)
        print ""


if __name__ == "__main__":
    main()
