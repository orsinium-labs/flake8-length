print(1 + 2 * 3)        # L15
print("hello")          # L5
print("hello world")    # L5
print("really-really-long-word")  # L5
print("""               # L9
    hello world         # L15
""")                    # L3
print(                  # L5
    """                 # L7
        hello world     # L19
    """                 # L7
)
print(                  # L5
    """hello world      # L18
    """                 # L7
)

# see also: https://github.com/life4/deal       # L22
# https://github.com/life4/deal                 # L12
"SELECT * FROM table_with_very_long_name"       # L25
q = "SELECT * FROM table_with_very_long_name"   # L29
print(q)                                        # L7
print(                                          # L5
    "SELECT * FROM table_with_very_long_name"   # L29
)
print(                                          # L5
    "SELECT * FROM table_with_very_long_name",  # L29
)
print("see also https://github.com/life4/deal")  # L5
