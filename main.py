class CurlyScript:
    def __init__(self):
        self.memory = [0] * 3000
        self.pointer = 0

    
    def parse_cell_offset(self, encoded):
        if not encoded:
            return 0
        
        if encoded.startswith("}"):
            count = 0
            for c in encoded:
                if c == "}":
                    count += 1
                else: 
                    break
            return count
        elif encoded.startswith("{"):
            count = 0
            for c in encoded:
                if c == "{":
                    count += 1
                else: 
                    break
            return -count
        else:
            return 0

    def parse_number(self, encoded):
        if not encoded:
            return 0
        
        number = ""
        i = 0

        while i < len(encoded):
            brace_count = 0
            current_brace = encoded[i]

            # Count consecutive braces of same type
            while i < len(encoded) and encoded[i] == current_brace:
                brace_count += 1
                i += 1
            
            digit = brace_count - 1
            if digit < 0 or digit > 9:
                raise ValueError(f"Invalid digit encoding: {brace_count} brackets gives digit {digit}")
            
            number += str(digit)

        return int(number) if number else 0
    
    def run(self, code):
        lines = code.strip().split('\n')

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            try:
                self.execute_line(line)
            except Exception as e:
                print(f"Error on line {line_num}: {e}")
                print(f"Line: {line}")
                self.debug_state()
                break
    
    def execute_line(self, line):
        tokens = line.split()
        if not tokens:
            return
            
        command = tokens[0]
        operands = tokens[1:]

        if command == "{}":
            # SET command
            if len(operands) < 2:
                raise ValueError(f"SET command requires number and data type, got: {operands}")
            
            encoded_number = operands[0]
            data_type = operands[1]
            
            value = self.parse_number(encoded_number)
            
            if data_type == "{{}}":  # ASCII
                self.memory[self.pointer] = value
            elif data_type == "}}":  # Digit
                self.memory[self.pointer] = value
            else:
                raise ValueError(f"Unknown data type: {data_type}")
        
        elif command == "{}}":
            # MOVE RIGHT
            old_pointer = self.pointer
            self.pointer = (self.pointer + 1) % len(self.memory)

        elif command == "{{}":
            # MOVE LEFT
            old_pointer = self.pointer
            self.pointer = (self.pointer - 1) % len(self.memory)

        elif command == "{{}}":
            # PRINT current cell
            value = self.memory[self.pointer]
            
            if value >= 32 and value <= 126:
                # Printable ASCII
                print(chr(value), end='')
            else:
                # Print as number
                print(value, end='')
        
        elif command == "{{{}}}":
            # PRINT NEWLINE
            print()
        
        # Binary Operations
        elif command == "{}{}":
            # ADD operation
            self._binary_operation(operands, lambda a, b: a + b, "ADD")
        
        elif command == "{}{}{}":
            # SUBTRACT operation
            self._binary_operation(operands, lambda a, b: a - b, "SUB")
        
        elif command == "{}{}{}{}":
            # MULTIPLY operation
            self._binary_operation(operands, lambda a, b: a * b, "MUL")
        
        elif command == "{}{}{}{}{}":
            # DIVIDE operation
            self._binary_operation(operands, lambda a, b: a // b if b != 0 else 0, "DIV")
        
        else:
            raise ValueError(f"Unknown command: {command}")
    
    def _binary_operation(self, operands, operation, op_name):
        """Helper method to handle binary operations"""
        
        if len(operands) == 0:
            # No operands given - operate current cell with itself
            offset1 = 0
            offset2 = 0
        elif len(operands) == 1:
            # One operand given - operate current cell with cell at offset
            offset1 = 0
            offset2 = self.parse_cell_offset(operands[0])
        elif len(operands) == 2:
            # Two operands given
            offset1 = self.parse_cell_offset(operands[0])
            offset2 = self.parse_cell_offset(operands[1])
        else:
            raise ValueError(f"Binary operation requires 0, 1, or 2 offset operands, got {len(operands)}")
        
        # Calculate target memory positions
        pos1 = (self.pointer + offset1) % len(self.memory)
        pos2 = (self.pointer + offset2) % len(self.memory)
        
        
        # Perform operation: memory[pos1] = memory[pos1] operation memory[pos2]
        try:
            result = operation(self.memory[pos1], self.memory[pos2])
            self.memory[pos1] = result
        except ZeroDivisionError:
            self.memory[pos1] = 0  # Handle division by zero
    
    def debug_state(self):
        print(f"[DEBUG] Pointer: {self.pointer}, Value: {self.memory[self.pointer]}")
        start = max(0, self.pointer - 3)
        end = min(len(self.memory), self.pointer + 4)
        memory_slice = self.memory[start:end]

        print("[DEBUG] Memory: ", end="")
        for i, value in enumerate(memory_slice):
            pos = start + i
            if pos == self.pointer:
                print(f"[{value}]", end=" ")
            else:
                print(f"{value}", end=" ")
        print()

def print_syntax():
    print("CurlyScript Assembly - Never Enough Braces")
    print("=" * 60)
    print("COMMANDS:")
    print("  {} [number] {{}}   - SET cell to number as ASCII")
    print("  {} [number] }}     - SET cell to number as digit")
    print("  {}}                - MOVE pointer RIGHT")
    print("  {{}                - MOVE pointer LEFT")
    print("  {{}}               - PRINT current cell")
    print("  {{{}}}             - PRINT newline")
    print()
    print("NUMBER ENCODING:")
    print("  Each digit = (bracket_count - 1)")
    print("  Concatenate patterns for multi-digit numbers")
    print()
    print("EXAMPLES:")
    print("  }} = digit 1 (2 brackets - 1)")
    print("  { = digit 0 (1 bracket - 1)")
    print("  }}}}}} = digit 5 (6 brackets - 1)")
    print("  72 = }}}}}}}}{}} (7 = 8 brackets, 2 = 3 brackets)")
    print("  105 = }}{}}}}}} (1, 0, 5)")
    print()
    print("BINARY OPERATIONS:")
    print("  Format = binary_operator [offset_1] [offset_2]")
    print("  Result stored in cell at offset_1 (or current if no offsets)")
    print()
    print("{}{}         - ADD")
    print("{}{}{}       - SUBTRACT") 
    print("{}{}{}{}     - MULTIPLY")
    print("{}{}{}{}{}   - DIVIDE")
    print()
    print("OFFSET EXAMPLES:")
    print("  {{     - 2 cells to the left")
    print("  {     - 1 cell to the left")
    print("  (none) - current cell (offset 0)")
    print("  }     - 1 cell to the right")
    print("  }}   - 2 cells to the right")
    print()
    print("=" * 60)


def test_curlyscript():
    print("=== TESTING CURLYSCRIPT ASSEMBLY ===")

    # Test 1: Print "Hi"
    cs = CurlyScript()
    hello_code = """
{} }}}}}}}}{{{ {{}}
{{}}
{}}
{} }}{}}}}}} {{}}
{{}}
{{{}}}
"""
    print("Test 1: Print 'Hi'")
    cs.run(hello_code)

    # Test 2: Print "27"
    cs = CurlyScript()
    number_code = """
{} }}} }}
{{}}
{}}
{} }}}}}}}} }}
{{}}
{{{}}}
"""
    print("\nTest 2: Print '27'")
    cs.run(number_code)

    # Test 3: Print "Hannah"
    cs = CurlyScript()
    hannah_code = """
{} }}}}}}}}{{{ {{}}
{{}}
{}}
{} }}}}}}}}}}{{{{{{{{ {{}}
{{}}
{}}
{} }}{{} {{}}
{{}}
{}}
{} }}{{} {{}}
{{}}
{}}
{} }}}}}}}}}}{{{{{{{{ {{}}
{{}}
{}}
{} }}{}}}}} {{}}
{{}}
{{{}}}
"""
    print("\nTest 3: Print 'Hannah'")
    cs.run(hannah_code)

def test_binary_operations():
    print("\n=== TESTING BINARY OPERATIONS ===")
    
    # Test 1: Addition (5 + 3 = 8)
    cs = CurlyScript()
    addition_test = """
{} }}}}}} }}
{}}
{} }}}} }}
{{}
{}{} }
{{}}
{{{}}}
"""
    print("\nTest 1: Addition (5 + 3):")
    cs.run(addition_test)
    
    # Test 2: Simple multiplication (3 * 3 = 9)
    cs = CurlyScript()
    simple_test = """
{} }}}} }}
{}{}{}{}
{{}}
{{{}}}
"""
    print("Test 2: Simple Multiplication (3 * 3):")
    cs.run(simple_test)
    
    # Test 3: Subtraction (10 - 4 = 6)
    cs = CurlyScript()
    subtraction_test = """
{} }}{ }}
{}}
{} }}}}} }}
{{}
{}{}{} }
{{}}
{{{}}}
"""
    print("Test 3: Subtraction (10 - 4):")
    cs.run(subtraction_test)
    
    # Test 4: Division (15 / 3 = 5)
    cs = CurlyScript()
    division_test = """
{} }}{{{{{{ }}
{}}
{} }}}} }}
{{}
{}{}{}{}{} }
{{}}
{{{}}}
"""
    print("Test 4: Division (15 / 3):")
    cs.run(division_test)

def interactive_mode():
    cs = CurlyScript()

    print("\nInteractive Mode")
    print("Commands: 'quit', 'help', 'debug', 'test', 'test_binary', or enter CurlyScript code")
    print("=" * 60)

    while True:
        try:
            code = input("\nCurlyScript> ").strip()
        
            if code.lower() == "quit":
                print("Thanks for trying CurlyScript!")
                break
            elif code.lower() == "help":
                print_syntax()
            elif code.lower() == "debug":
                cs.debug_state()
            elif code.lower() == "test":
                print("Testing: Set cell to 65 (A) and print as ASCII")
                cs.run("{} }}}}}}}{{{{ {{}}\n{{}}")
            elif code.lower() == "test_binary":
                test_binary_operations()
            elif code == "":
                continue
            else:
                if all(c in '{} \n#' for c in code):
                    cs.run(code)
                else:
                    print("Error: Only {, }, space, newlines, and # allowed.")
        
        except KeyboardInterrupt:
            print("\nThanks for trying CurlyScript!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_curlyscript()
    test_binary_operations()
    interactive_mode()
