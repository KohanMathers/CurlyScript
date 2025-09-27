# CurlyScript
I can't come up with a reasonable explanation as to why I made this, just know I did and it was worth it.

---

## Commands
- `{} [number] {{}}` – SET cell to number as **ASCII**  
- `{} [number] }}` – SET cell to number as **digit**  
- `}}` – MOVE pointer **RIGHT**  
- `{{` – MOVE pointer **LEFT**  
- `{{}}` – PRINT current cell  
- `{{{}}}` – PRINT newline  

---

## Number Encoding
- Each digit = `(bracket_count - 1)`  
- Concatenate patterns for multi-digit numbers  

**Examples**:  
- `}}` → digit **1** (2 brackets – 1)  
- `{` → digit **0** (1 bracket – 1)  
- `}}}}}}` → digit **5** (6 brackets – 1)  
- `72` → `}}}}}}}}}}}}` (7 = 8 brackets, 2 = 3 brackets)  
- `105` → `}}{{}}}}}` (1, 0, 5)  

---

## Binary Operations
Format:  
```
binary_operator [offset_1] [offset_2]
```
- Result stored in cell at **offset_1** (or current cell if no offsets provided)

Operators:  
- `{}{}` – ADD  
- `{}{}{} `– SUBTRACT  
- `{}{}{}{}` – MULTIPLY  
- `{}{}{}{}{}` – DIVIDE  

---

## Offset Examples
- `{{` – 2 cells to the left  
- `{` – 1 cell to the left  
- *(none)* – current cell (offset 0)  
- `}` – 1 cell to the right  
- `}}` – 2 cells to the right  

---
## Example Programs

### Print "Hi"
```
{} }}}}}}}}{{{ {{}} # SET cell to 72 ('H') as ASCII
{{}} # Print
{}} # Move right
{} }}{}}}}}} {{}}
{{}}
{{{}}} # Newline
```


### Print "123"
```
{} }} }} # SET cell to 1 as digit
{{}} # Print
{}} # Move right
{} }}} }}
{{}}
{}}
{} }}}} }}
{{}}
{{{}}} # Newline
```


### Add Two Numbers
```
{} }} }} # SET cell to 1 as digit
{}} # Move right
{} }}}}} }}
{}{} { # ADD current cell to (cell_offset - 1)
{{}} # Print result
{{{}}} # Newline
```
