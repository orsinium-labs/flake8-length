print(1 + 2 * 3)        # L16
print("hello")          # L14
print("hello world")    # L20
print("really-really-long-word")  # L32
print("""               # L9
    hello world         # L15
""")                    # L4
print(                  # L6
    """                 # L7
        hello world     # L19
    """                 # L7
)                       # L1
print(                  # L6
    """hello world      # L18
    """                 # L7
)                       # L1

# see also: https://github.com/life4/deal       # L22
# https://github.com/life4/deal                 # L12
"SELECT * FROM table_with_very_long_name"       # L25
q = "SELECT * FROM table_with_very_long_name"   # L29
print(q)  # L8
