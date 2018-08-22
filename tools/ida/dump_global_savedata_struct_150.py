import idaapi
import idautils
import idc
import os

# only valid in 1.5.0
LOAD_SAVEDATA_FUNCTION_START = 0x71008BF8A0
LOAD_SAVEDATA_FUNCTION_END = 0x71008E3DB8
CRC32_FUNCTION_EA = 0x7100B2170C
SAVEDATA_STRUCT = 0x710246F9E0

with open(os.path.dirname(os.path.realpath(__file__)) + "/global_savedata_struct_150.h", "w") as file:
    file.write("// LOAD_SAVEDATA_FUNCTION: %016x-%016x\n" % \
                  (LOAD_SAVEDATA_FUNCTION_START, LOAD_SAVEDATA_FUNCTION_END))
    file.write("// CRC32_FUNCTION: %016x\n" % CRC32_FUNCTION_EA)
    file.write("struct Savedata {\n")

    struct_offset = 0
    for ref in idautils.CodeRefsTo(idc.GetFunctionAttr(CRC32_FUNCTION_EA, idc.FUNCATTR_START), 1):
        if not (LOAD_SAVEDATA_FUNCTION_START < ref < LOAD_SAVEDATA_FUNCTION_END):
            continue

        string_xref = idaapi.get_arg_addrs(ref)[0]
        iterator = idautils.XrefsFrom(string_xref, 0)
        next(iterator)
        string_addr = next(iterator).to
        string = idc.GetString(string_addr)

        # For some reason the struct includes dummy members that should be skipped.
        if idaapi.get_dword(SAVEDATA_STRUCT + struct_offset) == 0:
            file.write("  int dummy_x%x;\n" % struct_offset)
            struct_offset += 4

        file.write("  int _%s;\n" % string)
        struct_offset += 4

    file.write("};\n\n")
