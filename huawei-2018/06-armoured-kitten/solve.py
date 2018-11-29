#!/usr/bin/env python3
import angr

p = angr.Project("re1", auto_load_libs=False)

initial_state = p.factory.blank_state(addr=0x400658)

class donothing(angr.SimProcedure):
    def run(self):
        pass

p.hook(0x4070d0, donothing(), replace=True)
p.hook(0x406ab0, donothing(), replace=True)

loops = 0
def check(state):
    global loops
    #print("[+] %s" % state)
    if state.ip.args[0] == 0x4008e8:
        return True
    elif state.ip.args[0] == 0x400858:
        loops += 1
        if loops >= 20:
            return True

    return False

sm = p.factory.simulation_manager(initial_state)

sm.one_active.options.add(angr.options.LAZY_SOLVES)
#e = sm.explore(find=0x004008e8, avoid=0x00400844)
e = sm.explore(find=check, avoid=0x400844)
print(e)

if len(e.found) > 0:
    s = e.found[0]
    sp =  s.solver.eval(s.regs.sp)
    print("SP: %x" % sp)
    key = []
    for i in range(20):
        key.append(s.mem[sp+30288 + i].char.concrete.decode('utf-8'))
    print(''.join(key))
