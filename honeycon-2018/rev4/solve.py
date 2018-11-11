import angr
import claripy
import sys

p = angr.Project("rev4", auto_load_libs=False)

sym_arg_size = int(sys.argv[1])
sym_arg = claripy.BVS('sym_arg', 8*sym_arg_size)

argv = [p.filename]
argv.append(sym_arg)
initial_state = p.factory.entry_state(args=argv)

init = ''

i = 0
for byte in sym_arg.chop(8):
    if i<len(init):
        initial_state.add_constraints(byte == init[i])
    else:
        initial_state.add_constraints(byte >= '0')
        initial_state.add_constraints(byte <= 'z')
    i += 1

sm = p.factory.simulation_manager(initial_state)
e = sm.explore(find=0x00400773, avoid=(0x0040077f, 0x0040078b))

print(e)

if len(e.found) > 0:
    s = e.found[0]
    results = s.solver.eval_upto(argv[1], 100)
    if len(results)>0:
        print("[+] Found %d solutions" % len(results))
        for result in results:
            print(bytes.fromhex('%x' % result).decode('utf-8'))

