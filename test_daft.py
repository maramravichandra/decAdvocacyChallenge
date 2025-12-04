
import daft
from matplotlib import rc

# It's good practice to set up matplotlib settings if you want publication-quality figures
# rc("font", family="serif", size=12)
# rc("text", usetex=True) # This requires a LaTeX installation

print("Attempting to create a PGM object...")
try:
    # 1. Initialize the PGM object
    pgm = daft.PGM([3, 3], origin=[0.5, 0.5])

    # 2. Add nodes
    pgm.add_node(daft.Node("A", "A", 1, 2))
    pgm.add_node(daft.Node("B", "B", 2, 2))
    
    # 3. Add an edge
    pgm.add_edge("A", "B")

    # 4. Render and save
    pgm.render()
    pgm.savefig("test_pgm.png")

    print("Successfully created and saved 'test_pgm.png'.")
    print("Your 'daft-pgm' installation is working correctly!")

except Exception as e:
    print(f"An error occurred: {e}")

