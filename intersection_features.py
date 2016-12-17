#!/usr/bin/python

"""
This is a script to find the intersection features of CPU model for qemu-kvm
"""

import argparse
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
    status, output = commands.getstatusoutput(
       '%s -enable-kvm -cpu help' % binary)

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
        'DISPLAY=fake.host.display:n.0 %s -enable-kvm -cpu %s,+%s,check' %
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


def main(args):
    if len(sys.argv) > 1:
        if "--help" in sys.argv or "-h" in sys.argv:
            usage()

    binary = args.b
    if varify_binary(binary) != 0:
        exit()

    models, features = get_models_and_features(QEMU_BINARY)

    model_feature = {}
    probe_models = models
    if args.m:
        probe_models = args.m.split(",")
        probe_models_map = dict([(m.lower(), m) for m in probe_models])
        all_models_map  = dict([(m.lower(), m) for m in models])

        unsupport_m = set(probe_models_map.keys()) - set(all_models_map.keys())
        if unsupport_m:
            m = [probe_models_map[k] for k in unsupport_m]
            print 'qemu does not support these models: "%s"' % ",".join(m)
            print 'please choose these models: "%s"' % ",".join(models)
            exit(1)
        probe_models = [all_models_map[m] for m in probe_models_map.keys()]

    for model in probe_models:
        support_f = get_model_features(QEMU_BINARY, model, features)
        model_feature[model] = support_f

    for k, v in model_feature.items():
        print "=" * 80
        print "model: %s" % k
        print "    support %s featurs: %s" % (len(v), v)
        if args.f:
            features = ",".join(v)
            features = features.replace("|", ",")
            unsupport_f = set(args.f.split(",")) - set(features.split(","))
            if unsupport_f:
                print "    **** do not support %s featurs: %s" % (
                     len(unsupport_f ), list(unsupport_f))
        print ""


if __name__ == "__main__":
    QEMU_BINARY = "qemu-system-x86_64"
    parser = argparse.ArgumentParser(
        description="find the intersection features of CPU model")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("-m", "--model", type=str, default="", dest="m",
                        help='The models name of cpu, -m "Haswell, ivybridge"')
    parser.add_argument("-f", "--feature", type=str, default="", dest="f",
                        help='The features to be probed, -f "avx,sse"')
    parser.add_argument("-b", "--binary", type=str,
                        default=QEMU_BINARY, dest="b",
                        help='The models name of cpu, -m "Haswell, ivybridge"')
    args = parser.parse_args()
    main(args)
