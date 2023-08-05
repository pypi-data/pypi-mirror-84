"""
Description: Extracts stack strings
AUTHOR: DC3
"""

from binascii import unhexlify

import idaapi
import idautils
import idc

import kordesii
from kordesii.utils import tracing

# main things to modify based on what you're looking for
STRING_GAP_TOLERANCE = 0  # should generally be 0
MAX_CHARACTER_WIDTH = 2  # should be 1 or 2
MIN_STR_LENGTH = 2  # do not make this less than 1
ALLOW_HEX = False

ASCII = True
MAX_CHARACTER_VALUE = 127 if ASCII else 2 ** (8 * MAX_CHARACTER_WIDTH) - 1

# FE
POS_FIRST = 0
POS_SECOND = 1
POS_THIRD = 2
POS_ALL = 3
POS_DATA = 10
POS_STACK = 20

IGNORED_MNEMONICS = ["cmp", "test"]

# fmt: off
JUMPS = [
    "ja", "jna",
    "jae", "jnae",
    "jb", "jnb",
    "jbe", "jnbe",
    "jc", "jnc",
    "jcxz", "jncxz",
    "jecxz", "jnecxz",
    "jrcxz", "jnrcxz",
    "je", "jne",
    "jg", "jne",
    "jge", "jnge",
    "jl", "jnl",
    "jle", "jnle",
    "jmp",
    "jmpe",
    "jmpf",
    "jo", "jno",
    "jp", "jnp",
    "jpe",
    "jpo",
    "js", "jns",
    "jz", "jnz",
]
# fmt: on


def get_function(ea):
    func = idaapi.func_t()
    func.start_ea = idc.get_func_attr(ea, idc.FUNCATTR_START)
    func.end_ea = idc.get_func_attr(ea, idc.FUNCATTR_END)
    func.flags = idc.get_func_attr(ea, idc.FUNCATTR_FLAGS)
    if idc.BADADDR == func.start_ea or idc.BADADDR == func.end_ea:
        return False
    else:
        return func


def get_functions():
    functions = {}
    for func_ea in idautils.Functions():
        fname = idaapi.get_func_name(func_ea)
        if fname and fname not in list(functions.keys()):
            func = get_function(func_ea)
            if func:
                functions[fname] = func
    return functions


def is_ascii(i):
    """
    Takes an int (supposedly) representing a char.
    """
    return i in [0, 9, 10, 13] or 31 < i < 127


def is_string_ascii(s):
    if isinstance(s, str):
        try:
            s.encode("ascii", errors="strict")
            return True
        except UnicodeEncodeError:
            return False
    for x in s:
        if not is_ascii(x):
            return False
    return True


class StackStrings(object):
    def __init__(self):
        self._strings = set()

    @property
    def strings(self):
        return self._strings

    def strings_in_range(self, start_ea, end_ea):
        strings = []
        for string in self.strings:
            if start_ea <= string.ea < end_ea:
                strings.append((string, "string"))
        return strings

    def get_char(self, char, char_width=1, allow_multi_chars=False, allow_hex=False):
        """
        Decode a character from char given the char_width.

        Returns decoded char, if found, otherwise BADADDR.
        """
        if isinstance(char, bytes):
            return char
        current_max_character_value = min(MAX_CHARACTER_VALUE, 2 ** (8 * char_width) - 1)
        if char == 9 or char == 10 or char == 13 or 31 < char < current_max_character_value:
            return str.encode(chr(char), "unicode-escape")
        elif char == 0:
            return char
        elif char > 2 * current_max_character_value and allow_multi_chars:
            formatted_char = format(int(char), "x").encode()  # format to hex, avoids 0x and L issues
            try:
                decoded = unhexlify(formatted_char)[::-1]  # decode if possible, and reverse it
                if len(decoded) > 1:
                    for thing in decoded:
                        thing = self.get_char(thing, char_width)
                        if not thing or thing == idc.BADADDR:
                            break
                    else:
                        return decoded
            except:
                pass
            try:
                decoded = formatted_char  # otherwise try to force to char
                if len(decoded) > 1:
                    for thing in decoded:
                        thing = self.get_char(thing, char_width)
                        if not thing or thing == idc.BADADDR:
                            break
                    else:
                        return decoded
            except:
                pass
        elif not isinstance(char, Filler) and allow_hex and char_width == 1:
            try:
                return bytes((char,))
            except:
                return idc.BADADDR
        return idc.BADADDR  # failed

    def consolidate_data_fragments(self, stack, continue_on_gap=True):
        """
         Given the stack dict, compresses it into a consolidated form. If continue_on_gap is true, it will be
         a list of chars with nulls terminating the distinct segments, otherwise it returns only the first
         distinct segment.
        """
        consolidated = []
        prev_key = min(stack.keys()) if stack else 0
        for key in sorted(stack.keys()):
            if key - prev_key > STRING_GAP_TOLERANCE + 1:
                if continue_on_gap:
                    consolidated.append((b"\x00", None))
                else:
                    return consolidated
            if stack[key][0] is not None and not isinstance(stack[key][0], Filler):
                consolidated.append(stack[key])
            prev_key = key
        return consolidated

    def extend_string_tuple(self, string_tuple, stack_tuple):
        string_tuple[0] += stack_tuple[0]
        string_tuple[1].append(stack_tuple[1])

    def parse_strings(self, stack, stack_min_value=None, stack_max_value=None, char_width=1):
        """ Attempts to parse strings out of stack. Returns list of string tuple information. """
        strs = []
        valid_key = lambda key: (stack_min_value is None or stack_min_value <= key) and (
            stack_max_value is None or key <= stack_max_value
        )
        stack = self.consolidate_data_fragments(
            {
                key: (self.get_char(value, char_width, allow_hex=ALLOW_HEX), ea)
                for key, (value, ea) in stack.items()
                if valid_key(key)
            },
            stack_min_value is None and stack_max_value is None,
        )
        temp_str = [b"", [], 0]
        current_width = 0
        require_zero = False
        if char_width == 2:
            require_zero = True
        found_zero = True
        for i in range(len(stack)):
            current_entry = stack[i]
            # if isinstance(current_entry[0], str):
            #     current_entry[0] = current_entry[0].encode("latin1")
            if isinstance(current_entry[0], int):
                is_null = current_entry[0] == 0
            elif isinstance(current_entry[0], bytes):
                is_null = all(c == 0 for c in current_entry[0])  # ignore all null strs
            else:
                is_null = bool(current_entry[0])
            if is_null:
                if current_width == char_width:
                    if len(temp_str[0]) >= MIN_STR_LENGTH:
                        strs.append(temp_str)
                    temp_str = [b"", [], 0]
                    current_width = 0
                elif current_width < char_width:
                    current_width += 1
                    found_zero = True
                else:
                    temp_str = [b"", [], 0]
            elif current_entry[0] == idc.BADADDR:
                if current_width < char_width:
                    current_width += 1
                    found_zero = True
                else:
                    if len(temp_str[0]) >= MIN_STR_LENGTH:
                        strs.append(temp_str)
                    current_width = 0
                    temp_str = [b"", [], 0]
            elif current_width == 0 or current_width == char_width:
                if require_zero:
                    if found_zero:
                        found_zero = False
                        self.extend_string_tuple(temp_str, current_entry)
                        temp_str[2] += char_width
                        current_width = 1
                    else:
                        if len(temp_str[0]) >= MIN_STR_LENGTH:
                            strs.append(temp_str)
                        temp_str = [b"", [], 0]
                        current_width = 0
                        found_zero = True
                else:
                    self.extend_string_tuple(temp_str, current_entry)
                    temp_str[2] += char_width
                    current_width = 1
            else:
                temp_str = [b"", [], 0]
                found_zero = False
                self.extend_string_tuple(temp_str, current_entry)
                temp_str[2] += char_width
                current_width = 1
        if len(temp_str[0]) >= MIN_STR_LENGTH and current_width == char_width:
            strs.append(temp_str)
            temp_str = [b"", [], 0]
        return strs

    def report_strings(self, strs, stack, stack_min_value=None, stack_max_value=None):
        """ Parses and returns Stack strings as Strings """
        for char_width in range(1, MAX_CHARACTER_WIDTH + 1):
            parsed_strs = self.parse_strings(stack, stack_min_value, stack_max_value, char_width)
            for string, eas, length in parsed_strs:
                start_ea, end_ea = self.find_start_and_end(eas)
                for string_obj in strs:
                    if string_obj[2] == string and string_obj[0] == start_ea and string_obj[1] == end_ea:
                        break
                else:  # if we didn't break
                    strs.add((start_ea, end_ea, string))
                    old_cmt = idc.get_cmt(eas[0], 0)
                    old_cmt = "" if not old_cmt else old_cmt
                    if not is_string_ascii(string):
                        new_cmt = string.hex()
                        new_cmt = old_cmt + "\nStack String (hex): " + new_cmt
                    else:
                        new_cmt = string.decode("unicode-escape").replace("\\x00", "\nStack String: ")
                        new_cmt = old_cmt + "\nStack String: " + new_cmt
                    new_cmt += "\nSize: " + str(length)
                    new_cmt = "\n".join(list(set(new_cmt.split("\n"))))  # Remove duplicates.
                    idc.set_cmt(eas[0], str(new_cmt).strip("\r\n"), 0)

    def find_start_and_end(self, eas):
        """Find the highest and lowest ea in the given list of eas"""
        eas = [ea for ea in eas if ea is not None]
        eas.sort()
        return eas[0], eas[-1]

    def clear_reg_if_needed(self, reg, regs):
        """Clears the state of a register, if it was known"""
        if reg and reg[0] in list(regs.keys()):
            del regs[reg[0]]

    def set_stack(self, offset, ea, pos, state):
        """
        Sets the stack dictionary, at the given offset, to contain the value at the given position at the given ea,
        performing a lookup in the register dictionary if needed.
        """
        fill = False
        if idc.get_operand_type(ea, pos) == idc.o_imm:
            val = idc.get_operand_value(ea, pos)
            state.stack[offset] = (val, ea)
            fill = True
        else:
            reg = tracing.get_reg_fam(tracing.get_opnd_replacement(ea, pos))
            if reg and reg[0] in state.regs:
                val = state.regs[reg[0]][0]
                state.stack[offset] = (state.regs[reg[0]][0], ea)
                fill = True
        if fill:
            for i in range(0, tracing.get_byte_size_of_operand(ea, pos)):
                state.stack[offset + i] = (val & 0xFF, ea)
                val //= 256

    def handle_lea(self, state):
        """Updates the state of the stack string finding based on an lea instruction"""
        if idc.get_operand_type(state.ea, POS_SECOND) == idc.o_reg:
            source_reg = tracing.get_reg_fam(tracing.get_opnd_replacement(state.ea, POS_SECOND))
            if source_reg and source_reg[0] in state.regs:
                value = state.regs[source_reg[0]]
            else:
                value = None
        else:
            value = tracing.get_operand_value_replacement(state.ea, POS_SECOND, state)
        if value is not None and value in state.stack:
            self.report_strings(state.strs, state.stack)
        self.clear_reg_if_needed(tracing.get_reg_fam(tracing.get_opnd_replacement(state.ea, POS_FIRST)), state.regs)

    def handle_call(self, state):
        """Updates the state of the stack string finding based on a call instruction"""
        stack_pointer = idc.get_spd(state.ea)
        next_ea = state.ea + idc.get_item_size(state.ea)
        stack_pointer_delta = idc.get_sp_delta(next_ea)
        if stack_pointer is not None and stack_pointer_delta is not None:
            next_reg = tracing.get_reg_fam(idc.print_operand(next_ea, POS_FIRST))
            # Caller cleanup handling, vulnerable to instruction reordering though.
            if next_reg and "esp" in next_reg and "add" in idc.print_insn_mnem(next_ea).lower():
                stack_pointer_delta += idc.get_sp_delta(next_ea + idc.get_item_size(next_ea))
            for index in range(stack_pointer, stack_pointer + stack_pointer_delta):
                if index in state.stack:
                    del state.stack[index]

    def handle_mov(self, state):
        """Updates the state of the stack string finding based on a mov instruction"""
        op1 = tracing.get_opnd_replacement(state.ea, POS_FIRST)
        if "[" in op1:
            offset = tracing.get_operand_value_replacement(state.ea, POS_FIRST, state)
            self.set_stack(offset, state.ea, POS_SECOND, state)
        else:
            reg = tracing.get_reg_fam(op1)
            type_ = idc.get_operand_type(state.ea, POS_SECOND)
            if reg:
                if type_ != idc.o_phrase and type_ != idc.o_displ:
                    if type_ == idc.o_reg:
                        reg2 = tracing.get_reg_fam(tracing.get_opnd_replacement(state.ea, POS_SECOND))
                        if reg2 and reg2[0] in state.regs:
                            val = state.regs[reg2[0]][0]
                        else:
                            val = None
                    else:
                        val = idc.get_operand_value(state.ea, POS_SECOND)
                    if val is not None:
                        state.regs[reg[0]] = (val, state.ea)
                else:
                    offset = tracing.get_operand_value_replacement(state.ea, POS_SECOND, state)
                    value = state.stack.get(offset, None)
                    if value is not None:
                        state.regs[reg[0]] = value
                    else:
                        self.clear_reg_if_needed(reg, state.regs)

    def get_stack_strings(self, functions):
        """
        Finds all the stack strings it can in the given functions.

        Parameters set globally:
            STRING_GAP_TOLERANCE - the gap allowed between string characters.
            MAX_CHARACTER_WIDTH  - the maximum character size, in bytes
            ASCII                - Whether character values must be 0-127
        """
        stack_strings = []
        for func in functions:
            state = tracing.BranchingTraceState(func.start_ea)
            state.strs = set()
            states = [state]
            func_eas = []
            ea = state.ea
            while ea < func.end_ea:
                func_eas.append(ea)
                ea += idc.get_item_size(ea)
            while states:
                state = states.pop()
                while state.ea < func.end_ea:
                    try:
                        func_eas.remove(state.ea)
                    except:
                        pass
                    state.visited_eas.append(state.ea)
                    mnemonic = idc.print_insn_mnem(state.ea)
                    if mnemonic in IGNORED_MNEMONICS:
                        pass
                    elif "pop" in mnemonic:
                        reg = tracing.get_reg_fam(tracing.get_opnd_replacement(state.ea, POS_FIRST))
                        if reg:
                            value = state.stack.get(idc.get_spd(state.ea), None)
                            if value is not None:
                                state.regs[reg[0]] = value
                            else:
                                self.clear_reg_if_needed(reg, state.regs)
                    elif "push" in mnemonic:
                        # bug where idc.get_spd was not correctly tracking the pointer,
                        # this case also hasn't really been seen often as part of a stack string
                        # self.set_stack(idc.get_spd(ea), ea, POS_FIRST, regs, stack)
                        pass
                    elif "mov" in mnemonic:
                        self.handle_mov(state)
                    elif (
                        (
                            "xor" in mnemonic
                            and tracing.get_reg_fam(tracing.get_opnd_replacement(state.ea, POS_FIRST))
                            == tracing.get_reg_fam(tracing.get_opnd_replacement(state.ea, POS_SECOND))
                        )
                        or ("lea" in mnemonic and idc.print_operand(state.ea, POS_SECOND) == "[0]")
                        or (
                            "sub" in mnemonic
                            and tracing.get_opnd_replacement(state.ea, POS_FIRST)
                            == tracing.get_opnd_replacement(state.ea, POS_SECOND)
                        )
                    ):
                        reg = tracing.get_reg_fam(tracing.get_opnd_replacement(state.ea, POS_FIRST))
                        if reg:
                            state.regs[reg[0]] = (0, state.ea)
                    elif "loop" in mnemonic or "movsb" in mnemonic:
                        state.regs["rcx"] = (0, state.ea)
                    elif mnemonic in JUMPS:
                        try:
                            target = next(idautils.CodeRefsFrom(state.ea, 0))
                        except StopIteration:
                            target = None
                        if target and target not in state.visited_eas:
                            if func.end_ea > target >= func.start_ea:
                                state.visited_eas.append(target)
                                new_state = tracing.BranchingTraceState(target, state)
                                new_state.strs = state.strs
                                states.append(new_state)
                            else:
                                self.report_strings(state.strs, state.stack)
                        # Always follow an unconditional jump
                        if mnemonic == "jmp":
                            break
                    elif (
                        "rep" in idc.GetDisasm(state.ea).split(" ")[0]
                        and "scas" not in idc.GetDisasm(state.ea).split(" ")[1]
                    ):
                        self.report_strings(state.strs, state.stack)
                    elif "lea" in mnemonic:
                        self.handle_lea(state)
                    elif "call" in mnemonic:
                        self.handle_call(state)
                    elif "ret" in mnemonic:
                        break
                    elif (
                        idc.get_operand_type(state.ea, POS_FIRST) == idc.o_reg
                    ):  # If we find a target register we were tracking, stop tracking it.
                        self.clear_reg_if_needed(
                            tracing.get_reg_fam(tracing.get_opnd_replacement(state.ea, POS_FIRST)), state.regs
                        )
                    state.ea += idc.get_item_size(state.ea)
                self.report_strings(state.strs, state.stack)
                if not states and func_eas:
                    new_state = tracing.BranchingTraceState(func_eas[0])
                    new_state.strs = set()
                    states.append(new_state)
                stack_strings.extend(state.strs)
        self.strings.update(stack_strings)


class Filler(object):
    """A class to represent the space that a wide char takes up during stack string finding"""

    def __new__(cls, *args, **kwargs):
        instance = cls.__dict__.get("__instance__", None)
        if instance is None:
            instance = super(Filler, cls).__new__(cls)
            instance.__init__()
            cls.__instance__ = instance
        return instance

    def __init__(self):
        super(Filler, self).__init__()

    def __bool__(self):
        return False

    def __int__(self):
        return 0

    def __long__(self):
        return self.__int__()


def getstackstrings():
    """
    Performs the work of retrieving the stack strings.

    :return: StackStrings object
    """
    stacked = StackStrings()
    functions = list(get_functions().values())
    stacked.get_stack_strings(functions)
    return stacked


@kordesii.decoder_entry
def main():
    stacked = getstackstrings()

    print("\n")
    for loc, end, string in sorted(stacked.strings, key=lambda tup: tup[0]):
        func_name: str = idaapi.get_func_name(loc)
        line = func_name.encode() + f", 0x{loc:X}: \x00".encode() + string + b'"'  # Use the \x00 for the replace below
        print((line.replace(b"\\x00", b'"\n\t\t"').replace(b'"\n', b"\n", 1) + b"\n").decode())
        kordesii.append_string(string.replace(b"\\x00", b"\n"))
    print("Found " + str(len(stacked.strings)) + " stack strings.")
