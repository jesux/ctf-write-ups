import angr
import logging
import claripy

def main():
    proj = angr.Project('secadmin',  load_options={'auto_load_libs': False})

    argv = [proj.filename]
    argv.append('ctf.hex')

    sym_arg = claripy.BVS('sym_arg', 8*7)
    argv.append(sym_arg)

    state = proj.factory.entry_state(args=argv, concrete_fs=True)

    for byte in sym_arg.chop(8):
        state.add_constraints(byte >= 'a')
        state.add_constraints(byte <= 'z')

    avoid       = (0x400dab, # usage
                   0x400f03, # memory
                   0x400e0c) # illegar char 

    print("Launching exploration")
    sm = proj.factory.simulation_manager(state, threads=16)


    def check(state):
        #print("FIND: %s" % state)
        find = 0x400b49
        if (state.ip.args[0] == find):
            BV_rbp = state.memory.load( state.regs.rbp - 10, 1 )
            xrbp = state.solver.eval(BV_rbp)
            print("RBP-10: 0x%02x" % xrbp)
            return True if xrbp == 0x2d else False
        else:
            return False

    ex = sm.explore(find=check, avoid=avoid)

    # Get stdout
    found = ex.found

    if( len(found)>0 ):
        found = ex.found[0]
        result = found.solver.eval(argv[2], cast_to=str)
    else:
        result = "Couldn't find any paths which satisfied our conditions."

    return result

if __name__ in '__main__':
    print(main())
